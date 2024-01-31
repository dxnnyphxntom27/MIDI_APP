import mido

def print_note_on_messages(midi_file_path):
    try:
        midi_file = mido.MidiFile(midi_file_path)

        print("Note-On Messages:")
        for track in midi_file.tracks:
            for message in track:
                if message.type == 'note_on':
                    print("Note:", message.note)
                    print("Velocity:", message.velocity)
                    print("Channel:", message.channel)
                    print("Time:", message.time)
                    print()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # Replace 'your_midi_file.mid' with the path to your MIDI file
    midi_file_path = 'output.mid'
    print_note_on_messages(midi_file_path)