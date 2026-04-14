# SenseTestingAudioMachOne

🎙️ Audio Recording & Transcription Tool

A web-based audio recorder that captures speech and automatically transcribes it to text using OpenAI's Whisper model. Record 30-second audio clips directly from your browser and get instant transcriptions with a single click.

🛠️ Requirements

Before you start, you need two things installed on your computer (these are NOT Python libraries):

IF YOU ALREADY HAVE PYTHON INSTALLED, SKIP PAST TO FFmpeg. 

**Python (3.9 or higher):** Download from [python.org](https://python.org). During installation, check the box that says "Add Python to PATH".

**FFmpeg:** A media engine that handles audio and video conversion.
- **Mac:** Open Terminal and run: `brew install ffmpeg`
- **Windows:** Run in PowerShell: `winget install ffmpeg` (or follow [this guide](https://ffmpeg.org/download.html))

After installing FFmpeg, restart your terminal/PowerShell.

🚀 Setup Instructions
Follow these steps in order to get the project running on your machine.

1. Clone the Project
Download this repository as a ZIP file and extract it, or use Git:

Bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. Install Python Dependencies

Run the following command in your terminal/command prompt to install all required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install these packages individually:
```bash
pip install flask pydub openai-whisper transformers torch
```

**What each package does:**
- **flask:** Web server framework for the recorder interface
- **pydub:** Converts audio files to .mp3 format
- **openai-whisper:** AI model for transcribing audio to text
- **transformers:** Framework for machine learning models
- **torch:** Machine learning engine (required by transformers)

🖥️ How to Use

1. **Start the Flask Server**
   
   Open your terminal and run:
   ```bash
   python server.py
   ```
   You should see output indicating the server is running, typically on `http://localhost:5000`.

2. **Open in Your Browser**
   
   Navigate to `http://localhost:5000` in your web browser.

3. **Record Audio**
   
   - Click **"Start Recording"** to begin recording (30-second limit)
   - Click **"Stop Recording"** or wait for the timer to complete
   - Your recording will be saved and appear in the "Saved Recordings" list

4. **Transcribe**
   
   - Click the **"Transcribe"** button next to any recording
   - The server will process the audio (conversion to .mp3, then transcription)
   - The transcript will appear below the recording (may take 30-60 seconds)

5. **Save Audio Files**
   
   - Click the **"Save"** link to download the .webm audio file to your computer
   - Processed .mp3 and transcript data are stored server-side in the `recordings/` folder

📂 Project Structure
- **server.py:** Flask web server that serves the recorder interface and handles transcription requests
- **templates/recorder.html:** Web interface for recording and transcribing audio
- **AudioConversionToTranscript.py:** Backend script that converts audio to .mp3 and transcribes using Whisper
- **requirements.txt:** Lists all Python dependencies
- **recordings/:** Directory where processed audio files and transcripts are stored

💡 How Transcription Works

**Processing Steps:**
1. **Audio Conversion:** Your .webm recording is converted to .mp3 format using pydub
2. **Transcription:** The audio is processed by OpenAI's Whisper "base" model, which converts speech to text
3. **Display:** The transcript appears in the browser for you to review and copy

**Model Details:**
- **Whisper Base Model:** Provides a good balance between accuracy and speed (~30-60 seconds per 30-second recording)
- **First Run:** The model is downloaded on first use (~500MB)
- **Supported Languages:** Whisper automatically detects and transcribes multiple languages

⚠️ Troubleshooting

**"Server won't start" or "Port 5000 already in use":**
- Another application is using port 5000
- Option 1: Close other applications
- Option 2: Edit `server.py` and change `port=5000` to a different port (e.g., `port=5001`)

**"Microphone access denied":**
- Your browser is blocking microphone access
- Check browser permissions for localhost
- Try a different browser or clear browser cache

**"Module not found: flask":**
- Run: `pip install -r requirements.txt` to install all dependencies

**"FFmpeg not found":**
- Restart your terminal after installing FFmpeg
- On Windows, close all PowerShell windows and reopen

**Slow first transcription:**
- On first use, the script downloads ~500MB of AI models
- Subsequent transcriptions are much faster
- Be patient—processing a 30-second recording may take 30-60 seconds

**Empty or garbled transcript:**
- Ensure your audio is clear and contains speech
- Speak clearly and at a normal volume
- Try re-recording and transcribing again

📄 License
This project is for audio recording, transcription, and research purposes. Ensure you have the right to record any audio and that you comply with local privacy and recording consent laws.