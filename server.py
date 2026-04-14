from flask import Flask, render_template, request, jsonify
import subprocess
import os
import sys
from pathlib import Path

app = Flask(__name__)

# Get the current directory
BASE_DIR = Path(__file__).parent
RECORDINGS_DIR = BASE_DIR / 'recordings'
RECORDINGS_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    """Serve the recorder.html file"""
    return render_template('recorder.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Receives an audio file, saves it, and runs the transcription pipeline.
    Expects: 'audio' file in the request
    Returns: JSON with transcript or error message
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Save the audio file
        filename = audio_file.filename
        filepath = RECORDINGS_DIR / filename
        audio_file.save(str(filepath))
        
        # Run the AudioConversionToTranscript.py script
        script_path = BASE_DIR / 'AudioConversionToTranscript.py'
        result = subprocess.run(
            [sys.executable, str(script_path), str(filepath)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or "Unknown transcription error"
            return jsonify({'error': f'Transcription failed: {error_msg}'}), 500
        
        # Extract the transcript from the output
        output = result.stdout
        # The script prints "Final Transcript: <text>" at the end
        lines = output.split('\n')
        transcript = None
        for line in lines:
            if line.startswith('Final Transcript:'):
                transcript = line.replace('Final Transcript:', '').strip()
                break
        
        if transcript is None:
            # Fallback: try to get the last non-empty line
            transcript = next((line for line in reversed(lines) if line.strip()), '')
        
        return jsonify({'transcript': transcript}), 200
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Transcription timed out (took too long)'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
