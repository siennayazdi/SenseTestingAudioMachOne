from pydub import AudioSegment
import os
import sys
from transformers import pipeline, AutoTokenizer

def prepare_audio(file_path):
    """
    Converts .webm, .mp4, or other formats to .mp3.
    Returns the path to the converted file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    file_name, ext = os.path.splitext(file_path)
    output_path = f"{file_name}_processed.mp3"
    
    print(f"--- Converting {ext} to mp3 ---")
    
    try:
        # Load the audio/video file
        # pydub's from_file handles most extensions if ffmpeg is installed
        audio = AudioSegment.from_file(file_path)
        
        # Export as mp3
        audio.export(output_path, format="mp3")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Audio conversion failed: {e}")

import whisper


def get_transcript(audio_path):
    """
    Transcribes the audio file using the Whisper 'base' model.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print("--- Starting Transcription (this may take a minute) ---")
    
    try:
        # Options: 'tiny', 'base', 'small', 'medium', 'large'
        model = whisper.load_model("base") 
        result = model.transcribe(audio_path)
        
        if not result.get('text'):
            raise ValueError("Transcription returned empty text")
        
        return result['text']
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}")

def run_pipeline(input_file):
    """
    Orchestrates the full pipeline: audio conversion -> transcription.
    """
    try:
        
        # Step 1: Conversion
        print()
        processed_audio = prepare_audio(input_file)
        
        # Step 2: Transcription
        print()
        transcript = get_transcript(processed_audio)
        #if len(transcript) > 200:
        #    print(f"\nTranscript Preview: {transcript[:100]}...\n")
        #else:
        #    print(f"\nTranscript: {transcript}\n")


        print(f"Final Transcript: {transcript}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        sys.exit(1)

# Usage
if __name__ == "__main__":
    # Get input file from command-line argument or use default
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "meeting_recording.webm"
        print(f"No input file specified. Using default: {input_file}\n")
    
    run_pipeline(input_file)