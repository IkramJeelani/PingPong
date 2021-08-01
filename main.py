import random, pygame

pygame.init()
pygame.font.init()

# screen
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("!PiNg PoNg¡")
FPS = 60

# blocks
BLOCK_WIDTH, BLOCK_HEIGHT = 60, 5
BLOCK_VEL = 5
PLAYER_1_X = WIDTH / 2 - (BLOCK_WIDTH / 2)
PLAYER_1_Y = (296 / 2) / 2
PLAYER_2_X = WIDTH / 2 - (BLOCK_WIDTH / 2)
PLAYER_2_Y = ((HEIGHT - 148) + (148 / 2)) - BLOCK_HEIGHT

# ball
BALL_WIDTH, BALL_HEIGHT = 20, 20
BALL_VEl = 5

# events
BALL_COLLIDED_EVENT = pygame.USEREVENT + 1
BALL_X_GREATER = pygame.USEREVENT + 2
BALL_X_LOWER = pygame.USEREVENT + 3
BALL_Y_GREATER = pygame.USEREVENT + 4
BALL_Y_LOWER = pygame.USEREVENT + 5
PLAYER_1_COLLIDED = pygame.USEREVENT + 6
PLAYER_2_COLLIDED = pygame.USEREVENT + 7
WALL_COLLIDED = pygame.USEREVENT + 8
PLAYER_1_POINT = pygame.USEREVENT + 9
PLAYER_2_POINT = pygame.USEREVENT + 10

# text
PLAYER_POINT_TEXT = pygame.font.SysFont("comicsans", 70)


def drawing(player_1_block, player_2_block, ball_block, player_1_points, player_2_points):
    WIN.fill((0, 0, 0))
    pygame.draw.rect(WIN, (255, 255, 255), [0, HEIGHT / 2 - 4, WIDTH, 8])

    pygame.draw.rect(WIN, (0, 255, 0),
                     (ball_block.x, ball_block.y, ball_block.width, ball_block.height))
    pygame.draw.rect(WIN, (255, 0, 0),
                     (player_1_block.x, player_1_block.y, player_1_block.width, player_1_block.height))
    pygame.draw.rect(WIN, (0, 0, 255),
                     (player_2_block.x, player_2_block.y, player_2_block.width, player_2_block.height))

    player_1_points_show = PLAYER_POINT_TEXT.render(str(player_1_points), True, (255, 255, 255))
    WIN.blit(player_1_points_show, (player_1_points_show.get_width(), player_1_points_show.get_height()))
    player_2_points_show = PLAYER_POINT_TEXT.render(str(player_2_points), True, (255, 255, 255))
    WIN.blit(player_2_points_show,
             (WIDTH - (player_2_points_show.get_width() * 2), HEIGHT - (player_2_points_show.get_height() * 2)))

    pygame.display.flip()


def controls(key, player_1_block, player_2_block):
    if key[pygame.K_a] and player_1_block.x - BLOCK_VEL > 0:
        player_1_block.x -= BLOCK_VEL
    if key[pygame.K_d] and player_1_block.x + BLOCK_VEL + BLOCK_WIDTH < WIDTH:
        player_1_block.x += BLOCK_VEL

    if key[pygame.K_LEFT] and player_2_block.x - BLOCK_VEL > 0:
        player_2_block.x -= BLOCK_VEL
    if key[pygame.K_RIGHT] and player_2_block.x + BLOCK_VEL + BLOCK_WIDTH < WIDTH:
        player_2_block.x += BLOCK_VEL


def ball_movement(ball_collided, random_initial_ball_x, random_initial_ball_y, ball_block, ball_x_increase,
                  ball_y_increase, wall_collided):
    if not ball_collided:
        ball_block.x += random_initial_ball_x
        if random_initial_ball_y == 0:
            ball_block.y -= BALL_VEl / 2
        else:
            ball_block.y += BALL_VEl / 2
    elif wall_collided:
        if ball_x_increase:
            ball_block.x -= BALL_VEl
        else:
            ball_block.x += BALL_VEl
        if ball_y_increase:
            ball_block.y -= BALL_VEl
        else:
            ball_block.y += BALL_VEl
    else:
        if ball_x_increase:
            ball_block.x += BALL_VEl
        else:
            ball_block.x -= BALL_VEl
        if ball_y_increase:
            ball_block.y -= BALL_VEl
        else:
            ball_block.y += BALL_VEl


def collisions(player_1_block, player_2_block, ball_block, ball_x_record, ball_y_record, player_1_collided,
               player_2_collided):
    if player_1_block.colliderect(ball_block) and player_1_collided == False:
        pygame.event.post(pygame.event.Event(BALL_COLLIDED_EVENT))
        pygame.event.post(pygame.event.Event(PLAYER_1_COLLIDED))
        if ball_x_record[len(ball_x_record) - 1] > ball_x_record[len(ball_x_record) - 2]:
            pygame.event.post(pygame.event.Event(BALL_X_GREATER))
        else:
            pygame.event.post(pygame.event.Event(BALL_X_LOWER))
        if ball_y_record[len(ball_y_record) - 1] > ball_y_record[len(ball_y_record) - 2]:
            pygame.event.post(pygame.event.Event(BALL_Y_GREATER))
        else:
            pygame.event.post(pygame.event.Event(BALL_Y_LOWER))

    if player_2_block.colliderect(ball_block) and player_2_collided == False:
        pygame.event.post(pygame.event.Event(BALL_COLLIDED_EVENT))
        pygame.event.post(pygame.event.Event(PLAYER_2_COLLIDED))
        if ball_x_record[len(ball_x_record) - 1] > ball_x_record[len(ball_x_record) - 2]:
            pygame.event.post(pygame.event.Event(BALL_X_GREATER))
        else:
            pygame.event.post(pygame.event.Event(BALL_X_LOWER))
        if ball_y_record[len(ball_y_record) - 1] > ball_y_record[len(ball_y_record) - 2]:
            pygame.event.post(pygame.event.Event(BALL_Y_GREATER))
        else:
            pygame.event.post(pygame.event.Event(BALL_Y_LOWER))

    if not ball_block.x - BALL_VEl > 0:
        pygame.event.post(pygame.event.Event(WALL_COLLIDED))
    if not ball_block.x + BALL_VEl + ball_block.width < WIDTH:
        pygame.event.post(pygame.event.Event(WALL_COLLIDED))

    if not ball_block.y - BLOCK_VEL > 0:
        pygame.event.post(pygame.event.Event(PLAYER_2_POINT))
    if not ball_block.y + BLOCK_VEL + BLOCK_HEIGHT < HEIGHT:
        pygame.event.post(pygame.event.Event(PLAYER_1_POINT))


def main():
    player_1_block = pygame.Rect(PLAYER_1_X, PLAYER_1_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
    player_2_block = pygame.Rect(PLAYER_2_X, PLAYER_2_Y, BLOCK_WIDTH, BLOCK_HEIGHT)
    ball_block = pygame.Rect((WIDTH / 2) - (BALL_WIDTH / 2), (HEIGHT / 2) - (BALL_HEIGHT / 2), BALL_WIDTH, BALL_HEIGHT)

    random_initial_ball_x = random.randint(-1, 1)
    random_initial_ball_y = random.randint(0, 1)
    ball_collided = False
    ball_x_record = []
    ball_y_record = []
    ball_x_increase = None
    ball_y_increase = None

    player_1_collided = False
    player_2_collided = False
    wall_collided = False

    player_1_points = 0
    player_2_points = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == BALL_COLLIDED_EVENT:
                ball_collided = True

            if event.type == BALL_X_GREATER:
                ball_x_increase = True
            if event.type == BALL_X_LOWER:
                ball_x_increase = False
            if event.type == BALL_Y_GREATER:
                ball_y_increase = True
            if event.type == BALL_Y_LOWER:
                ball_y_increase = False

            if event.type == PLAYER_1_COLLIDED:
                player_1_collided = True
                player_2_collided = False
                wall_collided = False
            if event.type == PLAYER_2_COLLIDED:
                player_2_collided = True
                player_1_collided = False
                wall_collided = False
            if event.type == WALL_COLLIDED:
                wall_collided = True
                player_1_collided = False
                player_2_collided = False

            if event.type == PLAYER_1_POINT:
                player_1_points += 1
                ball_collided = False
                ball_block = pygame.Rect((WIDTH / 2) - (BALL_WIDTH / 2), (HEIGHT / 2) - (BALL_HEIGHT / 2), BALL_WIDTH,
                                         BALL_HEIGHT)
                random_initial_ball_x = random.randint(-1, 1)
                random_initial_ball_y = random.randint(0, 1)
            if event.type == PLAYER_2_POINT:
                player_2_points += 1
                ball_collided = False
                ball_block = pygame.Rect((WIDTH / 2) - (BALL_WIDTH / 2), (HEIGHT / 2) - (BALL_HEIGHT / 2), BALL_WIDTH,
                                         BALL_HEIGHT)
                random_initial_ball_x = random.randint(-1, 1)
                random_initial_ball_y = random.randint(0, 1)

        ball_x_record.append(ball_block.x)
        ball_y_record.append(ball_block.y)

        key = pygame.key.get_pressed()
        controls(key, player_1_block, player_2_block)
        collisions(player_1_block, player_2_block, ball_block, ball_x_record, ball_y_record, player_1_collided,
                   player_2_collided)
        ball_movement(ball_collided, random_initial_ball_x, random_initial_ball_y, ball_block, ball_x_increase,
                      ball_y_increase, wall_collided)
        drawing(player_1_block, player_2_block, ball_block, player_1_points, player_2_points)


if __name__ == '__main__':
    main()
