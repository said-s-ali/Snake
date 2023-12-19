# Snake game written in Python to exercise oop and python syntax.

import pygame                            # Imports pygame package
from pygame.locals import*               # Importing names (attributes) from pygame.locals module to access events and keyboard functionalities
import time

size = 40

class Snake:

     def __init__(self, parent_surface, length):
          self.block = pygame.image.load("resources/block.jpg").convert()  # Pygame method to load any image from directory
          self.length = length
          self.block_x = [size]*length                                                 # x-y co-ordinates for image to be loaded ("a block" in this case)
          self.block_y = [size]*length
          self.parent_surface = parent_surface                             # attribute (member variable) that will take data from the Game class "surface" attribute
          self.direc = "Down"                                              # This sets an initial direction for the snake to move in.
                       
          

     def draw_block(self):
          self.parent_surface.fill((52,133,73))

          for _i in range(self.length):
               self.parent_surface.blit(self.block, (self.block_x[_i], self.block_y[_i]))

          pygame.display.flip()   



     def move_up(self):                                      # When an arrow key is pressed, these methods store the direction the snake should travel
          self.direc = "Up" 

     def move_down(self):
          self.direc = "Down"  

     def move_right(self):
          self.direc = "Right" 

     def move_left(self):
          self.direc = "Left" 


     def movement(self): 
                                                                  # Reverse for loop is responsible for the x-y positioning of the "snake body" blocks                 
           for _i in range(self.length-1, 0, -1):
                self.block_x[_i] = self.block_x[_i - 1]
                self.block_y[_i] = self.block_y[_i - 1]
                                                                 # ** Add boundry control loop code here **

                                                                 # Moves the block by  by -/+ 30, depedending upon the direction value returned                                         
           if self.direc == "Up":                      
               self.block_y[0] -= 30          
               
           if self.direc == "Down":
               self.block_y[0] += 30
                
           if self.direc == "Left":
               self.block_x[0] -= 30
               
           if self.direc == "Right":
               self.block_x[0] += 30
               
           else:
               pass
           
           self.draw_block()

class Game:

     def __init__(self):
          pygame.init()
          self.surface = pygame.display.set_mode((1000,1000))   # Creates a display[l x w]
          self.surface.fill((52, 133, 73))                      # Fills background with selected RGB colour
          self.snake = Snake(self.surface, 100)
          self.snake.draw_block()

     def run(self):
          game_running = True                                   # UI event loop flag variable

          while game_running:                              # UI event infinite loop - broken by specified events (esc key, etc.) 
               
               for event in pygame.event.get():                # Loop that gets events
                    if event.type == KEYDOWN:                  # Conditional Statement to check if a key is pressed down
                         if event.key == K_ESCAPE:             # Conditional Statement to check if "Escape Key" is pressed down 
                              game_running = False             # Breaks UI infinite loop (quits game) if both above conditions are met

                         if event.key == K_UP:                # When a key is pressed down, and that key is the Up Arrow Key, variable returns direction value
                              self.snake.move_up()
                              

                         if event.key == K_DOWN:              # When a key is pressed down, and that key is the Down Arrow Key, variable returns direction value
                               self.snake.move_down()
                              
                              
                              

                         if event.key == K_LEFT:             # When a key is pressed down, and that key is the Left Arrow Key, variable returns direction value
                               self.snake.move_left()
                              
                              

                         if event.key == K_RIGHT:            # When a key is pressed down, and that key is the Right`` Arrow Key, variable returns direction value
                               self.snake.move_right()
                                     

                    elif event.type == QUIT:                   # Conditional Statement that checks if the event type is "QUIT" i.e. UI close button, and quits game
                         game_running = False
                    
               
               self.snake.movement()       # Updates block x-y co-ordinates corresponding to key presses, then prints block to the screen
               time.sleep(0.1)             # A small delay to prevent the blocks from updating its position too quickly on the screen
               
          



if __name__ == "__main__":               # Only initialises if this script is the main program.
    
     game = Game()
     game.run()
    
    
    

#---------------------------------------------------------------GAME RUNNING-----------------------------------------------------------------------------------#

     
        
                   



    



 