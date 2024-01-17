# Snake game written in Python to exercise oop and python syntax.

import random
import time

import pygame  # Imports pygame module
from pygame.locals import *  # Importing names (attributes) from pygame.locals module to access events and keyboard functionalities

SIZE = 48  # Pixle, or image SIZE of each icon (48 x 48) - Global Variable
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Class to draw, and spawn an apple object
class Apple:
    def __init__(self, parent_surface):
        self.apple = pygame.image.load("resources/apple.png").convert_alpha()
        self.parent_surface = parent_surface
        self.pos_x = 3  # Real apple x position
        self.pos_y = 3  # Real apple y position
        self.x = SIZE * self.pos_x
        # X-Y of apple is a multiple of "SIZE" for snake to be able to move fully across it, "pos" variable used to change apple position when it is eaten
        self.y = SIZE * self.pos_y
    # N.B - self.pos_x/y is the actual x-y co-ordinate of the apple. self.x/y is the co-ordinate when multiplied by SIZE

    def draw(self):
        self.parent_surface.blit(self.apple, (self.x, self.y))

    def respawn(self):  # Takes an argument of the snake's x and y co-ordinates, to insure not to spawn on top of the snake.
          self.pos_y = random.randrange(1, 10)
          self.pos_x = random.randrange(1, 10)
          self.x = self.pos_x * SIZE
          self.y = self.pos_y * SIZE
          self.draw()

class Snake:
    def __init__(self, parent_surface):
        self.snake_head = pygame.image.load("resources/snake_head.png").convert_alpha()  # Pygame method to load any image from directory (convert_alpha allows png transparency)
        self.snake_body = pygame.image.load("resources/snake_body.png").convert_alpha()
        self.length = 1  # Initial length of snake
        self.snake_x = [SIZE] * self.length  # x-y co-ordinates for image to be loaded ("a snake" in this case)
        self.snake_y = [SIZE] * self.length
        self.parent_surface = parent_surface  # Attribute (member variable) that will take data from the Game class "surface" attribute
        self.direction = (0,SIZE,)  # This sets an initial down direction for the snake to move in.
        self.score_val = 0

    def draw_snake(self):
        self.parent_surface.blit(self.snake_head, (self.snake_x[0], self.snake_y[0]))  # Drawing snake's head

        for _i in range(1, self.length):
            self.parent_surface.blit(self.snake_body, (self.snake_x[_i], self.snake_y[_i]))  # Drawing snake's body

    # Keyboard input validation!
    def set_direction(self, new_direction):
        # Update the direction only if the new direction is not opposite of the current direction
        if (new_direction[0] + self.direction[0],new_direction[1] + self.direction[1],) != (0, 0):
            self.direction = new_direction

    def movement(self):
        for _i in range(self.length - 1, 0, -1):  # Reverse for loop is responsible for the x-y position values of all the "snake body" snakes
            self.snake_x[_i] = self.snake_x[_i - 1]
            self.snake_y[_i] = self.snake_y[_i - 1]

        keys = (pygame.key.get_pressed())  # Returns a list with the state of all keyboard buttons

        # Checks state of arrow keys, if pressed, moves the snakes in corresponding direction (-/+ SIZE (x-y)), only if valid by calling set_direction method

        if keys[K_UP]:
            self.set_direction((0, -SIZE))
        elif keys[K_DOWN]:
            self.set_direction((0, SIZE))
        elif keys[K_LEFT]:
            self.set_direction((-SIZE, 0))
        elif keys[K_RIGHT]:
            self.set_direction((SIZE, 0))

        self.snake_x[0] += self.direction[0]  # Sums the new snake xy values and the current snake xy values
        self.snake_y[0] += self.direction[1]

        self.draw_snake()

    def extend_length(self):  # Instance Method to extend the snake length
        self.length += 1  # Increments the length of the snake list variable

        self.snake_y.append(None)  # Appends a new space for a set of xy co-ordinate to the end of the list for the new snake block
        self.snake_x.append(None)


class Game:
    def __init__(self):
        self.game_running = True  # Game State flag variable
        pygame.init()
        pygame.display.set_caption("Said Ali's Snake")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Creates a display[w x h]
        self.snake_icon = pygame.image.load("resources/snake_icon.png").convert_alpha()
        self.font_intro_ending = pygame.font.SysFont("Candara", 100)  # Initialises intro font
        self.font = pygame.font.SysFont("Candara", 50)  # Initialises start screen font
        play_button = pygame.Rect(200,200,110,60)
        self.score_alert = [10, 20, 30, 40]

        self.render_bg()  # Fills background with selected background image
        self.snake = Snake(self.surface)
        self.snake.draw_snake()
        self.apple = Apple(self.surface)
        self.apple.draw()  # Draws apple
        self.bg_music()
        self.intro()

    def render_bg(self):
        border = pygame.image.load("resources/border.png").convert_alpha()
        background = pygame.image.load("resources/background.jpg").convert()
        self.surface.blit(background, (0, 0))
        self.surface.blit(border, (0, 0))

    def collision(self):
        apple_x = self.apple.x  # Takes x-y co-ordinates of the apple
        apple_y = self.apple.y

        if (self.snake.snake_x[0] == apple_x and self.snake.snake_y[0] == apple_y):  # Compares "snake head/first snake" x-y position to apple x-y position
            
            self.apple.respawn()  # Respawns apple in new location
            self.snake.extend_length()  # Call snake method to extend length
            self.snake.score_val += 1  # Increments score value
            self.sound_effect(1)

            # Score checkpoint when snake collides with 10th apple
            if self.snake.score_val in self.score_alert:
                self.sound_effect(4)

        # Ends the game if the snake eats itself
        for _i in range(3, self.snake.length):
            if (self.snake.snake_x[0] == self.snake.snake_x[_i]and self.snake.snake_y[0] == self.snake.snake_y[_i]):
                self.sound_effect(2)
                self.game_over()

        # End the game if the snake exceeds the screen boundary
        if self.snake.snake_x[0] > (SCREEN_WIDTH) or self.snake.snake_y[0] > (SCREEN_HEIGHT):
            self.sound_effect(3)
            self.game_over()

        elif self.snake.snake_x[0] < 0 or self.snake.snake_y[0] < 0:
            self.sound_effect(3)
            self.game_over()

    def game_over(self):
        self.render_bg()
        self.gameover_text = self.font.render("Game Over", True, (255, 0, 70))
        self.surface.blit(self.gameover_text, (280, 250))
        pygame.display.flip()
        time.sleep(1.5)
        self.reset()

    def exit(self):
        self.game_running = False
        self.render_bg()
        self.exit_text = self.font.render("Exiting...", True, (255, 0, 70))
        self.surface.blit(self.exit_text, (300, 50))
        pygame.display.flip()

    def score(self):
        self.score_text = self.font.render(f"{self.snake.score_val}", True, (255, 0, 70))
        self.surface.blit(self.score_text, (720, 40))
        pygame.display.flip()
        self.hs_text = self.font.render(f"High Score: {self.snake.score_val}", True, (255, 0, 70))  # Highscore text

        if self.snake.score_val == 50:  # Highest score, player has won
            self.win()

    # Method to reset the game. Displays "Play again" and "Exit" text
    def reset(self):
        self.render_bg()
        play_again = self.font.render("Press Space to play again.", True, (255, 0, 70))
        esc_game = self.font.render("Press ESC to quit.", True, (255, 0, 70))
        self.surface.blit(play_again, (150, 100))
        self.surface.blit(esc_game, (230, 400))
        self.surface.blit(self.hs_text, (250, 250))
        pygame.display.flip()
        pygame.event.clear()

        while self.game_running:
            event = pygame.event.wait()

            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:
                    self.snake = Snake(self.surface)  # Resets the game and creates a new Snake and Apple object
                    self.apple = Apple(self.surface)
                    self.run()

                if event.key == K_ESCAPE:
                    self.exit()

            elif event.type == QUIT:
                self.exit()

    def bg_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Plays bg music on a loop (-1)

    def sound_effect(self, type):
        self.type = type
        pop = pygame.mixer.Sound("resources/pop.mp3")
        bite = pygame.mixer.Sound("resources/bite.mp3")
        crash = pygame.mixer.Sound("resources/crash.mp3")
        score_checkpoint = pygame.mixer.Sound("resources/score_checkpoint.mp3")
        won = pygame.mixer.Sound("resources/won.mp3")

        if self.type == 1:
            pygame.mixer.Sound.play(pop, 0)
        if self.type == 2:
            pygame.mixer.Sound.play(bite, 0)
        if self.type == 3:
            pygame.mixer.Sound.play(crash, 0)
        if self.type == 4:
            pygame.mixer.Sound.play(score_checkpoint, 0)
        if self.type == 5:
            pygame.mixer.Sound.play(won, 0)

    def play(self):
        self.render_bg()
        self.snake.movement()  # Updates snake x-y co-ordinates corresponding to key presses, then prints snake to the screen
        self.apple.draw()  # Draws apple
        self.collision()  # Runs collision method
        self.score()  # Displays score
        time.sleep(0.07)  # A small delay to prevent the snakes from updating its position too quickly on the screen

    def intro(self):
        self.render_bg()
        self.surface.blit(self.snake_icon, (160, 230))
        play_text = self.font.render("Press Space to play!", True, (255, 0, 70))
        intro_text = ["S", "n", "a", "k", "e"]
        x = 280  # X-axis location of first letter

        for _i in range(0, (len(intro_text))):  # For loop to iterate over the intro_text letters
            intro = self.font_intro_ending.render(f"{intro_text[_i]}", True, (255, 0, 70))
            self.surface.blit(intro, (x, 230))
            pygame.display.flip()
            time.sleep(0.35)
            x += 50  # Increase x-axis value to print text accross the screen

        self.surface.blit(play_text, (180, 400))    
        pygame.display.flip()

     # Press "Space" to play game
        while self.game_running:
            event = pygame.event.wait()

            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:
                    self.run() 

                if event.key == K_ESCAPE:
                    self.exit()

            elif event.type == QUIT:
                self.exit()

    def win(self):
        won = True
        self.render_bg()
        self.sound_effect(5)
        end_text = ["Congradulations!", " You have won!", "Press Space to continue"]

        endtext_1 = self.font_intro_ending.render(end_text[0], True, (255, 0, 70))
        endtext_2 = self.font_intro_ending.render(end_text[1], True, (255, 0, 70))
        endtext_3 = self.font.render(end_text[2], True, (0, 0, 0))

        self.surface.blit(endtext_1, (50, 100))
        self.surface.blit(endtext_2, (80, 350))
        self.surface.blit(endtext_3, (150, 500))
        self.surface.blit(self.snake_icon, (350, 250))
        pygame.display.flip()

        while won == True:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:

                    if event.key == K_SPACE:
                        won = False
                        self.reset()

                    if event.key == K_ESCAPE:
                        won = False
                        self.exit()

                elif event.type == QUIT:
                    won = False
                    self.exit()

    def run(self):
        while (self.game_running):  # Game infinite loop - broken by specified events (esc key, etc.)
            
            for event in pygame.event.get():  # Loop that gets events
                
                if (event.type == KEYDOWN):  # Conditional Statement to check if a key is pressed down
                    if (event.key == K_ESCAPE):  # Conditional Statement to check if "Escape Key" is pressed down
                        self.exit()  # Breaks UI infinite loop (exits game) if both above conditions are met

                elif (event.type == QUIT):  # Conditional Statement that checks if the event type is "QUIT" i.e. UI close button, and exits game
                    self.exit()

            self.play()


if __name__ == "__main__":
    game = Game()
    
