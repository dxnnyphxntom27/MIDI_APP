import pygame
import pygame.midi

def main():
    pygame.init()
    pygame.midi.init()

    input_device_id = 1
    midi_input = pygame.midi.Input(input_device_id)

    print("MIDI Input Device Name:", pygame.midi.get_device_info(input_device_id))

    try:
        while True:
            if midi_input.poll():
                midi_events = midi_input.read(10)
                for midi_event in midi_events:
                    status_byte = midi_event[0][0] & 0xF0
                    if status_byte in [0x90, 0x80]:
                        print("MIDI Event:", midi_event)

    except KeyboardInterrupt:
        pass

    finally:
        midi_input.close()
        pygame.midi.quit()
        pygame.quit()

if __name__ == "__main__":
    main()