from random import randint
import pygame as pg

WIDTH = 800
HEIGHT = 600
TARGET_SIZE = 50

class Target:
    def __init__(self, font: pg.font.Font):
        x = randint(0, WIDTH - TARGET_SIZE)
        y = randint(0, HEIGHT - TARGET_SIZE)
        self.missed = False
        self.font = font
        self.score = 0
        self.score_text = lambda: f'Score: {self.score}'
        self.rect = pg.Rect(x, y, TARGET_SIZE, TARGET_SIZE)
    
    def get_mouse_click(self):
        mx, my = pg.mouse.get_pos()
        if self.rect.left < mx < self.rect.right and \
            self.rect.top < my < self.rect.bottom:
                self.score += 1
                self.respawn()
        else:
            self.missed = True if self.score > 0 else False
    
    def draw_to(self, screen: pg.Surface):
        pg.draw.rect(screen, pg.Color('red'), self.rect)
        screen.blit(self.font.render(self.score_text(), True, pg.Color("green")), [0, 0])

    def respawn(self):
        self.rect.x = randint(0, WIDTH - TARGET_SIZE)
        self.rect.y = randint(0, HEIGHT - TARGET_SIZE)


def main():
    pg.init()
    font = pg.font.Font(pg.font.get_default_font(), 20)
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    pg.display.set_caption("Aim Trainer")
    clock = pg.time.Clock()
    fps = 75

    target = Target(font)

    start_text = font.render(
        'Click the red target to begin!',
        True,
        pg.Color('green')
    )
    sx, sy = screen.get_rect().center
    sx -= start_text.get_width() // 2
    sy -= start_text.get_height() // 2

    game_over_text = font.render(
        'Game Over! Press R to restart',
        True,
        pg.Color('green')
    )
    cx, cy = screen.get_rect().center
    cx -= game_over_text.get_width() // 2
    cy -= game_over_text.get_height() // 2

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if not target.missed:
                    target.get_mouse_click()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    target.missed = False
                    target.score = 0
                    target.respawn()
        

        screen.fill(pg.Color("darkgray"))

        target.draw_to(screen)
        if target.missed:
            screen.blit(game_over_text, [cx, cy])
        elif target.score == 0:
            screen.blit(start_text, [sx, sy])

        clock.tick(fps)
    
        pg.display.update()
    
    pg.quit()


if __name__ == "__main__":
    main()