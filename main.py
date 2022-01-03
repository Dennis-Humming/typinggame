import pygame
import sys
import random
import time
import text_box
from difflib import SequenceMatcher


class user():
    name = 'user1'           #用户名
    score = 0                #得分
    correct = 0              #正确个数
    wrong = 0                #错误个数
    correction_rate = 0      #正确率
    error_typing = ''        #错误键入
    gap = []                 #击中时间
    simularity = 0           #文本相似度
    time_use = 0             #总用时


user1 = user

screen = pygame.display.set_mode((1200, 563), 0, 0)

most = 50
#同屏最大字符数
wordstring = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
dictionary = []

section = ["park.txt", "bedroom.txt"]

wordlist = []

xlist = []

ylist = []

score = 0

count = 0

speed = 10

clock = time.time()

background =pygame.image.load("timg.jfif")


def login():
    # 自定义用户名
    global screen, user1
    pygame.font.init()
    font = pygame.font.Font("LeviReBrushed.ttf", 50)
    dic = text_box.text_box(20, 5, 30, 250, 100, font)

    while True:
        screen.blit(background, (0, 0))
        title = font.render("input your username", True, (0, 0, 0))
        confirm = font.render("OK", True, (0, 0, 0))

        screen.blit(title, (300, 20))
        screen.blit(confirm, (1000, 450))
        dic.text_box_paint(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, (1000, 450, 100, 50)):
                    user1.name = dic.text
                    return

            if event.type == pygame.KEYDOWN:
                dic.key_down(event)

        pygame.display.flip()


def menu():
    #主菜单

    pygame.display.set_caption("打字游戏")

    while True:
        screen.blit(background, (0, 0))

        menu_check_mouse()

        paintmenu()

        pygame.time.delay(speed)

        pygame.display.update()


def menu_check_mouse():
    #监听鼠标
    global dictionary
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_rect(event.pos, (550, 80, 240, 100)):
                dictionary = wordstring.split()
                game1()
            elif is_rect(event.pos, (500, 200, 340, 100)):
                game2()
            elif is_rect(event.pos, (500, 320, 340, 100)):
                self_def_mode()


def is_rect(pos, rect):
    #判断点击范围
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
        return True
    return False


def paintmenu():
    #绘制主菜单
    pygame.font.init()
    font = pygame.font.Font("LeviReBrushed.ttf", 100)
    game1_start = font.render("Word", True, (0, 0, 0))
    game2_start = font.render("section", True, (0, 0, 0))
    score_save = font.render("selfdef", True, (0, 0, 0))
    screen.blit(game1_start, (550, 80))
    screen.blit(game2_start, (500, 200))
    screen.blit(score_save, (500, 320))


def game1():
    # 单字游戏总流程
    global clock,score,count
    clock = time.time()
    score = 0
    count = 0
    init_word()

    while True:

        screen.blit(background, (0, 0))

        game1calculate()

        game1paint()

        pygame.time.delay(speed)

        pygame.display.update()


def init_word():
    # 单字游戏单字初始化
    global dictionary
    flag = 0
    while flag < most:
        wordlist.append(0)
        xlist.append(0)
        ylist.append(0)
        flag += 1
    flag = 0
    while flag < most:
        wordlist[flag] = random.choice(dictionary)
        xlist[flag] = random.randint(400, 850)
        ylist[flag] = -50 - flag * 50
        flag += 1


def new_word(num):
    # 生成新单字
    global dictionary

    wordlist[num] = random.choice(dictionary)
    xlist[num] = random.randint(400, 850)
    ylist[num] = min(ylist)-50


def game1calculate():
    #单字游戏算法

    global  score, ord, count, speed, clock, user1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            sys.exit()

        if event.type == pygame.KEYDOWN:
            flag = ylist.index(max(ylist))
            if event.key == ord(wordlist[flag]) + 32 or event.key == ord(wordlist[flag]):
                new_word(flag)
                score += count//5 + 1
                count += 1
                if time.time()-clock < 20 :
                    user1.correct += 1
                    user1.gap.append(round(time.time()-clock, 2))
            else:
                if time.time()-clock < 20 :
                    user1.error_typing += wordlist[flag]
                    user1.wrong += 1

    flag = 0
    while flag < most:
        ylist[flag] += count//5 + 1
        if ylist[flag] > 523:

            file_v = open("game1.txt", "a")
            file_v.write(user1.name)
            file_v.write(" correction rate: ")
            file_v.write(str(round(user1.correct / (user1.correct + user1.wrong), 2)))
            file_v.write(" error typing: ")
            file_v.write(user1.error_typing)
            file_v.write(" error typing rate: ")
            error_typing_rate = {}
            for i in user1.error_typing:
                error_typing_rate[i] = round(user1.error_typing.count(i)/user1.wrong, 2)
            error_typing_rate1 = sorted(error_typing_rate.items(), key=lambda d: d[1], reverse=True)
            for i in range(len(error_typing_rate1)):
                s = str(error_typing_rate1[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
                s = s.replace("'", '').replace(',', '') + ' '  # 去除单引号，逗号，每行末尾追加换行符
                file_v.write(s)

            file_v.write(" hittime: ")
            for i in range(len(user1.gap)):
                s = str(user1.gap[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
                s = s.replace("'", '').replace(',', '') + 's '  # 去除单引号，逗号，每行末尾追加换行符
                file_v.write(s)

            file_v.write("\n")
            file_v.close()
            game1_dead()
        flag += 1


def game1paint():
    #单字游戏绘图

    pygame.font.init()

    font = pygame.font.Font("LeviReBrushed.ttf", 50)

    flag = 0
    while flag < most:
        fontRead = font.render(wordlist[flag], True, (0, 0, 0))
        scoreShow = font.render("score:%s"%score, True, (0, 0, 0))
        screen.blit(fontRead, (xlist[flag], ylist[flag]))
        screen.blit(scoreShow, (20, 20))
        flag += 1


def game2():
    #段落游戏总流程
    pygame.font.init()
    font = pygame.font.Font("LeviReBrushed.ttf", 50)
    global clock, user1, screen
    clock = time.time()
    string = ''
    filename = random.choice(section)
    file = open(filename, "r")
    txt = file.read()
    file.close()
    text = text_box.text_box(40, 5, 30, 400, 250, font)

    while True:
        screen.blit(background, (0, 0))

        if game2_check_mouse(text):
            break

        paint_game2(txt)

        text.text_box_paint(screen)

        pygame.time.delay(speed)

        pygame.display.flip()

    string = text.text
    user1.simularity = SequenceMatcher(None, string, txt).ratio()
    user1.time_use = time.time() - clock
    file_v = open("game2.txt", "a")
    file_v.write(user1.name)
    file_v.write(" simularity: ")
    file_v.write(str(round(user1.simularity, 2)))
    file_v.write(" time used: ")
    file_v.write(str(round(user1.time_use, 2)))
    file_v.write("\n")
    file_v.close()
    game2_dead()


def game2_check_mouse(text):
    #段落游戏鼠标键盘监听函数
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if is_rect(event.pos, (1000, 450, 100, 50)):
                return True
        if event.type == pygame.KEYDOWN:
            text.key_down(event)
    return False


def paint_game2(txt):
    #段落游戏绘制函数
    global clock
    pygame.font.init()
    font = pygame.font.Font("LeviReBrushed.ttf", 50)
    check = font.render("check", True, (0, 0, 0))
    scoreShow = font.render("score:%.2f" % (time.time() - clock), True, (0, 0, 0))
    screen.blit(check, (1000, 450))
    screen.blit(scoreShow, (20, 20))

    font = pygame.font.Font("LeviReBrushed.ttf", 30)
    txt_temp = txt.split('\n')
    height = 10
    for temp in txt_temp:
        tmp = font.render(temp, True, (0, 0, 0))
        screen.blit(tmp, (300, height))
        height += 40


def self_def_mode(form=None):
    #自定义字符集
    global dictionary, wordstring, screen
    pygame.font.init()
    font = pygame.font.Font("LeviReBrushed.ttf", 50)
    dic = text_box.text_box(30, 5, 50, 250, 100, font)

    while True:
        screen.blit(background, (0, 0))
        title = font.render("input your trainning dictionary", True, (0, 0, 0))
        confirm = font.render("OK", True, (0, 0, 0))

        screen.blit(title, (300,20))
        screen.blit(confirm, (1000,450))
        dic.text_box_paint(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, (1000, 450, 100, 50)):
                    dic.text.replace('\n', '')
                    dictionary = dic.text.split(' ')
                    game1()

            if event.type == pygame.KEYDOWN:
                dic.key_down(event)

        pygame.display.flip()


def game1_dead():
    global wordlist,xlist,ylist
    while True:
        pygame.font.init()
        font = pygame.font.Font("LeviReBrushed.ttf", 50)

        replay= font.render("train again", True, (0, 0, 0))
        exit= font.render("exit", True, (0, 0, 0))

        font = pygame.font.Font("LeviReBrushed.ttf", 100)
        scoreShow = font.render("score:%s" % score, True, (0, 0, 0))

        screen.blit(replay, (600, 450))
        screen.blit(exit, (1000, 450))
        screen.blit(scoreShow, (300, 200))

        pygame.time.delay(speed)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, (600, 450, 200, 50)):
                    wordlist = []
                    xlist = []
                    ylist = []
                    menu()
                elif is_rect(event.pos, (1000, 450, 100, 50)):
                    sys.exit()


def game2_dead():
    pygame.font.init()
    global user1
    while True:

        font = pygame.font.Font("LeviReBrushed.ttf", 50)

        replay = font.render("train again", True, (0, 0, 0))
        exit = font.render("exit", True, (0, 0, 0))

        sim = font.render("similarity :  %.2f" %user1.simularity, True, (0, 0, 0))
        timeShow = font.render("time used :  %.2f" %user1.time_use,True, (0, 0, 0))

        screen.blit(replay, (600, 450))
        screen.blit(exit, (1000, 450))
        screen.blit(sim, (300, 100))
        screen.blit(timeShow, (300, 200))

        pygame.time.delay(speed)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_rect(event.pos, (600, 450, 200, 50)):
                    menu()
                elif is_rect(event.pos, (1000, 450, 100, 50)):
                    sys.exit()


if __name__ == '__main__':
    login()
    menu()








