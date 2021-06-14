import pygame
import sys
from adaboost import AlgorithmID3
from dbscan import AlgorithmDBSCAN
from svm import AlgorithmSVM
from knn import AlgorithmKNN
from kmeans import AlgorithmKMEANS
from linear_regression import AlgorithmLR

class Instructions:
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 560

    RIGHT = 1
    MIDDLE = 2
    LEFT = 3

    RED = (255, 0, 0)
    BLUE = (55, 55, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    WHITE = (255, 255, 255)
    LIGHTGREY = (210, 210, 210)

    TITLE = "Instructions"

    display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pixel_points = []
    pixel_points_green = []
    pixel_points_red = []

    button_back = pygame.Rect(0, 510, 240, 60)  # left #top #width #height
    button_start = pygame.Rect(240, 510, 240, 60)  # left #top #width #height

    all = pygame.Rect(40, 220, 400, 468)
    # pygame.draw.rect(window, LIGHTGREY, all)
    intermediate = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT + SCREEN_HEIGHT * 1/2))
    text_window = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_WIDTH))

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.window.fill(self.WHITE)
        self.text_window.fill(self.BLACK)
        self.intermediate.fill(self.WHITE)

    def draw_text(self, window, text, color, size, x, y):
        font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
        text_obj = font_draw.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        window.blit(text_obj, text_rect)

    def draw_instr(self, my_string):
        scroll_y = 0
        self.initialize_game()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        scroll_y = min(scroll_y + 15, 0)
                    if event.button == 5:
                        scroll_y = max(scroll_y - 15, -100)
                    if self.button_back.collidepoint(pygame.mouse.get_pos()):
                        return
                    if self.button_start.collidepoint(pygame.mouse.get_pos()):
                        eval(f'Algorithm{my_string.upper()}().main()')
            self.window.blit(self.text_window, (0, 0))
            self.text_window.blit(self.intermediate, (0, scroll_y))

            self.draw_text(self.intermediate, 'Instructions', self.BLACK, 20, 240, 50)
            self.draw_text(self.intermediate, 'Algorithm explained', self.BLACK, 20, 240, 200)
            pygame.draw.rect(self.window, self.LIGHTGREY, self.button_back)
            pygame.draw.rect(self.window, self.LIGHTGREY, self.button_start)
            pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
            pygame.draw.line(self.window, self.BLACK, (238, 510), (238, 558), 2)

            self.draw_text(self.window, 'Back', self.BLACK, 20, 118, 534)
            self.draw_text(self.window, 'Start', self.BLACK, 20, 358, 534)
            with open(f'instructions/{my_string}', 'r') as f:
                string_instr = f.read()
            my_font = pygame.font.Font(None, 22)
            rendered_text = self.render_textrect(string_instr, my_font, self.all, self.BLACK, self.WHITE, 1)
            if rendered_text:
                self.intermediate.blit(rendered_text, self.all.topleft)
            # pygame.draw.rect(window, LIGHTGREY, all)
            # clock.tick(60)
            # why.fill(GREEN)
            pygame.display.update()

    def render_textrect(self, string, font, rect, text_color, background_color, justification=0):
        final_lines = []
        requested_lines = string.splitlines()

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

                # Let's try to write the text out on the surface.

        surface = pygame.Surface(rect.size)
        surface.fill(background_color)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException("Invalid justification argument: " + str(justification))
            accumulated_height += font.size(line)[1]

        return surface

if __name__ == "__main__":
    Instructions().draw_instr('id3')

class TextRectException(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message
