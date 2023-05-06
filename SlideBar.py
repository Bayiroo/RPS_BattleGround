import pygame


class SlideBar():
    def __init__(self, x, y, name, base_color, base_color2, screen_size, screen_surface):
        self.screen_surface = screen_surface
        self.bar_size = screen_size
        self.scaled_x = self.bar_size[0] / 100
        self.scaled_y = self.bar_size[1] / 100

        self.bar_lenght = self.scaled_x * 10
        self.bar_thickness = self.scaled_y * 1.5
        self.ball_size = self.scaled_y * 3
        self.text_distance = self.scaled_x * 3


        self.base_color2 = base_color2
        self.clicked = False

        self.bar_edge_surface = pygame.Surface((self.scaled_x, self.scaled_y * 3))
        self.bar_edge_surface.fill(base_color2)
        self.bar_body_surface = pygame.Surface((self.bar_lenght, self.bar_thickness))
        self.bar_body_surface.fill(base_color)

        self.bar_body_rect = self.bar_body_surface.get_rect(center=(x, y))
        self.bar_edge_rect_left = self.bar_edge_surface.get_rect(midright=self.bar_body_rect.midleft)
        self.bar_edge_rect_right = self.bar_edge_surface.get_rect(midleft=self.bar_body_rect.midright)

        self.ball_loc = [self.bar_body_rect.center[0], self.bar_body_rect.center[1]]
        self.name_loc = (self.bar_body_rect.center[0], self.bar_body_rect.center[1] - self.text_distance)
        self.ball = pygame.draw.circle(self.screen_surface, color='blue'
                                       , center=self.ball_loc
                                       , radius=self.ball_size)

        self.font = pygame.font.Font("Foonts\DejaVuSerif-BoldItalic.ttf", 25)
        self.value_font = pygame.font.Font("Foonts\DejaVuSerif-BoldItalic.ttf", 15)
        self.bar_name = name
        self.bar_name_image = self.font.render(self.bar_name, True, base_color)
        self.bar_name_rect = self.bar_name_image.get_rect(center=self.name_loc)

    def get_mouse_pos(self):
        self.pos = pygame.mouse.get_pos()
        return self.pos

    def MouseClicked(self):

        if self.ball.collidepoint(self.get_mouse_pos()) or self.bar_body_rect.collidepoint(self.get_mouse_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked

    def move_ball(self):

        if self.MouseClicked():
            self.ball_loc[0] = self.pos[0]

            # check ball border
            if self.ball_loc[0] <= self.bar_body_rect.left:
                self.ball_loc[0] = self.bar_body_rect.left
            if self.ball_loc[0] >= self.bar_body_rect.right:
                self.ball_loc[0] = self.bar_body_rect.right

    def set_value(self):

        self.value = round(float((self.ball.centerx - self.bar_body_rect.left) * 2 / self.bar_lenght), 1)
        self.value_image = self.value_font.render(str(self.value),True,'black',)
        self.value_rect = self.value_image.get_rect(right=self.bar_edge_rect_left.left,bottom=self.bar_edge_rect_left.bottom)

    def draw_caption(self):

        pygame.draw.rect(self.screen_surface
                         , self.base_color2
                         , self.bar_name_rect
                         , 0, 5)
        self.screen_surface.blit(self.bar_name_image, self.bar_name_rect)
        self.screen_surface.blit(self.value_image, self.value_rect)


    def draw(self):

        # draw the Slide bar
        # pygame.draw.rect(surface, self.current_background_color, self.rect, 0, 5)

        self.screen_surface.blit(self.bar_edge_surface, self.bar_edge_rect_left)
        self.screen_surface.blit(self.bar_edge_surface, self.bar_edge_rect_right)
        self.screen_surface.blit(self.bar_body_surface, self.bar_body_rect)

        # surface.blit(self.ball_surface, self.bar_body_rect)

        self.ball = pygame.draw.circle(self.screen_surface, color='blue'
                                       , center=self.ball_loc
                                       , radius=self.scaled_y*2)

    def reset(self):
        self.ball_loc = [self.bar_body_rect.center[0], self.bar_body_rect.center[1]]

    def update(self):
        self.set_value()
        self.draw_caption()
        self.draw()
        self.move_ball()
        return self.value
