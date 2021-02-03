import sys
import math
import random
import pygame as pg

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
DK_GRAY = (80, 80, 80)


class Particle(pg.sprite.Sprite):
    """Builds ejecta particles for volcano simulation"""

    gas_color = {'SO2': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY, 'H2O': WHITE}

    VENT_LOCATION_XY = (320, 320)
    IO_SURFACE_Y = 308
    GRAVITY = 0.5
    VELOCITY_SO2 = 8

    vel_scalar = {'SO2': 1.6, 'CO2': 1.7, 'H2S': 1.9, 'H2O': 3.6}

    def __init__(self, screen, background):
        super().__init__()
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4, 4))
        self.rect = self.image.get_rect()
        self.gas = random.choice(list(Particle.gas_color.keys()))
        self.color = Particle.gas_color[self.gas]
        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]
        self.x, self.y = Particle.VENT_LOCATION_XY
        self.vector()

    def vector(self):
        """Calculate particle vector at launch"""
        orient = random.uniform(60, 120)
        radians = math.radians(orient)
        self.dx = self.vel * math.cos(radians)  # trigonometric equations
        self.dy = -self.vel * math.sin(radians)

    def update(self):
        """Apply gravity, draw path, and handle boundary conditions"""
        self.dy += Particle.GRAVITY
        pg.draw.line(self.background, self.color, (self.x, self.y),
                     (self.x + self.dx, self.y + self.dy))
        self.x += self.dx
        self.y += self.dy

        if self.x < 0 or self.x > self.screen.get_width():
            self.kill()
        if self.y < 0 or self.y > Particle.IO_SURFACE_Y:
            self.kill()


def main():
    """Set up and run game screen and loops."""
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption('Io Volcano Simulator')
    background = pg.image.load('tvashtar_plume.gif')

    legend_font = pg.font.SysFont('None', 24)
    water_label = legend_font.render('--- H20', True, WHITE, BLACK)
    h2s_label = legend_font.render('--- H2S', True, DK_GRAY, BLACK)
    co2_label = legend_font.render('--- C02', True, GRAY, BLACK)
    so2_label = legend_font.render('--- SO2/S2', True, LT_GRAY, BLACK)

    particles = pg.sprite.Group()

    clock = pg.time.Clock()

    while True:
        clock.tick(25)
        particles.add(Particle(screen, background))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(water_label, (40, 20))
        screen.blit(h2s_label, (40, 40))
        screen.blit(co2_label, (40, 60))
        screen.blit(so2_label, (40, 80))

        particles.update()
        particles.draw(screen)

        pg.display.flip()


if __name__ == "__main__":
    main()
