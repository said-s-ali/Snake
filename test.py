# Snake game written in Python to exercise oop and python syntax.

import pygame                            # Imports pygame package
from pygame.locals import*               # Importing names (attributes) from pygame.locals module to access events and keyboard functionalities
import time


class Snake:

     def __init__(self, parent_surface):
          self.block = pygame.image.load("resources/block.jpg").convert()  # Pygame method to load any image from directory
          self.snake_pic = pygame.image.load("resources/snake.jpg").convert()  # Pygame method to load any image from directory
          self.block_x = [0,0,0]                                      # x-y co-ordinates *LIST* for image to be loaded ("a block" in this case)          
          self.block_y = [0,40,-20]     
          self.parent_surface = parent_surface
          self.direc = "Down"                      
          

     def draw_block(self):
          self.parent_surface.fill((52,133,73)) 
          self.parent_surface.blit(self.snake_pic, (self.block_x[0], self.block_y[0]))
          self.parent_surface.blit(self.block, (self.block_x[1], self.block_y[1]))
          pygame.display.flip()   


     def direction(self, direc):
          self.direc = direc
          return self.direc
          
     def movement(self):
           if self.direc == "Up":
               
               self.block_y[1] -= 10

               self.block_y[0] = self.block_y[1] - 40   #--
               self.block_x[0] = self.block_x[1]        #--

      #-- These blocks of code "Allow" the snakes HEAD to appear as the "first" block when moving around
      #-- This was done by manipulating the x-y co-ordinates of the blocks when moving in different directions
      #-- However, this code does not seem efficient when more snake blocks are going to be added... To Be Changed.. 


           if self.direc == "Down":
               
               self.block_y[1] += 10

               self.block_y[0] = self.block_y[1] + 40  #--
               self.block_x[0] = self.block_x[1]       #--
                

           if self.direc == "Left":
               self.block_x[0] -= 10

               self.block_x[1] = self.block_x[0] + 40   #--
               self.block_y[1] = self.block_y[0]        #--
              

               
           if self.direc == "Right":
               self.block_x[0] += 10

               self.block_x[1] = self.block_x[0] - 40
               self.block_y[1] = self.block_y[0]

              
               
           else:
               pass
           
           self.draw_block()

class Game:

     def __init__(self):
          pygame.init()
          pygame.font.init()
          self.surface = pygame.display.set_mode((1000,1000))   # Creates a display[l x w]
          self.surface.fill((52, 133, 73))                      # Fills background with selected RGB colour
          self.snake = Snake(self.surface)
          self.snake.draw_block()

     def run(self):
          game_running = True                                   # UI event loop flag variable

          while game_running:                              # UI event infinite loop - broken by specified events (esc key, etc.) 
               
               for event in pygame.event.get():                # Loop that gets events
                    if event.type == KEYDOWN:                  # Conditional Statement to check if a key is pressed down
                         if event.key == K_ESCAPE:             # Conditional Statement to check if "Escape Key" is pressed down 
                              game_running = False             # Breaks UI infinite loop (quits game) if both above conditions are met

                         if event.key == K_UP:                # When a key is pressed down, and that key is the Up Arrow Key, move block up by 10
                              direction = "Up"
                              self.snake.direction(direction)
                              

                         if event.key == K_DOWN:              # When a key is pressed down, and that key is the Down Arrow Key, move block down by 10
                              direction = "Down"
                              self.snake.direction(direction)
                              
                              
                              

                         if event.key == K_LEFT:             # When a key is pressed down, and that key is the Left Arrow Key, move block left by 10
                              direction = "Left"
                              self.snake.direction(direction)
                              
                              

                         if event.key == K_RIGHT:            # When a key is pressed down, and that key is the Right`` Arrow Key, move block up by 10
                              direction = "Right"
                              self.snake.direction(direction)

                  
                    elif event.type == QUIT:                   # Conditional Statement that checks if the event type is "QUIT" i.e. UI close button, and quits game
                         game_running = False
                    
               
               self.snake.movement()
               time.sleep(0.1)
               
          



if __name__ == "__main__":               # Only initialises if this script is the main program.
    
     game = Game()
     game.run()
    
    
    

#---------------------------------------------------------------GAME RUNNING-----------------------------------------------------------------------------------#

     
        
                   



    



 