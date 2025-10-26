import streamlit as st
import numpy as np
import librosa
import soundfile as sf
from scipy import signal
from io import BytesIO
import plotly.graph_objects as go

st.set_page_config(page_title="Advanced Voice Editor", layout="wide")

st.title("🎙️ Advanced Voice Editor")

# Initialize session state
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
    st.session_state.sample_rate = None
    st.session_state.processed_audio = None

# File upload
uploaded_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3', 'ogg', 'flac'])

if uploaded_file:
    # Load audio
    audio_bytes = uploaded_file.read()
    audio_data, sample_rate = librosa.load(BytesIO(audio_bytes), sr=None, mono=True)
    st.session_state.audio_data = audio_data
    st.session_state.sample_rate = sample_rate
    st.session_state.processed_audio = audio_data.copy()
    
    st.success(f"✅ Loaded: {uploaded_file.name} | Sample Rate: {sample_rate} Hz | Duration: {len(audio_data)/sample_rate:.2f}s")

if st.session_state.audio_data is not None:
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Audio Effects")
        
        # Pitch shifting
        st.markdown("### Pitch Control")
        pitch_shift = st.slider("Pitch Shift (semitones)", -12.0, 12.0, 0.0, 0.5)
        
        # Time stretching
        st.markdown("### Time Stretch")
        time_stretch = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)
        
        # Volume control
        st.markdown("### Volume")
        volume = st.slider("Gain (dB)", -20.0, 20.0, 0.0, 1.0)
        
        # Equalizer
        st.markdown("### Equalizer")
        bass = st.slider("Bass (< 200Hz)", -20.0, 20.0, 0.0, 1.0)
        mid = st.slider("Mid (200Hz - 2kHz)", -20.0, 20.0, 0.0, 1.0)
        treble = st.slider("Treble (> 2kHz)", -20.0, 20.0, 0.0, 1.0)
        
        # Noise reduction
        st.markdown("### Noise Reduction")
        noise_reduction = st.slider("Strength", 0.0, 1.0, 0.0, 0.1)
        
        # Reverb
        st.markdown("### Reverb")
        reverb_amount = st.slider("Reverb Amount", 0.0, 1.0, 0.0, 0.1)
        room_size = st.slider("Room Size", 0.1, 1.0, 0.5, 0.1)
        
        # Echo
        st.markdown("### Echo")
        echo_delay = st.slider("Echo Delay (ms)", 0, 1000, 0, 50)
        echo_decay = st.slider("Echo Decay", 0.0, 0.9, 0.0, 0.1)
        
        # Robot voice
        st.markdown("### Special Effects")
        robot_voice = st.checkbox("Robot Voice")
        
        # Process button
        if st.button("🎵 Apply Effects", type="primary"):
            with st.spinner("Processing audio..."):
                processed = st.session_state.audio_data.copy()
                sr = st.session_state.sample_rate
                
                # Pitch shift
                if pitch_shift != 0:
                    processed = librosa.effects.pitch_shift(processed, sr=sr, n_steps=pitch_shift)
                
                # Time stretch
                if time_stretch != 1.0:
                    processed = librosa.effects.time_stretch(processed, rate=time_stretch)
                
                # Volume adjustment
                if volume != 0:
                    processed = processed * (10 ** (volume / 20))
                
                # Equalizer
                if bass != 0 or mid != 0 or treble != 0:
                    # Bass filter (< 200 Hz)
                    sos_bass = signal.butter(2, 200, btype='low', fs=sr, output='sos')
                    bass_filtered = signal.sosfilt(sos_bass, processed)
                    
                    # Mid filter (200 Hz - 2000 Hz)
                    sos_mid = signal.butter(2, [200, 2000], btype='band', fs=sr, output='sos')
                    mid_filtered = signal.sosfilt(sos_mid, processed)
                    
                    # Treble filter (> 2000 Hz)
                    sos_treble = signal.butter(2, 2000, btype='high', fs=sr, output='sos')
                    treble_filtered = signal.sosfilt(sos_treble, processed)
                    
                    # Combine with gains
                    processed = (bass_filtered * (10 ** (bass / 20)) + 
                               mid_filtered * (10 ** (mid / 20)) + 
                               treble_filtered * (10 ** (treble / 20))) / 3
                
                # Noise reduction using spectral gating
                if noise_reduction > 0:
                    S = librosa.stft(processed)
                    S_mag = np.abs(S)
                    S_phase = np.angle(S)
                    
                    # Estimate noise floor
                    noise_floor = np.percentile(S_mag, 10, axis=1, keepdims=True)
                    
                    # Apply soft gating
                    mask = (S_mag / (noise_floor + 1e-10)) ** (1 - noise_reduction)
                    mask = np.minimum(mask, 1.0)
                    
                    S_clean = S_mag * mask * np.exp(1j * S_phase)
                    processed = librosa.istft(S_clean, length=len(processed))
                
                # Reverb (simple convolution-based)
                if reverb_amount > 0:
                    reverb_length = int(sr * room_size * 0.5)
                    reverb_ir = np.exp(-np.linspace(0, 5, reverb_length)) * np.random.randn(reverb_length)
                    reverb_ir = reverb_ir / np.max(np.abs(reverb_ir))
                    
                    reverb_signal = signal.convolve(processed, reverb_ir, mode='same')
                    processed = (1 - reverb_amount) * processed + reverb_amount * reverb_signal
                
                # Echo
                if echo_delay > 0 and echo_decay > 0:
                    delay_samples = int(sr * echo_delay / 1000)
                    echo_signal = np.zeros_like(processed)
                    
                    for i in range(3):  # 3 echoes
                        delay_pos = delay_samples * (i + 1)
                        if delay_pos < len(processed):
                            echo_signal[delay_pos:] += processed[:-delay_pos] * (echo_decay ** (i + 1))
                    
                    processed = processed + echo_signal
                
                # Robot voice effect
                if robot_voice:
                    # Vocoder-like effect using ring modulation
                    carrier_freq = 200  # Hz
                    t = np.arange(len(processed)) / sr
                    carrier = np.sin(2 * np.pi * carrier_freq * t)
                    processed = processed * carrier
                
                # Normalize to prevent clipping
                max_val = np.max(np.abs(processed))
                if max_val > 0.95:
                    processed = processed * (0.95 / max_val)
                
                st.session_state.processed_audio = processed
                st.success("✅ Effects applied successfully!")
    
    with col2:
        st.subheader("📊 Audio Visualization")
        
        # Waveform comparison
        fig = go.Figure()
        
        time_orig = np.linspace(0, len(st.session_state.audio_data) / st.session_state.sample_rate, 
                                len(st.session_state.audio_data))
        time_proc = np.linspace(0, len(st.session_state.processed_audio) / st.session_state.sample_rate, 
                                len(st.session_state.processed_audio))
        
        # Downsample for visualization
        downsample = max(1, len(time_orig) // 5000)
        
        fig.add_trace(go.Scatter(
            x=time_orig[::downsample], 
            y=st.session_state.audio_data[::downsample],
            mode='lines',
            name='Original',
            line=dict(color='blue', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_proc[::downsample], 
            y=st.session_state.processed_audio[::downsample],
            mode='lines',
            name='Processed',
            line=dict(color='red', width=1)
        ))
        
        fig.update_layout(
            title="Waveform Comparison",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            height=300,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Spectrogram
        st.markdown("### Spectrogram (Processed)")
        D = librosa.amplitude_to_db(np.abs(librosa.stft(st.session_state.processed_audio)), ref=np.max)
        
        fig_spec = go.Figure(data=go.Heatmap(
            z=D,
            x=np.linspace(0, len(st.session_state.processed_audio) / st.session_state.sample_rate, D.shape[1]),
            y=librosa.fft_frequencies(sr=st.session_state.sample_rate),
            colorscale='Viridis',
            colorbar=dict(title="dB")
        ))
        
        fig_spec.update_layout(
            title="Spectrogram",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            height=300,
            yaxis_type='log'
        )
        
        st.plotly_chart(fig_spec, use_container_width=True)
        
        # Audio players
        st.markdown("### 🔊 Listen")
        
        col_play1, col_play2 = st.columns(2)
        
        with col_play1:
            st.markdown("**Original Audio**")
            original_bytes = BytesIO()
            sf.write(original_bytes, st.session_state.audio_data, st.session_state.sample_rate, format='WAV')
            st.audio(original_bytes.getvalue(), format='audio/wav')
        
        with col_play2:
            st.markdown("**Processed Audio**")
            processed_bytes = BytesIO()
            sf.write(processed_bytes, st.session_state.processed_audio, st.session_state.sample_rate, format='WAV')
            st.audio(processed_bytes.getvalue(), format='audio/wav')
        
        # Download processed audio
        st.markdown("### 💾 Download")
        download_bytes = BytesIO()
        sf.write(download_bytes, st.session_state.processed_audio, st.session_state.sample_rate, format='WAV')
        
        st.download_button(
            label="⬇️ Download Processed Audio",
            data=download_bytes.getvalue(),
            file_name="processed_audio.wav",
            mime="audio/wav"
        )

else:
    st.info("👆 Upload an audio file to get started")
    
    st.markdown("""
    ### Features:
    - 🎵 **Pitch Shifting**: Change the pitch without affecting speed
    - ⏱️ **Time Stretching**: Change speed without affecting pitch
    - 🔊 **Volume Control**: Adjust overall audio level
    - 🎚️ **3-Band Equalizer**: Control bass, mid, and treble frequencies
    - 🔇 **Noise Reduction**: Remove background noise using spectral gating
    - 🏛️ **Reverb**: Add room ambience with adjustable size
    - 📢 **Echo**: Create delay effects
    - 🤖 **Robot Voice**: Apply vocoder-like effects
    - 📊 **Real-time Visualization**: Waveform and spectrogram display
    - 💾 **Export**: Download processed audio as WAV
    """)