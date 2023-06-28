# imports
import pygame
import tkinter as tk
from tkinter import simpledialog
from ast import literal_eval
from math import sqrt

# file loads
pygame.init()
icon_image = pygame.image.load('images/icon.png')
background_sound = pygame.mixer.Sound('sounds/background_sound.mp3')

# window creation
background_image = pygame.image.load('images/background.jpg')
image_width, image_height = background_image.get_size()
window_width, window_height = image_width, image_height
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Marker')
pygame.display.set_icon(icon_image)

# points options
font = pygame.font.SysFont('arialblack', 14)
save_points_text = font.render('Pressione F10 para Salvar os Pontos', True, (255, 255, 255))
load_points_text = font.render('Pressione F11 para Carregar os Pontos', True, (255, 255, 255))
delete_points_text = font.render('Pressione F12 para Deletar os Pontos', True, (255, 255, 255))


# save stars in .txt file (call by F10)
def save_database(stars_list):
    with open("star_database.txt", "w") as db:
        for star_ in stars_list:
            for key, value in star_.items():
                x, y = value[0], value[1]
                if key == 'name':
                    db.write(f'{value}: ')
                else:
                    db.write(f"({x}, {y})\n")


# load stars reading the "star_database.txt" archive (call by F11)
def load_database():
    stars.clear()
    with open("star_database.txt", "r") as db:
        for line in db:
            line = line.strip()
            if line:
                key, tup = line.split(': ')
                tuple_obj = literal_eval(tup)
                stars.append(
                    {
                        'name': key,
                        'coordinates': tuple_obj
                    }
                )

# calculate and show the distance between the stars as a label above the stars connections
# extra function
def calculate_distance(star1, star2):
    x1, y1 = star1['coordinates']
    x2, y2 = star2['coordinates']
    distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return round(distance, 2)

# main program
if __name__ == "__main__":
    stars = list()
    running = True
    while running:
        pygame.display.update()
        window.blit(background_image, (0, 0))
        window.blit(save_points_text, (5, 0))
        window.blit(load_points_text, (5, 20))
        window.blit(delete_points_text, (5, 40))
        background_sound.set_volume(0.1)
        background_sound.play(-1)

        for i, star in enumerate(stars):
            for k, v in star.items():
                name = star['name']
                coordinate_x, coordinate_y = star['coordinates']
                window.blit(font.render(f'{name}', True, (255, 255, 255)), (coordinate_x, coordinate_y + 2))
                pygame.draw.circle(background_image, (255, 255, 255), (coordinate_x, coordinate_y), 5)
                if len(stars) >= 2:
                    try:
                        coordinate_x, coordinate_y = star['coordinates']
                        next_star_coordinate_x, next_star_coordinate_y = stars[i + 1]['coordinates']
                        distance = calculate_distance(star, stars[i + 1])
                        text = font.render(f'{distance:.2f}', True, (255, 255, 255))
                        text_rect = text.get_rect(center = ((coordinate_x + next_star_coordinate_x) // 2,
                                                           (coordinate_y + next_star_coordinate_y) // 2))
                        window.blit(text, text_rect)
                        pygame.draw.line(background_image, (255, 255, 255), (coordinate_x, coordinate_y),
                                        (next_star_coordinate_x, next_star_coordinate_y))
                    except IndexError:
                        pass
                else:
                    pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                center_x, center_y = pygame.mouse.get_pos()
                star_add = tk.Tk()
                star_add.iconbitmap(default="images/icon.ico")
                star_add.withdraw()
                dialog = simpledialog.askstring('Space', 'Nome da estrela:')
                if dialog is None or dialog == '':
                    name_coordinate = str((center_x, center_y))
                    dialog = 'desconhecido'+f'{name_coordinate}'
                stars.append(
                    {
                        'name': dialog,
                        'coordinates': (center_x, center_y)
                    }
                )
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F10:
                    save_database(stars)
                elif event.key == pygame.K_F11:
                    load_database()
                elif event.key == pygame.K_F12:
                    stars.clear()
                    background_image = pygame.image.load('images/background.jpg')
                    image_width, image_height = background_image.get_size()
                    window_width, window_height = image_width, image_height
                    window = pygame.display.set_mode((window_width, window_height))
                elif event.key == pygame.K_ESCAPE:
                    running = False
            pygame.display.update()
            pygame.display.flip()
    pygame.quit()
