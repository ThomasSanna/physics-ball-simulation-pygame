import pygame
import pygame.midi
import random
import os
import mido

class MusicMidi():
    nbMusic = 0
    NOTE_DELAY = 0.1  # Délai entre les notes en secondes
    
    def __init__(self, dir=None, volume=0.5):
        self.midiOut = pygame.midi.Output(MusicMidi.nbMusic)
        MusicMidi.nbMusic += 1
        self.midiOut.set_instrument(4)
        
        if dir:
            sounds_dir = os.path.join(os.path.dirname(__file__), "../"+dir)
            self.sound_files = [os.path.join(sounds_dir, f) for f in os.listdir(sounds_dir) if os.path.isfile(os.path.join(sounds_dir, f))]
        
        self.notes = self.chargerRandomFichierMIDI()
        
    
    def chargerRandomFichierMIDI(self):
        random.shuffle(self.sound_files)
        random_sound_file = random.choice(self.sound_files)
        print(f"Fichier choisi : {random_sound_file}")
        midi_file = mido.MidiFile(random_sound_file)
        notes = []
        for track in midi_file.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    notes.append(msg.note)
        self.numNote = 0
        self.lastNoteTime = 0
        return notes    

    def jouerNote(self):
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.lastNoteTime >= MusicMidi.NOTE_DELAY:
            self.midiOut.note_on(self.notes[self.numNote%len(self.notes)], 127)
            self.numNote = (self.numNote + 1) % len(self.notes)
            self.lastNoteTime = current_time
            
            
    