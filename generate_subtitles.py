import os
import sys
import argparse
import whisper
from tqdm import tqdm

def generate_subtitles(input_file, output_file=None, language=None, model_type="medium"):
    """
    Generates subtitles for a video using Whisper.
    
    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to save the output .srt file. If None, saves in the same directory as input_file.
        language (str): Language of the audio. If None, Whisper will auto-detect.
        model_type (str): Whisper model to use (tiny, base, small, medium, large).
    """
    # Check if input file exists
    if not os.path.isfile(input_file):
        print(f"Error: File {input_file} does not exist.")
        sys.exit(1)

    # Load the Whisper model
    print(f"Loading Whisper model '{model_type}'...")
    model = whisper.load_model(model_type)

    # Transcribe the video
    print("Transcribing audio...")
    result = model.transcribe(input_file, language=language)

    # Determine the output file path
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.srt"

    # Write the SRT file
    print(f"Saving subtitles to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(tqdm(result["segments"], desc="Writing subtitles")):
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            f.write(f"{i + 1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{segment['text']}\n\n")

    print(f"Subtitles generated successfully: {output_file}")

def format_time(seconds):
    """
    Formats time in seconds to SRT timestamp format.
    """
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def main():
    parser = argparse.ArgumentParser(description="Generate subtitles for videos using Whisper.")
    parser.add_argument("-i", "--input_file", help="Path to the input video file.")
    parser.add_argument("-o", "--output_file", help="Path to save the output .srt file.", default=None)
    parser.add_argument("-l", "--language", help="Language of the audio (e.g., 'en', 'zh'). Auto-detect if not specified.", default=None)
    parser.add_argument("-m", "--model", help="Whisper model to use (tiny, base, small, medium, large). Default is 'base'.", default="small")

    args = parser.parse_args()
    generate_subtitles(args.input_file, args.output_file, args.language, args.model)

if __name__ == "__main__":
    main()