# import menu as menu
#
# while menu.running:
#     menu.display_menu()
#     menu.game_loop()

# import pygame
# import sys
# from pygame import *
#
# pygame.init()
# width, height = 900, 500
# mid_weight, mid_height = width/2, height/2
# up_key, down_key, start_key, back_key = False, False, False, False
# display = pygame.Surface((width, height))
# window = pygame.display.set_mode((width, height))
# pygame.display.set_caption("First game!")
# white, blue, green, red, black = (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
# FPS = 60
# #font = pygame.font.SysFont(None, 20)
# font_name = pygame.font.get_default_font()
# click, run, play = False, True, False
# cursor_rect = pygame.Rect(0, 0, 20, 20)
# offset = -100
# #welcome = font.render('Welcome to Game&Learn!', True, blue)
#
#
# def draw_text(text, color, size, x, y):
#     font_draw = pygame.font.Font(font_name, size)
#     text_obj = font_draw.render(text, True, color)
#     text_rect = text_obj.get_rect()
#     text_rect.center = (x, y)
#     display.blit(text_obj, text_rect)
#
#
# def check_events():
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#         if event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 pygame.quit()
#                 sys.exit()
#             if event.key == K_RETURN:
#                 start_key = True
#         if event.type == K_BACKSPACE:
#             back_key = True
#         if event.type == K_DOWN:
#             down_key = True
#         if event.type == K_UP:
#             up_key = True
#         if event.type == MOUSEBUTTONDOWN:
#             if event.button == 1:
#                 click = True
#
#
# def reset_keys():
#     up_key, down_key, start_key, back_key = False, False, False, False
#
# def game_loop():
#     while play:
#         check_events()
#         if start_key:
#             play = False
#         display.fill(black)
#         draw_text('Thanks for playing!', white, 20, mid_weight, mid_height)
#         window.blit(display, (0, 0))
#         pygame.display.update()
#         reset_keys()
#
# def game_1():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         window.fill(white)
#         draw_text('game', white, 10, 20, 20)
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     run = False
#         pygame.display.update()
#
#
# def game1_1():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         window.fill(white)
#         draw_text('game', white, 10, 20, 20)
#         clock.tick(FPS)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     run = False
#         pygame.display.update()
#
#
# def game_2():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         window.fill(white)
#         clock.tick(FPS)
#         draw_text('game', white, 10, 20, 20)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     run = False
#         pygame.display.update()
#
#
# def game_3():
#     clock = pygame.time.Clock()
#     run = True
#     while run:
#         window.fill(white)
#         clock.tick(FPS)
#         draw_text('game', white, 10, 20, 20)
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     run = False
#         pygame.display.update()
#
#
# def draw_cursor():
#     draw_text('*', white, 15, cursor_rect.x, cursor_rect.y)
#
# def blit_screen():
#     window.blit(display, (0, 0))
#     pygame.display.update()
#     reset_keys()
#
# def move_cursor():
#     if down_key:
#         if state == 'First':
#             cursor_rect.midtop(second_gx + offset, second_gy)
#             state = 'Second'
#         elif state == 'Second':
#             cursor_rect.midtop(third_gx + offset, third_gy)
#             state = 'Third'
#         elif state == 'Third':
#             cursor_rect.midtop(first_gx + offset, first_gy)
#             state = 'First'
#     if up_key:
#         if state == 'First':
#             cursor_rect.midtop(third_gx + offset, third_gy)
#             state = 'Third'
#         elif state == 'Second':
#             cursor_rect.midtop(first_gx + offset, first_gy)
#             state = 'First'
#         elif state == 'Third':
#             cursor_rect.midtop(second_gx + offset, second_gy)
#             state = 'Second'
#
# def check_input():
#     move_cursor()
#     if start_key:
#         if state == 'First':
#             play = True
#         elif state == 'Second':
#             pass
#         elif state == 'Third':
#             pass
#
# def display_menu():
#     run_display = True
#     state = "First"
#     first_gx, first_gy = mid_weight, mid_height + 30
#     second_gx, second_gy = mid_weight, mid_height + 50
#     third_gx, third_gy = mid_weight, mid_height + 70
#     cursor_rect.midtop = (first_gx + offset, first_gy)
#     while run_display:
#         check_events()
#         check_input()
#         window.fill(black)
#         draw_text('Welcome to Game&Learn!', white, 20, mid_weight, mid_height - 20)
#         draw_text('First game', white, 20, first_gx, first_gy)
#         draw_text('Second game', white, 20, second_gx, second_gy)
#         draw_text('Third game', white, 20, third_gx, third_gy)
#         draw_cursor()
#         blit_screen()
#
# def main():
#     clock = pygame.time.Clock()
#
#     run = True
#     while run:
#         game_loop()
#         clock.tick(FPS)
#         mx, my = pygame.mouse.get_pos()
#         button_1 = pygame.Rect(350, 100, 200, 50)
#         button_2 = pygame.Rect(350, 200, 200, 50)
#         button_3 = pygame.Rect(350, 300, 200, 50)
#
#         if button_1.collidepoint((mx, my)):
#             if click:
#                 game_1()
#         if button_2.collidepoint((mx, my)):
#             if click:
#                 game_2()
#         if button_3.collidepoint((mx, my)):
#             if click:
#                 game_3()
#
#         pygame.draw.rect(window, green, button_1)
#         pygame.draw.rect(window, green, button_2)
#         pygame.draw.rect(window, green, button_3)
#
#         click = False
#         check_events()
#         pygame.display.update()
#
#
# if __name__ == '__main__':
#     main()
