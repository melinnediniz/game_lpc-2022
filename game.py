import pygame

from config import Constants, Aim, Images, Lives
from config import display_lives, update_live
from players import Player
from ball import Ball
from sys import exit

# screen
screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
pygame.display.set_caption("DODGE-BALL INVASION")
pygame.display.set_icon(Images.icon)

# control var of sprite coordinates
player_1 = Player(30, 300, 'player_1')
player_2 = Player(900, 300, 'player_2')
collision = 75


# Balls
ball_1 = Ball(position_x=240,
              position_y=325,
              ball_image='ball_1')

ball_2 = Ball(position_x=730,
              position_y=325,
              ball_image='ball_2')

movements = dict(
    up=lambda: player_1.moves('up'),
    down=lambda: player_1.moves('down'),
    right=lambda: player_1.moves('right'),
    left=lambda: player_1.moves('left')
)
key_pressed = set()


def move_player():
    for move in key_pressed:
        movements[move]()


player_1.get_ball(ball_1)
player_2.get_ball(ball_2)


# mouse invisible
pygame.mouse.set_visible(False)


class Game:
    def __init__(self):
        self.current_screen = "start_screen"

    def start_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.current_screen = "main"
                elif event.key == pygame.K_ESCAPE:
                    exit()

        screen.blit(Images.menu, Constants.COURT_CORD)
        pygame.display.flip()

    # PLAYING THE GAME
    @staticmethod
    def main():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    key_pressed.add('right')
                elif event.key == pygame.K_LEFT:
                    key_pressed.add('left')
                elif event.key == pygame.K_UP:
                    key_pressed.add('up')
                elif event.key == pygame.K_DOWN:
                    key_pressed.add('down')
                elif event.key == pygame.K_SPACE:
                    player_1.throw()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    key_pressed.remove('right')
                elif event.key == pygame.K_LEFT:
                    key_pressed.remove('left')
                elif event.key == pygame.K_UP:
                    key_pressed.remove('up')
                elif event.key == pygame.K_DOWN:
                    key_pressed.remove('down')

        move_player()
        if player_1.throw_ball:
            ball_1.move('player_1')

        if player_2.throw_ball:
            ball_2.move('player_2')

        # ball collision with player_1
        if ball_2.position_x <= player_1.position_x:
            if player_1.position_y < ball_2.position_y + collision:
                if player_1.position_y + collision > ball_2.position_y:
                    update_live(1)
                    player_2.hold()
                    player_2.throw_ball = False
                    
        # ball collision with player_2 (npc)
        if ball_1.position_x > player_2.position_x:
            if player_2.position_y < ball_1.position_y + collision:
                if player_2.position_y + collision > ball_1.position_y:
                    update_live(2)
                    player_1.hold()
                    player_1.throw_ball = False

        player_1.wall_limits()

        if ball_1.position_x > 1000:
            player_1.throw_ball = False
            player_1.hold()

        if ball_2.position_x < 0:
            player_2.throw_ball = False
            player_2.hold()

        player_2.npc(enemy=player_1, ball_enemy=ball_1)

        # scope position
        mx = player_1.position_x + 100
        my = player_2.position_y + 50
        if mx >= 968:
            mx = 968
        if my >= 668:
            my = 668

        # drawing the objects
        screen.blit(Images.court, Constants.COURT_CORD)
        screen.blit(Aim.scope, (mx - 16, my - 16))
        display_lives(screen, Lives.P1_LIVE_POS, 'player 1')
        display_lives(screen, Lives.P2_LIVE_POS, 'player 2')
        player_1.render(screen)
        player_2.render(screen)
        ball_1.render(screen)
        ball_2.render(screen)

        # update screen
        pygame.display.flip()

    def change_screen(self):
        if self.current_screen == "start_screen":
            self.start_screen()
        if self.current_screen == "main":
            self.main()
