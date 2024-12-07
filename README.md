# Video Subtitles Generator

## 1. Introduction
Video subtitles generaotor is a tiny project that helps me to generate video subtitles quickly and get bilingual subtitles without doing too many work. The project is based on OpenAI's whisper and Google Translate for getting the subtitle and translating it to the target language.

## 2. Requirements
- Python 3.8 or higher;
- ffmpeg;
- GPU recommendation;

## 3. Installation & Usage
1. Install all dependencies, commands may be different based on your operating system.
    ```
    pip install openai-whisper
    sudo apt install ffmpeg
    pip install googletrans==4.0.0-rc1
    ```
2. Clone the repository and enter to the project directory.
3. Create such folder in order to hold video files and subtitles files
    ```
    ./data
    ├── videos
    └── subtitles
    ```
4. Put your video files to the `./data/videos` folder.
5. Run the script
    * For getting the original subtitles:
    ```
    python generate_subtitles.py -i ./data/videos/test.mp4 -o ./data/videos/test.srt
    ```
    * For getting the bilingual subtitles:
    ```
    python translate_subtitles.py -i ./data/subtitles/test.srt -o ./data/subtitles/zh-cn.srt -l zh-cn
    ```
    These arguments can be changed based on the requirements.

## 4. Limitations
- The project is based on OpenAI's whisper, which is a large model. It may take a long time to generate subtitles for a long video.
- The project is based on Google Translate, which may not be accurate for some words.
- The subtitles segmentation is not so perfect and the translator can't consider the relationship between neighbor segments, which may cause some mistakes.
