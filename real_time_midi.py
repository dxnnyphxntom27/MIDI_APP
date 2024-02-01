import mido
import time
midi_file_path = 'output.mid'
midi_file = mido.MidiFile(midi_file_path)
start_time = time.time()
for track in midi_file.tracks:
    delta_time = 0
    for message in track:
        if message.type == 'note_on':
            delta_time += message.time
            current_time = time.time() - start_time
            sleep_time = (delta_time - current_time) / 6000
            if sleep_time > 0:  # Only sleep if the time difference is positive
                print("message no.", count)
                time.sleep(sleep_time)
                print("current:", current_time)
                print("delta:", delta_time)
                print("sleep time:", delta_time - current_time)
            print("Time:", current_time)
            print("Message:", message)
            print()
