(*
Copyright (c) 2025 Ethan Griffith
Licensed under the MIT License. See LICENSE file for details.
*)

-- provides a gui for selecting files and running the python script midisync.py

-- set python interpreter path
set pythonInterpreter to "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3"

-- python script embedded as text
set pythonCode to "import sys
import mido
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip
import numpy as np

def extractNotes(filePath, chordThreshold=0.1):
    mid = mido.MidiFile(filePath)
    noteEvents = []
    currentTime = 0.0
    activeNotes = {}
    
    for msg in mid:
        currentTime += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            activeNotes[msg.note] = currentTime
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            if msg.note in activeNotes:
                startTime = activeNotes[msg.note]
                endTime = currentTime
                noteEvents.append({'pitch': msg.note, 'start': startTime, 'end': endTime})
                del activeNotes[msg.note]
    
    noteEvents.sort(key=lambda x: x['start'])
    noteNum = 0
    lastStartTime = None
    groupedEvents = []
    
    for event in noteEvents:
        if lastStartTime is None or (event['start'] - lastStartTime) > chordThreshold:
            noteNum += 1
            lastStartTime = event['start']
            groupedEvents.append({'noteNum': noteNum, 'start': event['start'], 'end': event['end']})
    
    return groupedEvents

def createVideo(midiPath, videoClipPath, outputPath):
    noteEvents = extractNotes(midiPath, chordThreshold=0.1)
    if not noteEvents:
        return
    
    sourceClip = VideoFileClip(videoClipPath)
    videoClips = []
    currentPos = 0.0
    
    for event in noteEvents:
        noteNum = event['noteNum']
        startTime = event['start']
        endTime = event['end']
        duration = endTime - startTime
        
        if startTime > currentPos:
            gapDuration = startTime - currentPos
            greenClip = ColorClip(size=(sourceClip.w, sourceClip.h), color=(0, 255, 0), duration=gapDuration)
            videoClips.append(greenClip)
        
        if sourceClip.duration < duration:
            clips = []
            remainingDuration = duration
            forward = True
            
            while remainingDuration > 0:
                if forward:
                    clipToAdd = sourceClip
                else:
                    clipToAdd = sourceClip.fl_time(lambda t: sourceClip.duration - t, apply_to=['video', 'audio'])
                
                if remainingDuration >= sourceClip.duration:
                    clips.append(clipToAdd)
                    remainingDuration -= sourceClip.duration
                else:
                    clips.append(clipToAdd.subclip(0, remainingDuration))
                    remainingDuration = 0
                
                forward = not forward
            
            noteClip = concatenate_videoclips(clips)
        else:
            noteClip = sourceClip.subclip(0, duration)
        
        if noteNum % 2 == 0:
            noteClip = noteClip.fx(lambda clip: clip.fl_image(lambda img: np.fliplr(img)))
        
        videoClips.append(noteClip)
        currentPos = endTime
    
    finalVideo = concatenate_videoclips(videoClips, method='compose')
    finalVideo.write_videofile(outputPath, fps=30, codec='libx264', audio=False)
    sourceClip.close()
    finalVideo.close()

if __name__ == '__main__':
    if len(sys.argv) == 4:
        midiFile = sys.argv[1]
        videoClip = sys.argv[2]
        outputVideo = sys.argv[3]
    else:
        sys.exit(1)
    createVideo(midiFile, videoClip, outputVideo)
"

try
	-- select MIDI file
	set midiFile to choose file with prompt "Select the MIDI file:" of type {"mid", "midi", "public.midi-audio"}
	set midiPath to POSIX path of midiFile
	
	-- select video clip file
	set videoFile to choose file with prompt "Select the video clip:" of type {"mov", "mp4", "avi", "public.movie", "public.mpeg-4"}
	set videoPath to POSIX path of videoFile
	
	-- choose output location and name
	set outputFile to choose file name with prompt "Save output video as:" default name "output.mp4"
	set outputPath to POSIX path of outputFile
	
	set msgString to "Processing video..." & return & "You will be notified when it is completed."
	display notification msgString with title "MIDISync"
	
	-- create temporary python script file
	set tempScript to (POSIX path of (path to temporary items)) & "midisync_temp.py"
	
	-- write python code to file using cat with heredoc to avoid quote issues
	do shell script "cat > " & quoted form of tempScript & " << 'ENDOFPYTHON'
" & pythonCode & "
ENDOFPYTHON"
	
	-- build and execute python command
	set pythonCommand to pythonInterpreter & " " & quoted form of tempScript & " " & quoted form of midiPath & " " & quoted form of videoPath & " " & quoted form of outputPath
	
	-- run the script
	set scriptOutput to do shell script pythonCommand
	
	-- clean up temp file
	do shell script "rm " & quoted form of tempScript
	
	-- show completion message
	display dialog "Video created successfully!" & return & return & "Output: " & outputPath buttons {"OK"} default button 1 with icon note with title "MIDISync"
	
	-- reveal in finder, delay to ensure file is registered
	delay 0.5
	try
		tell application "Finder"
			reveal POSIX file outputPath
			activate
		end tell
	on error
		-- if reveal fails, open the containing folder
		do shell script "open " & quoted form of (do shell script "dirname " & quoted form of outputPath)
	end try
	
on error errMsg number errNum
	if errNum is not -128 then
		display dialog "Error: " & errMsg buttons {"OK"} default button 1 with icon stop
	end if
end try
