# MIDISync

A Python utility that synchronizes a video clip to MIDI note timings. Personal project.

## Table of Contents
- [Background](#background)
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Results](#results)
- [Takeaways](#takeaways)
- [Improvements & Extensions](#improvements--extensions)
- [Download & Setup](#download--setup)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Background

My love of watching [YouTube Poop](https://en.wikipedia.org/wiki/YouTube_poop) (YTP) edits of my favorite TV shows growing up naturally led to my discovery of YouTube Poop Music Videos (YTPMVs), a subgenre where clips sampled from other media are used to create a song (often a cover). I now enjoy making these myself from time to time, but one thing that had been holding me back was the video editing process. I found manually syncing video clips to notes frame-by-frame to be extremely time-consuming.

For me, the typical workflow involved:
1. Creating a MIDI composition in a digital audio workstation (e.g. Logic Pro), and exporting the audio
2. Placing video clips corresponding to each note on a timeline in video editing software (e.g. Final Cut Pro)
3. Adjusting clip length for each note
4. Adding visual effects and keying

I wanted to automate what I found to be the most tedious parts, which were the initial sync of video clips to note timings, and the clip length adjustments.

## Project Overview

In this project, I created a tool that takes a MIDI file and a video clip, then produces a video with the clip synchronized to each note in the MIDI file. Silences between notes are filled with chroma key green for easy removal, and for even-numbered notes, the clip is horizontally flipped for more visual interest. Short clips are also cut or "bounced" back and forth to fit exactly to the note length.

The Python script can be executed on any system. I also created a macOS app that provides a user-friendly dialog interface for selecting files.

## Technologies Used
- Python 3.x (Core script logic)
- mido (MIDI file parsing)
- moviepy (Video processing and manipulation)
- numpy (Array operations for video transformations)
- AppleScript (macOS GUI wrapper)

## Results

This tool has dramatically improved my workflow. The automated process is more accurate (frame-perfect timing), faster (seconds vs. hours), and consistent (no human timing errors). The created videos are ready for immediate import into video editing software, where I can focus on cropping, effects, and other creative decisions rather than focusing on timing.

## Takeaways

This project:
- Taught me how to parse and work with MIDI data
- Introduced me to video processing and frame manipulation with Python
- Showed me how to create seamless Python-AppleScript integrations
- Reinforced the value of automating repetitive tasks

## Improvements & Extensions
- Add audio export option to include the MIDI playback.
- Add support for images as well as videos.
- Create a GUI app for Windows or Linux users.
- Options presented all at once instead of in sequential dialog boxes.

## Download & Setup

### Prerequisites
- macOS (for the GUI app) or any OS (for command-line usage)
- [Python 3.7+](https://www.python.org/downloads/)
- `mido`, `moviepy`, `numpy`

### How to Run

#### GUI app (macOS only):
1. Download the `.zip` archive: [`MIDISync.zip`](MIDISync.zip).
2. Extract the archive and move the app to your Applications folder (optional but recommended).
3. Run the app.

> [!NOTE]
> The app will use your system's Python installation. If you encounter errors, verify Python is installed by running `which python3` in Terminal.

#### Command-line interface (any OS):
1. Clone this repository or download the Python file directly: [`midisync.py`](midisync.py).
5. Install the required packages:

```bash
pip install mido moviepy numpy
```

3. Run the script:

```bash
python3 midisync.py <midi_file> <video_clip> <output_video>
```

Parameters:
- midi_file: Path to your MIDI file (.mid)
- video_clip: Path to your source video clip (.mp4, .mov, etc.)
- output_video: Path for the completed output video (.mp4, .mov, etc.)

### Usage

#### GUI app
Run the app and follow the dialogs to:
- Select your MIDI file
- Select your video clip
- Choose where to save the output

#### Command line
```bash
python3 /path/to/midisync.py /path/to/input.mid /path/to/video.mp4 /path/to/output.mp4
```

## Troubleshooting

### Missing or skipped notes
If certain notes do not appear in the output video, the issue is likely corrupted data in the MIDI file. Some notes may have zero-duration timestamps even though they display and play normally in your DAW.
** Solution:** Open the MIDI file in your DAW (e.g., Logic Pro), locate the problematic notes, delete them, and re-enter them manually. Adding slight spacing between notes can also help prevent timing conflicts.

## Contributing

- Fork the repo and submit a pull request with any improvements.
- Suggestions or bug reports welcome via email or GitHub issues.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this code, provided you include proper credit and retain the license notice.

> © 2025 Ethan Griffith
