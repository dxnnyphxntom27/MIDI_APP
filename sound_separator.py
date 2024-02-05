from pydub import AudioSegment

full_audio = AudioSegment.from_wav("piano.wav")
notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

start_octave = 0
end_octave = 7

segment_duration = 2000

current_time = 0
note_index = 0

for octave in range(start_octave, end_octave + 1):
    for note in notes:
        note_name = f"{note}{octave}"
        segment = full_audio[current_time:current_time + segment_duration]
        segment.export(f"{note_name}.wav", format="wav")
        current_time += segment_duration
        note_index += 1