# Program created by Matheus Da Silva for Day 3 of HackAlphaX Coding Olympics
# TITLE: Python That Was Easy Button
# BONUS: Medium Difficulty: Button will move when mouse is approaching it
# Bonus: Impossible Difficulty: Mouse will disappear when hovering over button, and is disabled until mouse
#                                                                               leaves button's collision box

# Importing libraries
import sys
import pygame
from pygame.locals import *
import time
import random
from random import seed

# Initialize pygame module
pygame.init()

# Initialize color values
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
lightred = pygame.Color(233, 116, 82)
red = pygame.Color(139, 0, 1)

# Initialize game screen (600x600)
display = pygame.display.set_mode((600, 600))
display.fill(white)
pygame.display.set_caption("That Was Easy!")

# Initialize screen size helper values
maxX, maxY = pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()
middleX = maxX/2
middleY = maxY/2

# Initialize starting difficulty
currentDifficulty = 1

# Initialize text fonts and display rectangle for author text
# Font Source: https://www.dafont.com/olympus-mount.font
font1 = pygame.font.Font('Olympus Mount.ttf', 16)
authorText = font1.render('AUTHOR: MATHEUS DA SILVA', True, black)
authorRect = authorText.get_rect()
authorRect.bottomleft = (5, pygame.display.get_surface().get_height())

# Initialize game sounds
soundObj = pygame.mixer.Sound('that_was_easy.mp3')

# Set up Easy Button class
class RedEasyButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Image Source: https://www.pinclipart.com/maxpin/ibJhhxo/
        imageSource = pygame.image.load("easybutton.png")
        self.surf = pygame.Surface((150, 150))
        self.image = pygame.transform.scale(imageSource, (150, 150))
        self.rect = self.surf.get_rect(center = (middleX, middleY))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def clicked(self):
        # Check if button was clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Button was clicked so play sound
            # Sound Effect Source: https://www.myinstants.com/instant/that-was-easy/
            soundObj.play()
            time.sleep(1)  # Let sound play for 1 second
            soundObj.stop()
            # Reset button location in particular for Medium difficulty
            self.reset()

    def move(self, velocity):  # Medium difficulty only
        xVelocity, yVelocity = velocity

        # Check if button will hit barrier, if so move it somewhere random, if not just move in same direction as mouse
        if self.rect.right + xVelocity > display.get_rect().right:
            self.randomize()
        elif self.rect.left + xVelocity < display.get_rect().left:
            self.randomize()
        elif self.rect.top + yVelocity < display.get_rect().top:
            self.randomize()
        elif self.rect.bottom + yVelocity > display.get_rect().bottom:
            self.randomize()
        else:
            self.rect.move_ip(velocity)

    def reset(self):
        self.rect.center = (middleX, middleY)

    def randomize(self):
        seed(time.time())
        self.rect.bottomleft = (random.randrange(0, maxX - 150), random.randrange(0 + 150, maxY))
        # Check if point is away from mouse, else randomize again
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.randomize()

# Set up Difficulty Button class
class DifficultyButton(pygame.sprite.Sprite):
    def __init__(self, thisButton):
        super().__init__()
        # Font Source: https://www.1001fonts.com/source-code-pro-font.html
        self.font = pygame.font.Font('SourceCodePro-Regular.ttf', 30)
        self.text = self.font.render(str(3 - thisButton) + ' ', True, black)
        self.rect = self.text.get_rect(bottomright = (maxX-5*thisButton-self.text.get_width()*thisButton, maxY))

    def clicked(self, thisButton, RedEasyButton):
        # Check if button was clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Button was clicked so change difficulty if need be
            global currentDifficulty
            # Only change and reset if necessary
            if 3 - thisButton != currentDifficulty:
                currentDifficulty = 3 - thisButton
                # Reset position of red 'Easy' button
                RedEasyButton.reset()

    def show(self, surface):
        surface.blit(self.text, self.rect)

# Setting program tick speed
FPS = pygame.time.Clock()

# Initialize red 'Easy' button
RedEasyButton = RedEasyButton()

# Initialize difficulty buttons
hardButton = DifficultyButton(0)
mediumButton = DifficultyButton(1)
easyButton = DifficultyButton(2)

# Infinite game loop
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:  # Mouse pressed
            # Only allow game completion when mouse is visible
            if pygame.mouse.get_visible():
                RedEasyButton.clicked()
            hardButton.clicked(0, RedEasyButton)
            mediumButton.clicked(1, RedEasyButton)
            easyButton.clicked(2, RedEasyButton)

    FPS.tick(60)  # 60 frames per second

    # Update background color depending on difficulty
    if currentDifficulty == 1:
        display.fill(white)
    elif currentDifficulty == 2:
        display.fill(lightred)
    elif currentDifficulty == 3:
        display.fill(red)

    mouseVelocity = pygame.mouse.get_rel()

    # Check if mouse if hovering over easy button collision box
    if RedEasyButton.rect.collidepoint(pygame.mouse.get_pos()):
        if currentDifficulty == 2:  # Medium difficulty - move button away from mouse
            RedEasyButton.move(mouseVelocity)
        elif currentDifficulty == 3:  # Hard difficulty - make mouse disappear
            pygame.mouse.set_visible(False)
    # Check if player is no longer hovering over button and that mouse is invisible
    if not RedEasyButton.rect.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_visible():
        # Make mouse visible again
        pygame.mouse.set_visible(True)

    # Draw author line
    display.blit(authorText, authorRect)

    # Draw red 'Easy' button a difficulty buttons
    RedEasyButton.draw(display)
    easyButton.show(display)
    mediumButton.show(display)
    hardButton.show(display)