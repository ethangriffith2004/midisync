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

I have always had an interest in YTPMV and otoMAD videos, which are a genre of online content where sampled video clips are sequenced and synchronized to create a song, often a cover of an existing piece. I enjoy making these myself from time to time, but one thing that had been holding me back was the video editing process. I found manually syncing video clips to notes to be extremely time-consuming and error-prone.

For me, the typical workflow involved:
1. Creating a MIDI file in a digital audio workstation (e.g. Logic Pro) and exporting the audio
2. Placing video clips corresponding to each note on a timeline in video editing software (e.g. Final Cut Pro)
3. Adjusting clip length for each note
4. Adding visual effects and keying

I wanted to automate what I found to be the most tedious parts: the initial sync of video clips to note timings and the clip duration adjustments.

## Project Overview

In this project, I created a tool that takes a MIDI file and a video clip, then produces a video with the clip synchronized to each note in the MIDI file. Silences between notes are filled with chroma key green for easy removal, and for even-numbered notes, the clip is horizontally flipped for more visual interest. Clips are also cut short or "bounced" back and forth to fit exactly to the note length.

The Python script can be executed on any system, but I also created an app for macOS that provides a user-friendly GUI for selecting files.

## Technologies Used
- Python 3.x (core script logic)
- mido (MIDI file parsing)
- moviepy (video processing and manipulation)
- numpy (array operations for video transformations)
- AppleScript (macOS GUI wrapper)

## Results

This tool has dramatically improved my workflow. The automated process is more accurate (frame-perfect timing), faster (seconds vs. hours), and consistent (no human timing errors). The created videos are ready for immediate import into video editing software, where I can focus on cropping, effects, and other creative decisions instead of basic timing.

## Takeaways

This project:
- Introduced me to video processing and frame manipulation with Python
- Taught me how to parse and work with MIDI data
- Showed me how to create seamless Python-AppleScript integrations
- Reinforced the value of automating repetitive tasks

## Improvements & Extensions
- Add export option to include the MIDI playback to ensure proper clip placement.
- Add support for images.
- Create a GUI app for Windows/Linux.
- Options presented all at once instead of in sequential dialog boxes.

## Download & Setup

### Prerequisites
- macOS (for GUI usage) or any OS (for command-line usage)
- [Python 3.7+](https://www.python.org/downloads/)
- `mido`, `moviepy`, `numpy`

### How to Run

#### GUI app (macOS only):
1. Download the `.zip` archive: [`MIDISync.zip`](MIDISync.zip).
2. Extract the archive and (optionally) move the app to your Applications folder.
3. Run the app and follow the dialogue boxes.

#### Command-line interface (any OS):
1. Clone this repository or download the Python file directly: [`midisync.py`](midisync.py).
2. Install the required packages:

```bash
pip install mido moviepy numpy
```

3. Go to the directory containing the script.
4. Run the script:

```bash
python3 midisync.py <midi_file> <video_clip> <output_video>
```

Parameters:
- midi_file: Path to your MIDI file (.mid)
- video_clip: Path to your source video clip (.mp4, .mov, etc.)
- output_video: Path for the completed output video (.mp4, .mov, etc.)

### Tips

#### Using images as the visual element
If you want to synchronize an image to your MIDI file rather than a video clip, you can convert the image to a still-frame video first. I would recommend setting the duration to 1 second for best results.

## Troubleshooting

### Missing or skipped notes

- If the output video is missing notes and appears to be severely shorter than expected, make sure that the MIDI file you are using begins at measure 1 of your project in your DAW.
- If certain notes still do not appear in the output video, the issue may be due to corrupted data; some notes may have zero-duration timestamps even though they display and play normally in your DAW. The solution is to locate the problematic notes, delete them, and re-enter them.

## Contributing

- Fork the repo and submit a pull request with any improvements.
- Suggestions or bug reports welcome via email or GitHub issues.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this code, provided you include proper credit and retain the license notice.

> © 2025 Ethan Griffith
