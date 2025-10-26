# 🎙️ Advanced Voice Editor

A powerful web-based audio editing application built with Streamlit that provides professional-grade voice and audio manipulation tools.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### Audio Effects
- **🎵 Pitch Shifting** - Adjust pitch ±12 semitones without affecting playback speed
- **⏱️ Time Stretching** - Change speed from 0.5x to 2x without altering pitch
- **🔊 Volume Control** - Precise gain adjustment in decibels (-20dB to +20dB)
- **🎚️ 3-Band Equalizer** - Independent control for:
  - Bass (< 200 Hz)
  - Mid (200 Hz - 2 kHz)
  - Treble (> 2 kHz)
- **🔇 Noise Reduction** - Advanced spectral gating to remove background noise
- **🏛️ Reverb** - Customizable room ambience with adjustable room size
- **📢 Echo Effect** - Configurable delay (0-1000ms) and decay parameters
- **🤖 Robot Voice** - Ring modulation for synthetic voice effects

### Visualization
- **📊 Waveform Comparison** - Side-by-side view of original and processed audio
- **🌈 Spectrogram** - Frequency-time analysis with logarithmic scale
- **🎨 Interactive Plots** - Powered by Plotly for zoom and hover details

### I/O Capabilities
- **📁 Multiple Format Support** - WAV, MP3, OGG, FLAC
- **🔊 Real-time Playback** - Compare original and processed audio instantly
- **💾 Export** - Download processed audio as high-quality WAV files

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository** (or create a new directory)
```bash
mkdir voice-editor
cd voice-editor
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install required packages**
```bash
pip install streamlit numpy librosa soundfile scipy plotly
```

### Package Details
- `streamlit` - Web application framework
- `numpy` - Numerical computing
- `librosa` - Audio analysis and processing
- `soundfile` - Audio file I/O
- `scipy` - Signal processing algorithms
- `plotly` - Interactive visualizations

## 📖 Usage

### Starting the Application

1. **Save the code** as `voice_editor.py`

2. **Run the Streamlit app**
```bash
streamlit run voice_editor.py
```

3. **Open your browser** - The app will automatically open at `http://localhost:8501`

### Workflow

1. **Upload Audio File**
   - Click "Browse files" or drag and drop
   - Supported formats: WAV, MP3, OGG, FLAC

2. **Adjust Effects**
   - Use sliders in the left panel to configure effects
   - Effects can be combined for complex processing
   - Changes are non-destructive to the original

3. **Apply Processing**
   - Click "🎵 Apply Effects" to process audio
   - View real-time waveform and spectrogram updates

4. **Compare Results**
   - Listen to original vs processed audio
   - Analyze waveform and frequency changes

5. **Export**
   - Click "⬇️ Download Processed Audio"
   - Save as WAV file for further use

## 🎛️ Effect Guidelines

### Pitch Shifting
- **+12 semitones** = One octave higher (chipmunk effect)
- **-12 semitones** = One octave lower (deep voice)
- **±1-3 semitones** = Subtle pitch correction

### Time Stretching
- **0.5x** = Half speed (slower, deeper feel)
- **2.0x** = Double speed (faster playback)
- Use with pitch shifting for creative effects

### Equalizer
- **Boost bass** (+5 to +10 dB) for warmth
- **Cut mid** (-3 to -5 dB) to reduce muddiness
- **Boost treble** (+3 to +7 dB) for clarity and presence

### Noise Reduction
- **0.3-0.5** = Light noise removal (preserve quality)
- **0.7-1.0** = Aggressive removal (may affect voice)
- Best for constant background noise

### Reverb
- **Small room** (0.1-0.3) = Subtle ambience
- **Large hall** (0.7-1.0) = Cathedral-like space
- Amount: 0.2-0.4 for natural sound

## 🔧 Technical Details

### Audio Processing Pipeline
1. File upload and decoding (librosa)
2. Mono conversion for consistency
3. Effect chain application
4. Normalization to prevent clipping
5. Real-time visualization generation

### Signal Processing Techniques
- **Pitch shift**: Phase vocoder algorithm
- **Time stretch**: WSOLA (Waveform Similarity Overlap-Add)
- **EQ**: Butterworth band filters (2nd order)
- **Noise reduction**: Spectral gating with soft masking
- **Reverb**: Convolution with impulse response
- **Echo**: Time-domain delay lines

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**
```bash
pip install --upgrade streamlit librosa soundfile scipy plotly numpy
```

**Audio won't load**
- Ensure file format is supported (WAV, MP3, OGG, FLAC)
- Check file isn't corrupted
- Try converting to WAV format first

**Processing is slow**
- Large files (>5 minutes) may take time
- Reduce sample rate if needed
- Close other applications

**Distorted output**
- Reduce volume/gain settings
- Lower effect intensities
- The app auto-normalizes, but extreme settings can still distort

## 📝 Tips & Best Practices

1. **Start subtle** - Small adjustments often sound more natural
2. **Use effects in order** - Pitch → Time → EQ → Effects → Volume
3. **Monitor waveform** - Avoid clipping (peaks touching ±1.0)
4. **Combine carefully** - Too many effects can degrade quality
5. **Save originals** - Always keep backup of source audio

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional effects (chorus, flanger, compression)
- Batch processing capabilities
- Preset management system
- Multi-track support
- Advanced noise profiling

## 📄 License

This project is licensed under the MIT License - feel free to use, modify, and distribute.

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - App framework
- [Librosa](https://librosa.org/) - Audio processing
- [SciPy](https://scipy.org/) - Scientific computing
- [Plotly](https://plotly.com/) - Interactive visualizations

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Made with ❤️ for audio enthusiasts, podcasters, and content creators**
