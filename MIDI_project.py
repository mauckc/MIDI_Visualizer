import mido
import pygame
# Get key commands for input
from pygame.locals import *
# sys module for terminating process
# Should replace end game with something like pygame.endgame or something
import sys
pathToMidi = "./Fukashigi_no_Carte_Shinkai_Ver..mid"
# from note_object import NoteObj

class NoteObj():
    # this file holds the note class
    def __init__(self, type, time, channel, note, velocity):
        self.height = 30
        self.width = 20
        self.x = note * 20
        self.y = 0
        self.change_x = 0
        self.change_y = 5
        self.color = (0,0,128)
        self.thickness = 1
    def move(self):
        self.x += self.change_x
        self.y += self.change_y
    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.thickness)

pygame.init()
pygame.display.set_caption('MIDI Project')
surface_dims = (1760, 990)
surface = pygame.display.set_mode(surface_dims)
background = (128,0,0)
FPS = 30

clock = pygame.time.Clock()

notes = []
mid = mido.MidiFile(pathToMidi)

# parse MIDI file and spawn notes in actual time
# for msg in mid.play(meta_messages=True): changed
for msg in mid:
    if msg.type == 'note_on':
        attrs = vars(msg)
        #print(attrs)
        print(" ".join(('note_on::',str(attrs),"\nappending...")))
        notes.append(NoteObj(msg.type, msg.time, msg.channel, msg.note, msg.velocity))
    elif msg.type == 'note_off':
        attrs = vars(msg)
        print(" ".join(('note::',str(attrs))))
    elif msg.is_meta == False:
        pass
    else:
        print(msg.type)
        print(" ".join(('else::',str(msg))))

file_num = 0
# draw
while True:
    # Draw the background
    surface.fill(background)
    for i in notes:
        i.move()
        i.draw()

    # # Save every frame
    # filename = "Snaps/%04d.png" % file_num
    # pygame.image.save(surface, filename)

    # Process Events
    for e in pygame.event.get():
        if e.type == KEYUP: # On User Key Press Up
            if e.key == K_ESCAPE:# End Game
                sys.exit()

    file_num = file_num + 1
    pygame.display.flip()
    clock.tick(FPS)
