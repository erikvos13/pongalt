import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500           #zo kun je meerdere variabelen definieren op 1 tekstlijn
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

WINNING_SCORE = 10
    
class Paddle:
    COLOR = WHITE             #attributen die elke instance meekrijgt kan hier en hoeft niet in een functie
    VEL = 5
    
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win,self.COLOR, (self.x, self.y, self.width, self.height))
    
    def move(self, up=True):
        if up:
            self.y -= self.VEL # x,y = 0,0 is linksbovenaan, dus omhoog is negatief!
        else:
            self.y += self.VEL    

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

def draw(win, paddles, ball1, ball2, left_score, right_score):
    win.fill(BLACK)
    
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, ((3 * WIDTH)//4 - right_score_text.get_width()//2, 20))
    
    
    for paddle in paddles:
        paddle.draw(win)
    
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    ball1.draw(win)
    ball2.draw(win)
    
    pygame.display.update()

    

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 *  y_vel
                
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1        
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel                
                

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up=True)
    if keys[pygame.K_s]:
        left_paddle.move(up=False)
        
    if keys[pygame.K_UP]:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN]:
        right_paddle.move(up=False)       
        
        

def main():
    run = True
    clock = pygame.time.Clock()
    
    left_paddle = Paddle(10,HEIGHT//2-PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH,HEIGHT//2-PADDLE_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
    
    ball1 = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    ball2 = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    ball2.x_vel = -2
    
    left_score = 0
    right_score = 0
    
    
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball1, ball2, left_score, right_score)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball1.move()
        ball2.move()
        
        handle_collision(ball1, left_paddle, right_paddle)
        handle_collision(ball2, left_paddle, right_paddle)
        
        if ball1.x < 0:
            right_score += 1
            ball1.reset()
        elif ball1.x > WIDTH:
            left_score += 1
            ball1.reset()
            
            
        if ball2.x < 0:
            right_score += 1
            ball2.reset()
        elif ball2.x > WIDTH:
            left_score += 1
            ball2.reset()
        
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left player won!"
            
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right player won!"
            
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball1.reset()
            ball2.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
    pygame.quit()

if __name__ == "__main__":
    main()