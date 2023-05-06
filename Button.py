import pygame


class Button():
    def __init__(self, x, y, text_input, base_color,hovering_color, background_color,screen_surface):
        self.screen_surface = screen_surface
        self.font =pygame.font.Font("Foonts\DejaVuSerif-BoldItalic.ttf", 25)
        self.text_input = text_input
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.text.get_rect(center=(x, y))
        self.background_color = background_color
        self.current_background_color = background_color
        self.clicked = False

    def animation(self):
        if self.rect.collidepoint(self.get_mouse_pos()):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.current_background_color = self.base_color

        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.current_background_color = self.background_color


    def get_mouse_pos(self):
        pos = pygame.mouse.get_pos()
        return pos

    def isclicked(self):

        if self.rect.collidepoint(self.get_mouse_pos()):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked

    def draw(self):

        # draw the button
        pygame.draw.rect(self.screen_surface, self.current_background_color, self.rect, 0, 5)
        self.screen_surface.blit(self.text, self.rect)

    def update(self):
        self.draw()
        self.animation()


