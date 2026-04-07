from pydub import AudioSegment
import os
import sys
from transformers import pipeline, AutoTokenizer

# Global model - loaded once
detector_model = None

def load_ai_detector():
    """Load the AI detector model once at startup."""
    global detector_model
    if detector_model is None:
        print("Loading AI detection model (roberta-base-openai-detector)...")
        detector_model = pipeline("text-classification", model="roberta-base-openai-detector")
        print("✓ Model loaded successfully\n")
    return detector_model

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



def local_ai_detector(text, detector):
    """
    Uses a locally hosted RoBERTa-based model to detect AI text.
    Splits text into 510-token chunks and analyzes each independently.
    Takes the pre-loaded detector model as a parameter.
    
    Args:
        text: The transcript to analyze
        detector: Pre-loaded pipeline object
    
    Returns:
        list of dicts with 'label' and 'score' keys for each chunk
    """
    print("--- Running Local AI Detection ---")
    
    if not text or not text.strip():
        raise ValueError("Empty text cannot be analyzed")
    
    try:
        # Load tokenizer for RoBERTa
        tokenizer = AutoTokenizer.from_pretrained("roberta-base-openai-detector")
        
        # Tokenize the entire text
        tokens = tokenizer.encode(text, add_special_tokens=False)
        chunk_size = 510
        
        # Create overlapping chunks
        chunks = []
        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i:i + chunk_size]
            # Decode tokens back to text
            chunk_text = tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        print(f"Analyzing {len(chunks)} chunk(s) ({len(tokens)} total tokens)...")
        
        # Process each chunk through the detector
        all_results = []
        for idx, chunk in enumerate(chunks, 1):
            if chunk.strip():
                chunk_result = detector(chunk)
                all_results.extend(chunk_result)
                print(f"  Chunk {idx}: {chunk_result[0]['label']} ({chunk_result[0]['score']:.2%})")
        
        return all_results
    except Exception as e:
        raise RuntimeError(f"AI detection failed: {e}")

def run_pipeline(input_file):
    """
    Orchestrates the full pipeline: audio conversion -> transcription -> AI detection.
    """
    try:
        # Load the detector model once
        detector = load_ai_detector()
        
        # Step 1: Conversion
        print()
        processed_audio = prepare_audio(input_file)
        
        # Step 2: Transcription
        print()
        transcript = get_transcript(processed_audio)
        if len(transcript) > 200:
            print(f"\nTranscript Preview: {transcript[:100]}...\n")
        else:
            print(f"\nTranscript: {transcript}\n")

        
        
        # Step 3: AI Detection
        print()
        results = local_ai_detector(transcript, detector)
        
        # Step 4: Final Report
        print("--- Final Report ---")
        
        # Aggregate results across all chunks
        total_chunks = len(results)
        fake_chunks = sum(1 for r in results if r.get('label') == 'Fake')
        real_chunks = sum(1 for r in results if r.get('label') == 'Real')
        avg_score = sum(r.get('score', 0) for r in results) / total_chunks if results else 0
        
        print(f"Chunks analyzed: {total_chunks}")
        print(f"  AI-Generated: {fake_chunks}")
        print(f"  Human-Written: {real_chunks}")
        print(f"Average confidence: {avg_score:.2%}")
        
        # Determine overall verdict
        if fake_chunks > real_chunks:
            print(f"\n⚠️  Content appears to be AI-Generated (majority of chunks)")
        elif real_chunks > fake_chunks:
            print(f"\n✓ Content appears to be Human-Written (majority of chunks)")
        else:
            print(f"\n❓ Mixed results - content contains both AI and human-written sections")
        
        # Cleanup processed file
        if os.path.exists(processed_audio):
            os.remove(processed_audio)
            print(f"\n✓ Cleaned up temporary file: {processed_audio}")
        
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