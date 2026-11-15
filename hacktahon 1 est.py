import pygame

"""
 This example shows having multiple balls bouncing around the screen at the
 same time. You can hit the space bar to spawn more balls.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""
 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25
MAX_BALLS = 12
 
 
class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0
        self.color = (0, 0, 0)
        self.r = 0
        
    def draw(self, pg, screen) :
        pg.draw.circle(screen, self.color, [self.x, self.y], self.r)
 
 
def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # Starting position of the ball.
    # Take into account the ball size so we don't spawn on the edge.
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
 
    # Speed and direction of rectangle
    ball.change_x = random.randrange(-6, 6)
    ball.change_y = random.randrange(-6, 6)
    ball.r = random.randrange(5, 25)
    ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
 
    return ball
 
def isCollision(b1, b2)->bool:
    return (b1.x-b2.x)**2+(b1.y-b2.y)**2 < (b1.r+b2.r)**2
 
def main():
    """
    This is our main program.
    """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Bouncing Ball Battles")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    ball_list = []
 
    for _ in range(MAX_BALLS) :
        
        ball = make_ball()
        ball_list.append(ball)
    
 
    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # Space bar! Spawn a new ball.
                if event.key == pygame.K_SPACE:
                    print("Add a new random ball")
                    ball = make_ball()
                    ball_list.append(ball)
 
        # --- Logic
        for ball in ball_list:
            
            # add collision detection
            for b in ball_list:
                if b!=ball and isCollision(b, ball) :
                    print("Collision detected")
                    ball_list.remove(b)
                    #TODO: how to remove the second ball participated in collision???
                    
                    break
                    
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y
 
            # Bounce the ball if needed
            if ball.y > SCREEN_HEIGHT - ball.r or ball.y < ball.r :
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - ball.r or ball.x < ball.r :
                ball.change_x *= -1
 
        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)
 
        # Draw the balls
        for ball in ball_list:
            ball.draw(pygame, screen)
 
        # --- Wrap-up
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Close everything down
    pygame.quit()
 
if __name__ == "__main__":
    main
    
