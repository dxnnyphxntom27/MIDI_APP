import pygame
import notes
from pygame import mixer
import pygame.midi
from midiutil import MIDIFile
import mido
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

pygame.init()
pygame.mixer.set_num_channels(50)

# MIDI Output file
midi_time = 0
track = 0
channel = 0
duration = 1
midi_output_file = MIDIFile(1)
tempo = 120
midi_output_file.addTempo(track, midi_time, tempo)

# MIDI Input file
input_file_path = 'output.mid'
midi_file = mido.MidiFile(input_file_path)
start_time = time.time()

# pygame initialization
font_whites = pygame.font.SysFont(None, 24)
font_blacks = pygame.font.SysFont(None, 15)
fps = 165
timer = pygame.time.Clock()
WHITE_BUTTON_WIDTH = 33
BLACK_BUTTON_WIDTH = WHITE_BUTTON_WIDTH - 12
WIDTH = 36 * WHITE_BUTTON_WIDTH
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('MIDI APP')
white_keys_color = (245, 245, 245)
white_keys_outline = (100, 100, 100)
black_keys_color = (35, 35, 35)
white_keys_text = (40, 40, 40)
black_keys_text = (245, 245, 245)
background_color = (55, 55, 55)
active_black_color = (166, 210, 8)
active_white_color = (216, 250, 8)

# piano variables
white_sounds = []
black_sounds = []
active_whites = []
active_blacks = []

# init functions
pygame.init()
pygame.midi.init()
input_device_id = pygame.midi.get_default_input_id()

# connected/not connected handling
isConnected = False
if input_device_id != -1:
    isConnected = True
    midi_input = pygame.midi.Input(input_device_id)

print("MIDI Input Device Name:", pygame.midi.get_device_info(input_device_id))


# piano drawing function
def draw_piano(whites, blacks):
    white_rects = []
    black_rects = []
    for i in range(36):
        rect = pygame.draw.rect(screen, white_keys_color, [i * WHITE_BUTTON_WIDTH, HEIGHT - 300, WHITE_BUTTON_WIDTH, 300], 0, 3)
        white_rects.append(rect)
        pygame.draw.rect(screen, white_keys_outline, [i * WHITE_BUTTON_WIDTH, HEIGHT - 300, WHITE_BUTTON_WIDTH, 300], 1, 3)

        for j in range(len(whites)):
            if whites[j][0] == i and whites[j][1] > 0:
                pygame.draw.rect(screen, active_white_color, [i * WHITE_BUTTON_WIDTH, HEIGHT - 300, WHITE_BUTTON_WIDTH, 300], 0, 2)
                pygame.draw.rect(screen, white_keys_outline, [i * WHITE_BUTTON_WIDTH, HEIGHT - 300, WHITE_BUTTON_WIDTH, 300], 1, 3)

    # Draw white key labels
    for i in range(36):
        key_label = font_whites.render(notes.white_notes[i], True, white_keys_text)
        screen.blit(key_label, (i * WHITE_BUTTON_WIDTH + 3, HEIGHT - 20))

    skip_count = 0
    last_skip = 2
    skip_track = 2

    for i in range(26):
        if i > 0:
            rect = pygame.draw.rect(screen, black_keys_color, [BLACK_BUTTON_WIDTH + ((i-2) * WHITE_BUTTON_WIDTH) + (skip_count * WHITE_BUTTON_WIDTH), HEIGHT - 300, BLACK_BUTTON_WIDTH + 2, 200], 0, 2)
            for q in range(len(blacks)):
                if blacks[q][0] == (i-1):
                    if blacks[q][1] > 0:
                        pygame.draw.rect(screen, active_black_color, [BLACK_BUTTON_WIDTH + ((i-2) * WHITE_BUTTON_WIDTH) + (skip_count * WHITE_BUTTON_WIDTH), HEIGHT - 300, BLACK_BUTTON_WIDTH + 2, 200], 0, 2)

            key_label = font_blacks.render(notes.black_labels[i], True, black_keys_text)
            screen.blit(key_label, (BLACK_BUTTON_WIDTH + 2 + ((i-2) * WHITE_BUTTON_WIDTH) + (skip_count * WHITE_BUTTON_WIDTH), HEIGHT - 120))
            black_rects.append(rect)
        skip_track += 1

        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    return white_rects, black_rects, whites, blacks


# midi playback function
def play_file():
    for input_track in midi_file.tracks:
        delta_time = 0
        for message in input_track:
            if message.type == 'note_on':
                if message.note in notes.midi_notes:  # ensuring the presence of input
                    if notes.midi_notes[message.note][1] == '#':  # black key detection
                        index = notes.black_labels.index(notes.midi_notes[message.note])  # index
                        black_sounds[index].play(0, 2000)  # playing sound
                    else:  # white key detection
                        index = notes.white_notes.index(notes.midi_notes[message.note])  # index
                        white_sounds[index].play(0, 2000)  # playing sound
                delta_time += message.time
                current_input_time = time.time() - start_time
                sleep_time = (delta_time - current_input_time) / 6000
                if sleep_time > 0:  # Only sleep if the time difference is positive
                    time.sleep(sleep_time)
                    print("current:", current_input_time)
                    print("delta:", delta_time)
                    print("sleep time:", delta_time - current_input_time)
                print("Message:", message)
                print()


# loading instrument .wav files
def instrument_load(name):
    white_sounds.clear()
    black_sounds.clear()
    for i in range(len(notes.white_notes)):
        white_sounds.append(mixer.Sound(
            f'assets\\notes\\{name}\\{notes.white_notes[i]}.wav'))

    for i in range(len(notes.black_notes)):
        black_sounds.append(mixer.Sound(
            f'assets\\notes\\{name}\\{notes.black_notes[i]}.wav'))


# button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 24)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, black_keys_color, self.rect)
        pygame.draw.rect(screen, (15, 15, 15), self.rect, 1)
        text_surface = self.font.render(self.text, True, black_keys_text)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.action is not None and callable(self.action):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.action()


def button_click_action():
    print("Button clicked!")


# timer function
def my_timer(elapsed_seconds):
    minutes = int(elapsed_seconds // 60)
    seconds = int(elapsed_seconds % 60)
    timer_text = f"{minutes:02d}:{seconds:02d}"
    return timer_text


# initializing default values
text = ""
run = True
isRecording = False
instrument = "Classic Piano"
instrument_load("piano")
theme = 1

button_start_rec = Button(20, 75, 120, 40, "Record (Q)", button_click_action)
button_stop_rec = Button(160, 75, 195, 40, "Stop Recording (W)", button_click_action)
button_import = Button(20, 20, 140, 40, "Import MIDI (1)", button_click_action)
button_start_play = Button(175, 20, 75, 40, "Play (2)", button_click_action)
button_stop_play = Button(265, 20, 90, 40, "Theme (3)", button_click_action)
button_recording = Button(20, 130, 335, 40, "", button_click_action)

button_tempo = Button((WIDTH/2)-60, 75, 120, 40, "", button_click_action)
button_minus = Button((WIDTH/2)-105, 80, 30, 30, "-", button_click_action)
button_plus = Button((WIDTH/2)+75, 80, 30, 30, "+", button_click_action)
button_instrument = Button((WIDTH/2)-215, 20, 430, 40, "Instrument  (4):                                       ", button_click_action)


while True:
    while run:
        if isRecording:
            current_time = pygame.time.get_ticks()
            elapsed_time = my_timer((current_time - start_rec_time)//1000)
        timer.tick(fps)
        midi_time += 0.01
        screen.fill(background_color)

        # drawing piano
        white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

        # drawing buttons
        button_start_rec.draw()
        button_stop_rec.draw()
        button_import.draw()
        button_start_play.draw()
        button_stop_play.draw()
        button_instrument.draw()
        button_recording.draw()
        button_tempo.draw()
        button_minus.draw()
        button_plus.draw()

        # drawing logo
        img = pygame.image.load('assets\\logo.png')
        screen.blit(img, (WIDTH-375, 10))

        # drawing recording panel
        if isRecording:
            time_text = font_whites.render(f"Recording:   {elapsed_time:}", True, (255, 100, 100))
            screen.blit(time_text, (112, 142))
        else:
            time_text = font_whites.render('Recording:   00:00', True, black_keys_text)
            screen.blit(time_text, (112, 142))

        # drawing tempo panel
        tempo_text = font_whites.render(f"BPM: {tempo}", True, black_keys_text)
        screen.blit(tempo_text, (560, 87))
        instrument_text = font_whites.render(f"{instrument}", True, black_keys_text)
        screen.blit(instrument_text, (590, 33))

    # MIDI CONTROLS
        if isConnected:
            if midi_input.poll(): #  polling message
                midi_events = midi_input.read(10) # storing polled messages
                for midi_event in midi_events:  # separating to particular message
                    status_byte = midi_event[0][0] & 0xF0
                    if status_byte in [0x90, 0x80]:  # filtering
                        print("MIDI Event:", midi_event)
                        if midi_event[0][2] > 0:  # if velocity of note >0 (pressed)
                            key_start_time = midi_time  # current time
                            if midi_event[0][1] in notes.midi_notes:  # ensuring the presence of input
                                if notes.midi_notes[midi_event[0][1]][1] == '#':  # black key detection
                                    index = notes.black_labels.index(notes.midi_notes[midi_event[0][1]])  # index
                                    black_sounds[index].play(0, 2000)  # playing sound
                                    active_blacks.append([index, 1, key_start_time])  # storing active button (UI, rec)
                                else:  # white key detection
                                    index = notes.white_notes.index(notes.midi_notes[midi_event[0][1]])  # index
                                    white_sounds[index].play(0, 2000)  # playing sound
                                    active_whites.append([index, 1, key_start_time])  # storing active button (UI, rec)

                        elif midi_event[0][2] == 0:  # if velocity of note = 0 or note off(released)
                            key_end_time = midi_time
                            if midi_event[0][1] in notes.midi_notes:
                                released_note = notes.midi_notes[midi_event[0][1]]
                                if released_note[1] == '#':
                                    for i in range(len(active_blacks)):
                                        if active_blacks[i][0] == notes.black_labels.index(released_note):
                                            key_total_time = key_end_time - active_blacks[i][2]
                                            print("total", key_total_time)
                                            print("midi_time", midi_time)
                                            if isRecording:
                                                midi_output_file.addNote(track, channel, midi_event[0][1], active_blacks[i][2], key_total_time, 100)
                                            active_blacks[i][1] = 0
                                            if active_blacks[i][1] == 0:
                                                active_blacks.pop(i)
                                                break
                                else:
                                    for i in range(len(active_whites)):
                                        if active_whites[i][0] == notes.white_notes.index(released_note):
                                            key_total_time = key_end_time - active_whites[i][2]
                                            print("total", key_total_time)
                                            print("midi_time", midi_time)
                                            if isRecording:
                                                midi_output_file.addNote(track, channel, midi_event[0][1], active_whites[i][2], key_total_time, 100)
                                            active_whites[i][1] = 0
                                            if active_whites[i][1] == 0:
                                                active_whites.pop(i)
                                                break

    # MOUSE CONTROLS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mouse Event:", event)
                black_key = False
                for i in range(len(black_keys)):
                    if black_keys[i].collidepoint(event.pos):
                        black_sounds[i].play(0, 2000)
                        black_key = True
                        active_blacks.append([i, 1])
                for i in range(len(white_keys)):
                    if white_keys[i].collidepoint(event.pos) and not black_key:
                        white_sounds[i].play(0, 2000)
                        active_whites.append([i, 1])

            if event.type == pygame.MOUSEBUTTONUP:
                print("Mouse Event:", event)
                for entry in active_blacks:
                    entry[1] = 0
                    active_blacks.remove(entry)
                for entry in active_whites:
                    entry[1] = 0
                    active_whites.remove(entry)

            button_start_rec.handle_event(event)
            button_stop_rec.handle_event(event)
            button_import.handle_event(event)
            button_start_play.handle_event(event)
            button_stop_play.handle_event(event)
            button_instrument.handle_event(event)


    # KEYBOARD CONTROLS
            if event.type == pygame.KEYDOWN:
                print("Keyboard Event:", event)
                if event.key == pygame.K_ESCAPE:  # You can handle special keys if needed
                    pygame.quit()

                key_char = pygame.key.name(event.key).upper()

                # importing MIDI file handle
                if key_char == '1':
                    input_file_path = filedialog.askopenfilename()
                    midi_file = mido.MidiFile(input_file_path)

                # playing MIDI file handle
                if key_char == '2':
                    play_file()

                # change theme handle
                if key_char == '3':
                    if theme == 1:
                        theme = 2
                        white_keys_color = (245, 245, 200)
                        white_keys_outline = (100, 100, 100)
                        black_keys_color = (40, 20, 0)
                        white_keys_text = (40, 40, 0)
                        black_keys_text = (245, 245, 215)
                        background_color = (25, 10, 0)
                        active_black_color = (120, 80, 0)
                        active_white_color = (255, 255, 235)
                    elif theme == 2:
                        theme = 1
                        white_keys_color = (245, 245, 245)
                        white_keys_outline = (100, 100, 100)
                        black_keys_color = (35, 35, 35)
                        white_keys_text = (40, 40, 40)
                        black_keys_text = (245, 245, 245)
                        background_color = (55, 55, 55)
                        active_black_color = (166, 210, 8)
                        active_white_color = (216, 250, 8)

                # stop recording handle
                if key_char == 'W':
                    run = False
                    isRecording = False

                # start recording handle
                if key_char == 'Q':
                    isRecording = True
                    midi_time = 0
                    start_rec_time = pygame.time.get_ticks()

                # change instrument table
                if key_char == '4':
                    if instrument == "Classic Piano":
                        instrument = "Crystal Glockenspiel"
                        instrument_load("crystal")

                    elif instrument == "Crystal Glockenspiel":
                        instrument = "Acoustic Guitar"
                        instrument_load("guitar")

                    elif instrument == "Acoustic Guitar":
                        instrument = "Classic Piano"
                        instrument_load("piano")

                # BPM decrease handle
                if key_char == '=':
                    tempo += 1
                    midi_output_file.addTempo(track, midi_time, tempo)
                    print("plus")

                # BPM increase handle
                if key_char == '-':
                    tempo -= 1
                    midi_output_file.addTempo(track, midi_time, tempo)
                    print("minus")

                # handling left hand keys input
                if key_char in notes.left_octave:
                    if notes.left_octave[key_char][1] == '#':
                        index = notes.black_labels.index(notes.left_octave[key_char])
                        black_sounds[index].play(0, 2000)
                        active_blacks.append([index, 1])
                    else:
                        index = notes.white_notes.index(notes.left_octave[key_char])
                        white_sounds[index].play(0, 2000)
                        active_whites.append([index, 1])

                # handling right hand keys input
                if key_char in notes.right_octave:
                    if notes.right_octave[key_char][1] == '#':
                        index = notes.black_labels.index(notes.right_octave[key_char])
                        black_sounds[index].play(0, 2000)
                        active_blacks.append([index, 1])
                    else:
                        index = notes.white_notes.index(notes.right_octave[key_char])
                        white_sounds[index].play(0, 2000)
                        active_whites.append([index, 1])

            # keyboard key release handle
            elif event.type == pygame.KEYUP:
                print("Keyboard Event:", event)
                key_char = pygame.key.name(event.key).upper()
                if key_char in notes.left_octave:
                    released_note = notes.left_octave[key_char]
                    if released_note[1] == '#':
                        for i in range(len(active_blacks)):
                            if active_blacks[i][0] == notes.black_labels.index(released_note):
                                active_blacks[i][1] = 0
                                if active_blacks[i][1] == 0:
                                    active_blacks.pop(i)
                                    break
                    else:
                        for i in range(len(active_whites)):
                            if active_whites[i][0] == notes.white_notes.index(released_note):
                                active_whites[i][1] = 0
                                if active_whites[i][1] == 0:
                                    active_whites.pop(i)
                                    break

                if key_char in notes.right_octave:
                    released_note = notes.right_octave[key_char]
                    if notes.right_octave[key_char][1] == '#':
                        for i in range(len(active_blacks)):
                            if active_blacks[i][0] == notes.black_labels.index(released_note):
                                active_blacks[i][1] = 0
                                if active_blacks[i][1] == 0:
                                    active_blacks.pop(i)
                                    break
                    else:
                        for i in range(len(active_whites)):
                            if active_whites[i][0] == notes.white_notes.index(released_note):
                                active_whites[i][1] = 0
                                if active_whites[i][1] == 0:
                                    active_whites.pop(i)
                                    break
        pygame.display.flip()
    # saving MIDI file
    with open("output.mid", "wb") as output_file:
        midi_output_file.writeFile(output_file)
    print("File was saved!")
    run = True
