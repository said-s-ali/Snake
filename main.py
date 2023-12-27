# Snake game written in Python to exercise oop and python syntax.

import pygame                            # Imports pygame module
from pygame.locals import*               # Importing names (attributes) from pygame.locals module to access events and keyboard functionalities
import time                              
import random


size = 40                                # Pixle, or image size of each block (40 x 40) - Global Variable


class Apple:                             # Class to draw, and spawn an apple object
   
     def __init__(self, parent_surface):
          self.apple = pygame.image.load("resources/apple.jpg").convert()
          self.parent_surface = parent_surface
          self.x = 0
          self.y = 0
          self.pos_x = 3      # apple x position
          self.pos_y = 3      # apple y position

     
                                             # self.pos_x/y is the actual x-y co-ordinate of the apple. self.x/y is the co-ordinate when multiplied by size
     def draw(self):
          self.x = size * self.pos_x         # X-Y of apple is a multiple of "size" for snake to be able to move fully across it, "pos" variable used to change apple position when it is eaten
          self.y = size * self.pos_y
          self.parent_surface.blit(self.apple, (self.x, self.y))
          pygame.display.flip()
          #self.type()?
          

     def type(self):      # Add different type of apples here, with a random apple type selector          
          pass
     
     def respawn(self):
          self.pos_y = random.randrange(1, 29)   # Spawn apple in new and random location... 
          self.pos_x = random.randrange(1, 29)   #...apple cannot spawn out of the defined window boundary 1200 x 1200 (1200 / 40 = 30) | Set to 29 


class Snake:

     def __init__(self, parent_surface):
          self.block = pygame.image.load("resources/block.jpg").convert()  # Pygame method to load any image from directory
          self.length = 1                                                  # Initial length of snake
          self.block_x = [size]* self.length                               # x-y co-ordinates for image to be loaded ("a block" in this case)
          self.block_y = [size]* self.length
          self.parent_surface = parent_surface                             # attribute (member variable) that will take data from the Game class "surface" attribute
          self.direc = "Down"                                              # This sets an initial direction for the snake to move in.
                       
          

     def draw_block(self):
          self.parent_surface.fill((52,133,73))
          
          for _i in range(self.length):
               self.parent_surface.blit(self.block, (self.block_x[_i], self.block_y[_i]))
          
          pygame.display.flip()   

     # When an arrow key is pressed, these methods store the direction the snake will travel in
     def move_up(self):                                          
          self.direc = "Up" 

     def move_down(self):
          self.direc = "Down"  

     def move_right(self):
          self.direc = "Right" 

     def move_left(self):
          self.direc = "Left" 

     def movement(self): 
                                                                                   
           for _i in range(self.length-1, 0, -1):                # Reverse for loop is responsible for the x-y position values of all the "snake body" blocks
                self.block_x[_i] = self.block_x[_i - 1]
                self.block_y[_i] = self.block_y[_i - 1]
                                                                  # ** Add boundry control loop code here **
                
          # Moves the blocks by -/+ 40, depedending upon the direction value returned                                                                                              
           if self.direc == "Up":                      
               self.block_y[0] -= size          
               
           if self.direc == "Down":
               self.block_y[0] += size
                
           if self.direc == "Left":
               self.block_x[0] -= size
               
           if self.direc == "Right":
               self.block_x[0] += size
               
           else:
               pass
           
           self.draw_block()
           

     def extend_length(self):                # Instance Method to extend the snake length
          
          self.length += 1                   # Increments the length of the snake list variable
                                             
          self.block_y.append(40)            # Appends a new set of xy co-ordinate to the end of the list for the new block
          self.block_x.append(40)
          
     

class Game:

     def __init__(self):
          self.game_running = True                              # Game State flag variable (bool)
          pygame.init()
          self.surface = pygame.display.set_mode((1200,1200))   # Creates a display[l x w]
          self.surface.fill((52, 133, 73))                      # Fills background with selected RGB colour
          self.snake = Snake(self.surface)
          self.snake.draw_block()
          self.apple = Apple(self.surface)
          self.font = pygame.font.SysFont("Calbri",50)          # Initialises fonts
          self.score_val = 0                                    

     def collision(self):         
          
          apple_x = self.apple.x               # Takes x-y co-ordinates of the apple         
          apple_y = self.apple.y

          if self.snake.block_x[0] == apple_x and self.snake.block_y[0] == apple_y:           # Compares "snake head/first block" x-y position to apple x-y position                                                          
               self.apple.respawn()                                                           # Respawns apple in new location
               self.snake.extend_length()                                                     # Call snake method to extend length
               self.score_val += 1                                                            # Increments score value
                  
               
          for _i in range(1, self.snake.length):   # Ends the game if the snake eats itself
                if self.snake.block_x[0] == self.snake.block_x[_i] and self.snake.block_y[0] == self.snake.block_y[_i]:
                     self.game_over() 

          
     def game_over(self):

          self.gameover_text = self.font.render("Game Over", True, 230)
          self.surface.blit(self.gameover_text, (500,100))
          self.surface.blit(self.hs_text, (500,300))
          pygame.display.flip() 
          time.sleep(3)
          self.reset()

          

     def exit(self):

          self.game_running = False
          self.exit_text = self.font.render("Exiting...", True, (000,000,000))
          self.surface.blit(self.exit_text, (500,100))
          pygame.display.flip()
          pygame.time.wait()                                                     
          
                 

     def score(self):

          self.score_text = self.font.render(f"{self.score_val}", True, (255, 255,255))
          self.surface.blit(self.score_text, (1150,10))
          pygame.display.flip()
          self.hs_text = self.font.render(f"High Score: {self.score_val}", True, (255, 255,255))   # Highscore text

     def reset(self):                                                                              # Method to reset the game. Displays "Play again" and "Exit" Text
         self.surface.fill((52, 133, 73))
         play_again = self.font.render("Press ENTER to play again.", True, (255,255,255))
         end_game = self.font.render("Press ESC to quit.", True, (255,255,255))
         self.surface.blit(play_again, (500,100))
         self.surface.blit(end_game, (500,300))
         pygame.display.flip()
         pygame.event.clear()

         while self.game_running:          # Add death/ retry counter here?
              event = pygame.event.wait()
              if event.type == KEYDOWN:
                   if event.key == K_RETURN:
                        self.__init__()           # Resets the game. Creates new window, new objects, and runs game.
                        self.run() 

                   if event.key == K_ESCAPE:
                        self.exit()                       

     def play(self):
               
               self.snake.movement()         # Updates block x-y co-ordinates corresponding to key presses, then prints block to the screen
               self.apple.draw()             # Draws apple
               self.collision()              # Runs collision method  
               self.score()                  # Displays score      
               time.sleep(0.15)              # A small delay to prevent the blocks from updating its position too quickly on the screen

     def run(self):
                                                                     
          while self.game_running:                             # Game infinite loop - broken by specified events (esc key, etc.) 
               
               for event in pygame.event.get():                # Loop that gets events
                    if event.type == KEYDOWN:                  # Conditional Statement to check if a key is pressed down
                         if event.key == K_ESCAPE:             # Conditional Statement to check if "Escape Key" is pressed down 
                              self.exit()                      # Breaks UI infinite loop (exits game) if both above conditions are met

                         if event.key == K_UP:                 # When a key is pressed down, and that key is the Up Arrow Key, variable returns direction value
                              self.snake.move_up()
                              

                         if event.key == K_DOWN:               # When a key is pressed down, and that key is the Down Arrow Key, variable returns direction value
                               self.snake.move_down()
                              
                              
                              

                         if event.key == K_LEFT:               # When a key is pressed down, and that key is the Left Arrow Key, variable returns direction value
                               self.snake.move_left()
                              
                              

                         if event.key == K_RIGHT:              # When a key is pressed down, and that key is the Right Arrow Key, variable returns direction value
                               self.snake.move_right()
                                     

                    elif event.type == QUIT:                   # Conditional Statement that checks if the event type is "QUIT" i.e. UI close button, and exits game
                         self.exit()
     
               self.play()
               
#---------------------------------------------------------------GAME RUNNING-----------------------------------------------------------------------------------#

if __name__ == "__main__":                 # Only initialises if this script is the main program.
    
     game = Game()
     game.run()
    