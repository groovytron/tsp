import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
from travel import City


class Gui:
    """Gui screen using pygame."""
    def __init__(self, cities=None):
        self.screen_x = 500
        self.screen_y = 500
        self.city_color = [10, 10, 200]  # blue
        self.city_radius = 3
        self.font_color = [255, 255, 255]  # white
        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('Exemple')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.collecting = True

        if cities:
            self.cities = cities
            self.draw()
            self.wait_for_user_input()
        else:
            self.cities = {}
            self.place_cities()

    def wait_for_user_input(self):
        while self.collecting:
            for event in pygame.event.get():
                if (event.type == QUIT or
                        (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    self.collecting = False

    def place_cities(self):
        city_counter = 0
        while self.collecting:
            for event in pygame.event.get():
                if (event.type == QUIT or
                        (event.type == KEYDOWN and event.key == K_ESCAPE)):
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    self.collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    name = "v{}".format(city_counter)
                    self.cities[name] = City(name, pos)
                    city_counter = city_counter + 1
                    self.draw()

    def draw(self):
        self.screen.fill(0)

        for city in self.cities.values():
            pygame.draw.circle(
                self.screen, self.city_color, city.position, self.city_radius
            )

        text = self.font.render(
            "Nombre: {}".format(len(self.cities)), True, self.font_color
        )
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()
