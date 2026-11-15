import pygame
import random
import asyncio

# Define some variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25

async def main():
    
    pygame.init()

    font = pygame.font.Font(None, 32)

    MAX_BALLS = random.randint(1, 15)

    class Ball:
        """Class to keep track of a ball's location and vector."""
        def __init__(self):
            self.x = 0
            self.y = 0
            self.change_x = 0
            self.change_y = 0
            self.color = (0, 0, 0)
            self.r = 0
            self.hit = 0
            self.max_hit = 3
            self.cooldown = 0  # Prevents multi-hits during a single overlap

        def draw(self, pg, screen):
            pg.draw.circle(screen, self.color, [self.x, self.y], self.r)

    def make_ball():
        """Function to make a new, random ball."""
        ball = Ball()
        ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
        ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
        
        # Ensure balls don't spawn stationary (0 speed)
        ball.change_x = random.choice([-5, -4, -3, 3, 4, 5])
        ball.change_y = random.choice([-5, -4, -3, 3, 4, 5])
        
        ball.r = 23
        ball.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        ball.hit = 0
        ball.max_hit = 3
        ball.cooldown = 0
        return ball

    def isCollision(b1, b2) -> bool:
        return (b1.x - b2.x)**2 + (b1.y - b2.y)**2 < (b1.r + b2.r)**2

    def hit_count(ball):
        if ball.cooldown == 0:
            ball.hit += 1
            ball.cooldown = 20  # 20 frames

    def ball_died(ball):
        return ball.hit >= ball.max_hit

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    done = False
    clock = pygame.time.Clock()

    ball_list = []
    for _ in range(MAX_BALLS):
        ball_list.append(make_ball())

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if len(ball_list) == 1:
            text = font.render('WINNER', True, WHITE, BLACK)
            textRect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.fill(BLACK)
            screen.blit(text, textRect)
            pygame.display.flip()
            continue
            
        if len(ball_list) == 0:
            text = font.render('TIE', True, WHITE, BLACK)
            textRect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.fill(BLACK)
            screen.blit(text, textRect)
            pygame.display.flip()
            continue

        # --- Logic
        # Tick down cooldowns for all active balls
        for ball in ball_list:
            if ball.cooldown > 0:
                ball.cooldown -= 1

        # Iterate over a copy of the list so we can safely remove balls
        for ball in ball_list[:]:
            if ball not in ball_list:
                continue

            for b in ball_list[:]:
                if b not in ball_list or b == ball:
                    continue

                if isCollision(b, ball):
                    print("Collision detected")
                    
                    # Register hit on BOTH balls
                    hit_count(ball)
                    hit_count(b)

                    # Bounce balls away from each other
                    ball.change_x *= -1
                    ball.change_y *= -1
                    b.change_x *= -1
                    b.change_y *= -1

                    # Remove the second ball if it reached 3 hits
                    if ball_died(b) and b in ball_list:
                        ball_list.remove(b)

                    # Remove the first ball if it reached 3 hits
                    if ball_died(ball) and ball in ball_list:
                        ball_list.remove(ball)
                    break

            # Move the ball's center if it wasn't eliminated
            if ball in ball_list:
                ball.x += ball.change_x
                ball.y += ball.change_y

                # Bounce off screen edges
                if ball.y > SCREEN_HEIGHT - ball.r or ball.y < ball.r:
                    ball.change_y *= -1
                if ball.x > SCREEN_WIDTH - ball.r or ball.x < ball.r:
                    ball.change_x *= -1

        # --- Drawing
        screen.fill(BLACK)

        for ball in ball_list:
            ball.draw(pygame, screen)
        
     

        # --- Wrap-up
        clock.tick(60)
        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
     
