# Video Subtitles Generator

## 1. Introduction
Video subtitles generaotor is a tiny project that helps me to generate video subtitles quickly and get bilingual subtitles without doing too many work. 
The project is based on OpenAI's whisper and Anthropic's Claude for getting the subtitle and translating it to the target language. Here is one example.

<video width="600" controls>
  <source src="./assets/football.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

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
    Or simply,
    ```
    pip install -r requirements.txt
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

    For each command, you can use `--help` or `-h` to get more information.
6. Insert the subtitles into the video (Optional)
    It's recommended to use `ffmpeg` to do it, just run this command
    ```
    ffmpeg -i <original_video_path> -vf subtitles=<srt_file_path> -c:a aac -b:a 192k <output_file_path>
    ```

## 4. Limitations
- The project is based on OpenAI's whisper, which is a large model. It may take a long time to generate subtitles for a long video.
- LLM can't make sure 100% accuracy. Based on my experiements, OpenAI's gpt-4o is not good at this task.
- Claude's performance is limited. The main problem is that its max token is too small (8,192 tokens maximum). One possible way is to change this model to Google's Gemini 1.5 or 2.0, which are very good for API invokation.

## 5. Future Improvements

1. The performance on long videos (standard or longer movies);