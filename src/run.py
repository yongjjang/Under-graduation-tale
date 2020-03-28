import pygame
import os
from src.undergraduate import Undergraduate
from src.pygame_textinput import *
from src.report import *
from src.save_load import *


EASY = 3
NORMAL = 6
HARD = 9

WIDTH, HEIGHT = 1920, 1080
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60  # Frames per second.
IS_INTRO: bool = True
IS_END: bool = False
IS_RUNNING: bool = False
USER_VARIABLE = False

WORD_QUANTITY = 3
REFRESH_TIME = 4

pressed_left = False
pressed_right = False
pressed_up = False
pressed_down = False

pygame.init()
pygame.mixer.init(frequency=44100, buffer=2048, channels=2)
pygame.font.init()

clock = pygame.time.Clock()

init_image = []
for i in range(4):
    init_image.append(pygame.image.load('../image/init/init{0}.png'.format(i)))

fun_report_image = []
for i in range(6):
    fun_report_image.append(pygame.image.load('../image/fun_report/fun_report{0}.png'.format(i)))

type_sound = pygame.mixer.Sound("../bgm/typing.wav")
short_type_sound = pygame.mixer.Sound("../bgm/short_typing.wav")
bird_sound = pygame.mixer.Sound("../bgm/bird.wav")
bgm = pygame.mixer.Sound("../bgm/megalovania.wav")
end_sound = pygame.mixer.Sound("../bgm/determination.wav")

type_sound.stop()
short_type_sound.stop()
bird_sound.stop()
bgm.stop()
end_sound.stop()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Under(graduate)tale")

font_eng = pygame.font.Font("../font/DTM-Sans.otf", 50)
title_text = font_eng.render("Under(graduate)tale", True, WHITE)

font_kor = pygame.font.Font("../font/윤디자인웹돋움.ttf", 50)

my = Undergraduate("NoName")

report_data = ReportData()
text_input = TextInput()
text_input.set_text_color(WHITE)
text_input.set_cursor_color(WHITE)

report_list = pygame.sprite.Group()

current_time = pygame.time.get_ticks()

hp_image = pygame.transform.scale(pygame.image.load("../image/me.png").convert_alpha(), (60, 60))


def display_text(seed_text):
    text = ""
    type_sound.play()
    for i in range(len(seed_text)):
        pygame.time.wait(200)
        text = text + seed_text[i]
        guide_text = font_kor.render(text, True, WHITE)
        screen.blit(guide_text, (WIDTH / 5 * 1, HEIGHT / 5 * 4))
        pygame.display.update()
    type_sound.stop()
    pygame.time.wait(1000)


def init_game():
    global IS_INTRO, my
    feel_text = "당신은 끔찍한 과제를 하게 될 것만 같은 예감이 든다."
    bird_sound.play()

    for image in init_image:
        screen.blit(image, (0, 0))
        pygame.display.update()
        pygame.time.wait(4000)
    bird_sound.stop()

    for image in fun_report_image:
        screen.blit(image, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)
    pygame.time.wait(1500)

    screen.fill(BLACK)
    pygame.display.update()

    display_text(feel_text)

    screen.fill(BLACK)
    pygame.display.update()

    display_text("이름을 입력하세요.")
    IS_INTRO = False


def init_user():
    global my, USER_VARIABLE

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:  # check for key presses
            short_type_sound.play()
            if event.key == pygame.K_RETURN:
                user_name = text_input.get_text()
                if os.path.exists('{0}_data.pickle'.format(user_name)):
                    my = load(user_name)
                else:
                    my = Undergraduate(user_name)
                text_input.clear_text()
                USER_VARIABLE = True

    text_input.update(events)
    screen.blit(text_input.get_surface(), (WIDTH / 2 - 100, HEIGHT / 5 * 3))
    pygame.display.update()


def end_game():
    global IS_END, my
    cheer_up_text = "힘을 내 {0}..! 졸업해야지!! 다시 한 번 팀원들에게 카톡 해보자...".format(my.name)
    if not IS_END:
        bgm.stop()
        end_sound.play()
        IS_END = True

    my.hp = 5
    my.total_score += my.score
    save(my)
    print("save ok")
    display_text(cheer_up_text)
    pygame.time.wait(2000)


def run_game():
    global current_time, IS_RUNNING

    if not IS_RUNNING:
        bgm.play(loops=1)
        IS_RUNNING = True

    seconds = (pygame.time.get_ticks() - current_time) / 1000

    if seconds > REFRESH_TIME:
        for i in range(EASY):
            report = Report(report_data.get_data(), font_eng, WIDTH, HEIGHT)
            report_list.add(report)
            current_time = pygame.time.get_ticks()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            quit()

        elif event.type == pygame.KEYDOWN:  # check for key presses
            short_type_sound.play()
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_RETURN:
                for elem in report_list:
                    if text_input.get_text() == elem.report:
                        report_list.remove(elem)
                        my.plus_score(100)
                text_input.clear_text()
            if event.key == pygame.K_LEFT:
                my.damage()
            if event.key == pygame.K_RIGHT:
                my.plus_score(100)

    report_list.update()

    report_list.draw(screen)

    screen.fill(BLACK)
    score_text = "Score : " + str(my.score)
    score_text = font_eng.render(score_text, True, WHITE)
    screen.blit(score_text, (WIDTH / 6 * 5, 20))
    screen.blit(title_text, (WIDTH / 5 * 2, 20))

    for report in report_list:
        if report.y >= HEIGHT:
            my.damage()
            report_list.remove(report)
        screen.blit(report.label, (report.x, report.y))

    for hp in range(my.hp):
        screen.blit(pygame.transform.scale(hp_image, (60, 60)), (WIDTH / 2 - 120 + hp * 80, HEIGHT / 5 * 4))

    text_input.update(events)

    screen.blit(text_input.get_surface(), (WIDTH / 2 - 100, HEIGHT / 5 * 3))

    dead_line = pygame.draw.rect(screen, RED, [0, HEIGHT-20, WIDTH, 20])

    pygame.display.update()


if __name__ == "__main__":
    while True:
        clock.tick(FPS)

        if IS_INTRO:
            init_game()

        if my.hp <= 0:
            end_game()
            break
        elif not USER_VARIABLE:
            init_user()
        else:
            run_game()
