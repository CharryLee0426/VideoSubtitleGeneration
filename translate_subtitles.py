import argparse
import anthropic
import os
import sys
import time
from dotenv import load_dotenv

# Dictionary mapping language codes to their natural language names
LANGUAGE_MAP = {
    'en-US': 'English (United States)',
    'en-GB': 'English (United Kingdom)',
    'en-AU': 'English (Australia)',
    'en-CA': 'English (Canada)',
    'fr-FR': 'French (France)',
    'es-ES': 'Spanish (Spain)',
    'es-MX': 'Spanish (Mexico)',
    'ja-JP': 'Japanese',
    'ko-KR': 'Korean',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'zh-HK': 'Chinese (Hong Kong)',
    # Add more language codes and their corresponding names as needed
}


def read_srt(file_path):
    """
    Reads the entire .srt file content as a string.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def translate_with_claude(srt_content, api_key, lang_code: str, model="claude-3-5-sonnet-20241022"):
    """
    Translates the entire .srt file content using the Claude API.
    """
    client = anthropic.Anthropic(api_key=api_key)
    
    # Display a timer while waiting for the response
    print("Sending translation request to Claude...")
    start_time = time.time()
    
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0,
        system=(
            f"You are a proficient subtitle translator tasked with converting .srt files into {LANGUAGE_MAP.get(lang_code)}.\n\n"
            "Given that Whisper may segment sentences based on pauses, resulting in single sentences being split "
            "across multiple segments, it's crucial to maintain the original segment structure. Translate each segment "
            "individually, but you need to look at the context when translating, ensuring that the translation aligns "
            "with the context and content of each segment. Make sure the translation has absolutely same segments as "
            "the original segments, for both segment quantity and segment start/end timestamp. That is, the translation "
            "must have 113 segments if the original has 113 segments. You have to make sure that the last segment's end "
            "timestamp is the original srt's last segment's end timestamp.\n\n"
            "If a complete sentence spans multiple segments, translate each segment's content separately to preserve "
            "the segment numbering and timing. Ensure that the translated text fits within the original time constraints "
            "of each segment.\n\n"
            "Just give the full translation in one response without any additional introduction."
        ),
        messages=[
            {"role": "user", "content": srt_content}
        ]
    )
    
    # Update the timer while waiting
    while response is None:
        elapsed_time = time.time() - start_time
        sys.stdout.write(f"\rWaiting for translation response... {int(elapsed_time)}s")
        sys.stdout.flush()
        time.sleep(1)
    
    elapsed_time = time.time() - start_time
    sys.stdout.write(f"\rTranslation completed in {int(elapsed_time)} seconds.\n")
    sys.stdout.flush()

    return response.content[0].text

def write_srt(content, output_path):
    """
    Writes the translated .srt content to an output file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: Claude API key not found in .env file. Please set ANTHROPIC_API_KEY.")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Translate .srt subtitle files to another language using Claude API."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input .srt file.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the translated .srt file.")
    parser.add_argument(
        "-m", "--model", default="claude-3-5-sonnet-20241022", help="Claude model to use. Default is 'claude-3-5-sonnet-20241022'."
    )
    parser.add_argument(
        '-l', '--language',
        choices=LANGUAGE_MAP.keys(),
        help="Specify the language code. Available options: " +
             ', '.join(f"{code} ({name})" for code, name in LANGUAGE_MAP.items())
    )

    args = parser.parse_args()

    # Check if the input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    # Read the .srt file
    print("Reading .srt file...")
    srt_content = read_srt(args.input)

    lang_code = args.language

    # Translate the content
    print("Translating subtitles...")
    translated_content = translate_with_claude(srt_content, api_key, lang_code, args.model)

    # Write the translated content to the output file
    print(f"Writing translated subtitles to '{args.output}'...")
    write_srt(translated_content, args.output)

    print("Translation completed successfully!")

if __name__ == "__main__":
    main()