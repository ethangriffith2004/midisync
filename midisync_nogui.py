'''
Copyright (c) 2025 Ethan Griffith
Licensed under the MIT License. See LICENSE file for details.
'''

'''
ytpmv helper script.
takes in a MIDI file and a video clip, and creates a video with the clip synced to the notes.
- video clip plays during notes/chords.
- green screen fills the silence between notes.
- every other note is horizontally flipped.
- output video has no audio (add separately in editor).
'''

import sys
import mido
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip
import numpy as np

def extractNotes(filePath, chordThreshold=0.1) :
    '''
    extract note timings from a MIDI file and return as a list.
    notes starting within chordThreshold seconds are grouped with the same number.
    
    args:
        filePath : path to the input MIDI file
        chordThreshold : time window in seconds to group notes as chords (default : 0.1)
    
    returns list of note events with noteNum, startTime, and endTime.
    '''

    # load the MIDI file
    mid = mido.MidiFile(filePath)
    
    # track note events with their timings
    noteEvents = []
    currentTime = 0.0
    
    # dict to track when each note was turned on
    activeNotes = {}
    
    # process all messages in the MIDI file
    for msg in mid :
        currentTime += msg.time
        
        if msg.type == 'note_on' and msg.velocity > 0 :
            activeNotes[msg.note] = currentTime
            
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0) :
            if msg.note in activeNotes :
                startTime = activeNotes[msg.note]
                endTime = currentTime
                noteEvents.append({
                    'pitch' : msg.note,
                    'start' : startTime,
                    'end' : endTime
                })
                del activeNotes[msg.note]
    
    # sort by start time
    noteEvents.sort(key=lambda x : x['start'])
    
    # assign note numbers, grouping chords together
    noteNum = 0
    lastStartTime = None
    groupedEvents = []
    
    for event in noteEvents :
        if lastStartTime is None or (event['start'] - lastStartTime) > chordThreshold :
            noteNum += 1
            lastStartTime = event['start']
            groupedEvents.append({
                'noteNum' : noteNum,
                'start' : event['start'],
                'end' : event['end']
            })
    
    print()
    print(f"MIDI file path : {filePath}")
    print(f"Extracted {len(noteEvents)} notes")
    print(f"Grouped into {noteNum} note/chord events")
    print()
    print("Note #, Start, End")
    
    for event in groupedEvents :
        print(f"{event['noteNum']}, {event['start'] :.3f}, {event['end'] :.3f}")
    
    return groupedEvents

def createVideo(midiPath, videoClipPath, outputPath, chordThreshold=0.1, fps=30) :
    '''
    create a video based on MIDI timings using a source video clip.
    
    args :
        midiPath: Path to the input MIDI file
        videoClipPath: Path to the video clip to use for each note
        outputPath: Path to save the output video
        chordThreshold: Time window in seconds to group notes as chords (default 0.1)
        fps: Frame rate for output video (default 30)
    '''

    # extract note timings
    noteEvents = extractNotes(midiPath, chordThreshold)
    
    if not noteEvents :
        print("No notes found :(")
        return
    
    # load the source video clip
    sourceClip = VideoFileClip(videoClipPath)
    
    # build the complete video timeline
    videoClips = []
    currentPos = 0.0
    
    for event in noteEvents :
        noteNum = event['noteNum']
        startTime = event['start']
        endTime = event['end']
        duration = endTime - startTime
        
        # add gap if there's silence before this note
        if startTime > currentPos :
            gapDuration = startTime - currentPos
            
            # Create a green screen clip (chroma key green: RGB 0, 255, 0)
            greenClip = ColorClip(
                size=(sourceClip.w, sourceClip.h),
                color=(0, 255, 0),
                duration=gapDuration
            )
            videoClips.append(greenClip)
        
        # create clip for this note
        # if clip is too short, loop it
        # if too long, trim it
        if sourceClip.duration < duration :
            numLoops = int(np.ceil(duration / sourceClip.duration))
            loopedClip = concatenate_videoclips([sourceClip] * numLoops)
            noteClip = loopedClip.subclip(0, duration)
        else :
            noteClip = sourceClip.subclip(0, duration)
        
        # flip horizontally for even-numbered notes
        if noteNum % 2 == 0 :
            noteClip = noteClip.fx(lambda clip : clip.fl_image(lambda img : np.fliplr(img)))
        
        videoClips.append(noteClip)
        currentPos = endTime
    
    # concatenate all clips
    print(f"\nCreating synced video with {len(videoClips)} clip segments (clips + silences)")
    finalVideo = concatenate_videoclips(videoClips, method="compose")
    
    # write output video
    print()
    finalVideo.write_videofile(
        outputPath,
        fps=fps,
        codec='libx264',
        audio=False
    )
    
    # clean up
    sourceClip.close()
    finalVideo.close()
    print()
    print("Make sure when you make the visuals:")
    print("- Crop the video to the proper size")
    print("- Key out the greenscreen")
    print()

if __name__ == "__main__" :
    
    # check if command-line arguments are provided
    if len(sys.argv) >= 4 :
        midi_file = sys.argv[1]
        video_clip = sys.argv[2]
        output_video = sys.argv[3]
        fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        chord_threshold = float(sys.argv[5]) if len(sys.argv) > 5 else 0.1
    else :
        print()
        print("Usage: python3 midisync_nogui.py <midi_file> <video_clip> <output_file> [fps] [chord_threshold]")
        print("\nExample:")
        print("  python3 midisync_nogui.py input.mid video.mp4 output.mp4")
        print("  python3 midisync_nogui.py input.mid video.mp4 output.mp4 60 0.05")
        print()
        sys.exit(1)
    
    createVideo(midi_file, video_clip, output_video, chord_threshold, fps)