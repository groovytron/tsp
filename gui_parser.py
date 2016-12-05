def get_cities():
    import pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
    import sys
    from city import City

    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

    i=0

    def draw(cities):
        screen.fill(0)
        for city in cities:
            pygame.draw.circle(screen, city_color, city.position, city_radius)
        text = font.render("Nombre: %i" % len(cities), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()


    cities = {}

    collecting = True

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                pos =pygame.mouse.get_pos()
                name = "v{}".format(i)
                cities[name] = City(name,pos)
                i=i+1
                draw(cities.values())

    return cities
