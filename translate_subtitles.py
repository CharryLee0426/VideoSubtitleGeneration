import argparse
from googletrans import Translator


def parse_srt(file_path):
    """
    Parses the .srt file into a list of subtitle entries.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    entries = []
    current_entry = {"id": None, "timestamp": None, "text": []}
    for line in content.splitlines():
        if line.strip().isdigit():
            if current_entry["id"]:
                entries.append(current_entry)
                current_entry = {"id": None, "timestamp": None, "text": []}
            current_entry["id"] = line.strip()
        elif "-->" in line:
            current_entry["timestamp"] = line.strip()
        elif line.strip():
            current_entry["text"].append(line.strip())
        elif current_entry["id"]:
            entries.append(current_entry)
            current_entry = {"id": None, "timestamp": None, "text": []}

    if current_entry["id"]:
        entries.append(current_entry)

    return entries


def translate_subtitles(entries, target_language):
    """
    Translates the subtitle entries to the target language.
    """
    translator = Translator()
    for entry in entries:
        text = "\n".join(entry["text"])
        translated = translator.translate(text, dest=target_language).text
        entry["translated_text"] = translated
    return entries


def write_srt(entries, output_path):
    """
    Writes the translated subtitle entries back to an .srt file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        for entry in entries:
            file.write(f"{entry['id']}\n")
            file.write(f"{entry['timestamp']}\n")
            file.write(f"{entry['translated_text']}\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Translate .srt subtitle files to another language."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to the input .srt file.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the translated .srt file.")
    parser.add_argument(
        "-l", "--language", required=True, help="Target language code (e.g., 'en' for English, 'zh-cn' for Simplified Chinese)."
    )

    args = parser.parse_args()

    # Parse the input .srt file
    print("Parsing .srt file...")
    entries = parse_srt(args.input)

    # Translate the subtitles
    print(f"Translating subtitles to '{args.language}'...")
    translated_entries = translate_subtitles(entries, args.language)

    # Write the translated subtitles to the output file
    print(f"Writing translated subtitles to '{args.output}'...")
    write_srt(translated_entries, args.output)

    print("Translation completed successfully!")


if __name__ == "__main__":
    main()