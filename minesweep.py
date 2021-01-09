import pygame as pg
import random as rd
import time

pg.init()

screen = pg.display.set_mode((350, 430))

pg.display.set_caption("minesweep")

running = True

num_font = pg.font.SysFont("Viga",35 ,bold=100)

white = (255,255,255)

pg.key.set_repeat(1, 1)

win_font = pg.font.SysFont("Viga", 150)

text_list = []

bomb = 10

down_button = 0

replay_button = True

win_game = win_font.render("WIN!", True, (255,255,255,128))

color_list = [(0,0,255), (0,128,0), (255,0,0),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124)]

num_light_list =[
    (True, True, True, True, True, True, False),
    (False, False, False, True, True, False, False),
    (True, False, True, True, False, True, True),
    (True, False, False, True, True, True ,True),
    (False, True, False, True, True,False, True),
    (True, True, False, False, True, True, True),
    (True, True, True, False, True, True, True),
    (True, False, False, True, True, False, False),
    (True, True, True, True, True, True, True),
    (True, True, False, True, True, True, True)
]
for a in range(8):
    text_list.append(num_font.render(str(a+1), True, color_list[a]))

def d_block(x1,y1, width, height, center_color, side_gap,ud_gap, flip):
    block_color = [ (128,128,128), white]
    if flip:
        block_color.reverse()
    pg.draw.polygon(screen, block_color[0], [(x1, y1), (x1 + width, y1), (x1, y1 + height)])
    pg.draw.polygon(screen, block_color[1], [(x1 + width, y1), (x1, y1 + height),(x1 + width, y1 + height )])
    pg.draw.rect(screen,  center_color, [ x1 + side_gap,y1 + ud_gap,  width - side_gap*2, height - ud_gap*2])

def set_array():
    global main_array, state_array
    main_array = []
    state_array = []
    for a in range(10):
        state_array.append([1,1,1,1,1,1,1,1,1,1])
        main_array.append([0,0,0,0,0,0,0,0,0,0])
    random = 0
    while not random == bomb:
        random_raw = rd.randint(0,9)
        random_column = rd.randint(0,9)
        if not main_array[random_raw][random_column] == 10:
            main_array[random_raw][random_column] = 10
            random += 1

    for a in range(10):
        for b in range(10):
            #print("[ ", end='')
            around_bomb = 0
            if not main_array[a][b] == 10:
                if not a == 0 and not b == 0:
                    if main_array[a - 1][b - 1] == 10:
                        around_bomb += 1
                        #print("1", end='')

                    # O X X
                    # X X X
                    # X X X 

                if not a == 0:
                    if main_array[a - 1][b] == 10:
                        around_bomb += 1
                        #print("2", end='')

                    # X O X
                    # X X X
                    # X X X 

                if not a == 0 and not b == 9 :
                    if main_array[a - 1][b + 1] == 10:
                        around_bomb += 1
                        #print("3", end='')

                    # X X O
                    # X X X
                    # X X X 

                if not b == 9:
                    if main_array[a][b + 1] == 10:
                        around_bomb += 1
                        #print("4", end='')

                    # X X X
                    # X X O
                    # X X X 

                if not b == 0:
                    if main_array[a][b - 1] == 10:
                        around_bomb += 1
                        #print("5", end='')

                    # X X X
                    # O X X
                    # X X X 

                if not a == 9:
                    if main_array[a + 1][b] == 10:
                        around_bomb += 1
                        #print("6", end='')

                    # X x X
                    # X X X
                    # X O X 

                if not b == 0 and not a == 9:
                    if main_array[a + 1][b - 1] == 10:
                        around_bomb += 1
                        #print("7", end='')

                    # X x X
                    # X X X
                    # O X X 

                if not b == 9 and not a == 9:
                    if main_array[a + 1][b + 1] == 10:
                        around_bomb += 1
                        #print("8", end='')

                    # X x X
                    # X X X
                    # X x O 
                
                #print(" ] ", end='')
                main_array[a][b] = around_bomb
        #print()

def draw_num(x,y,num):
    light = num_light_list[num]


    light_color = (96,0,0)
    if light[0]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x , y, 10,6])
    pg.draw.polygon(screen, light_color, [(x, y), (x - 5, y ), (x, y + 5)])
    pg.draw.polygon(screen, light_color, [(x + 10, y), (x + 15, y ), (x + 10, y + 5)])

    light_color = (96,0,0)
    if light[1]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x - 6 , y + 8, 6,9])
    pg.draw.polygon(screen, light_color, [(x - 6 , y + 8), (x - 1, y + 8 ), (x  - 6, y + 3)])
    pg.draw.polygon(screen, light_color, [(x - 6 , y + 17), (x - 1, y + 17 ), (x - 6, y + 22)])

    light_color = (96,0,0)
    if light[2]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x - 6 , y + 31, 6,9])
    pg.draw.polygon(screen, light_color, [(x - 6 , y + 30), (x - 1, y + 30 ), (x  - 6, y + 24)])
    pg.draw.polygon(screen, light_color, [(x - 6 , y + 40), (x - 1, y + 40 ), (x - 6, y + 45)])

    light_color = (96,0,0)
    if light[3]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x + 12 , y + 8, 6,9])
    pg.draw.polygon(screen, light_color, [(x + 17 , y + 8), (x + 12, y + 8 ), (x  + 17, y + 3)])
    pg.draw.polygon(screen, light_color, [(x + 17 , y + 17), (x + 12, y + 17 ), (x +17, y + 22)])

    light_color = (96,0,0)
    if light[4]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x + 12 , y + 31, 6,9])
    pg.draw.polygon(screen, light_color, [(x + 17 , y + 30), (x + 12, y + 30 ), (x  + 17, y + 24)])
    pg.draw.polygon(screen, light_color, [(x + 17 , y + 40), (x + 12, y + 40 ), (x +17, y + 45)])

    light_color = (96,0,0)
    if light[5]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x + 1 , y + 42, 9,6])
    pg.draw.polygon(screen, light_color, [(x + 1, y + 42), (x - 4, y + 47 ), (x, y + 47)])
    pg.draw.polygon(screen, light_color, [(x + 10, y  +42), (x + 15, y+ 47 ), (x + 10, y + 47)])

    light_color = (96,0,0)
    if light[6]:
        light_color = (255,0,0)

    pg.draw.rect(screen, light_color, [x , y + 20, 11,7])
    pg.draw.polygon(screen, light_color, [(x , y + 20), ( x - 5,y+ 23 ), (x, y + 26)])
    pg.draw.polygon(screen, light_color, [(x + 10 , y + 20), ( x + 15,y+ 23 ), (x + 10, y + 26)])

def game_set():
    global main_array, state_array, gameover, bomb, start_time, start, win, red_block
    bomb = 10
    set_array()
    gameover = False
    start_time = True
    start = 0
    win = False
    red_block = [None, None]

def d_time():
    global now
    if gameover or win:
        for a,num in enumerate(now):
            draw_num(224+a*34,28, int(num))
    else:
        if start == 0:
            for a in range(3):
                draw_num(224+a*34,28, 0)
        else:
            now = round(time.time() - start)
            if int(now) > 999:
                now = 999
            else:
                if int(now) < 10:
                    now = f"00{now}"
                elif int(now) < 100:
                    now = f"0{now}"
                else:
                    now = str(now)
            for a,num in enumerate(now):
                draw_num(224+a*34,28, int(num))

def d_background():
    d_block(0,0,350,500,(192,192,192),4,4,True)
    d_block(20 , 13 , 311 , 80,(198,198,198),5,2, False)

    d_block(20, 100, 310,310,(0,0,0),5,5 ,False)

    d_block(30 , 23 , 110 , 60, (0,0,0),3,3, False)
    d_block(209 , 23 , 110 , 60, (0,0,0),3,3, False)
    d_block(145, 23 , 60,60 ,  (198,198,198),5,5, replay_button)

    pg.draw.circle(screen, (248,253,34), (175,53), 20)
    pg.draw.circle(screen, (0,0,0), (168 , 48), 3)
    pg.draw.circle(screen, (0,0,0), (183 , 48), 3)
    pg.draw.ellipse(screen, (0,0,0), [165,57, 21, 10])
    pg.draw.ellipse(screen, (255,255,0), [165,53, 21, 10])
    
def d_line():
    for a in range(11):
        pg.draw.line(screen, (128,128,128),(55+30*a, 105),(55+30*a, 404),  1)
        pg.draw.line(screen, (128,128,128),(25, 104+30*a),(325, 104+30*a),  1)

def check_win():
    global gameover
    find = 0
    for a in range(100):
            if state_array[a//10][a%10] == 0:
                find += 1
    if 90 == find:
        return True

def d_board(i,j):
    if state_array[i][j] == 0:
        pg.draw.rect(screen, (196,196,196), [25+j*30, 105+i*30, 30,30])
        if not  main_array[i][j] == 0:
            if not main_array[i][j] == 10:
                screen.blit(text_list[main_array[i][j] - 1], (34+j*30, 109+i*30))

    if state_array[i][j] > 0:
        d_block(25+j*30,105+i*30,30,30,(198,198,198), 5,5,True)

    if state_array[i][j] == 2:
        pg.draw.polygon(screen, (255,0,0), [(35+j*30, 122+i*30), (35+j*30, 108 +i*30),(48+j*30, 115+i*30)])
        pg.draw.line(screen, (0,0,0), (34+j*30, 109 +i*30), (34+j*30, 128 +i*30), 3)

def d_all_bomb(i,j):
    if main_array[i][j] == 10:
        if [i,j] == red_block:
            pg.draw.rect(screen, (255,0,0), [25+j*30, 105+i*30, 30,30])
        else:
            pg.draw.rect(screen, (196,196,196), [25+j*30, 105+i*30, 30,30])
        pg.draw.line(screen, (255,0,0),(35+j*30, 120+i*30),(45+j*30, 108+i*30),  2)
        pg.draw.circle(screen, (0,0,0), (40+j*30, 120+i*30), 10)

def update_main_array():
    global gameover, main_array, open_list, state_array, red_block, start, now, bomb
    if main_array[mouse_y][mouse_x] == 10:
        gameover = True
        now = round((time.time() - start))
        if int(now) > 999:
            now = "999"
        else:
            if int(now) < 10:
                now = f"00{now}"
            elif int(now) <  100:
                now = f"0{now}"
            else:
                now = str(now)
        red_block = [mouse_y, mouse_x]

    elif state == 1 or state == 2:
        if state == 2:
            bomb += 1
        if main_array[mouse_y][mouse_x] == 0:
            open_list = [(mouse_y, mouse_x)]         
            
            for a in range(20):
                copy_list = open_list[:]
                for y,x in copy_list:
                    if not x == 0:                                 
                        if main_array[y][x - 1] == 0:
                            open_list.append((y, x - 1))

                    if not x == 9:
                        if main_array[y][x + 1] == 0:
                            open_list.append((y, x + 1))

                    if not y == 9:
                        if main_array[y + 1][x] == 0:
                            open_list.append((y + 1, x))

                    if not y == 0:
                        if main_array[y - 1][x] == 0:    
                            open_list.append((y - 1, x))

                    if not y == 0 and not x == 9:
                        if  main_array[y - 1][x + 1] == 0:
                            open_list.append((y - 1, x + 1))

                    if not y == 0 and not x == 0:
                        if  main_array[y - 1][x - 1] == 0:
                            open_list.append((y - 1, x - 1))

                    if not y == 9 and not x == 9:
                        if  main_array[y + 1][x + 1] == 0:
                            open_list.append((y + 1, x + 1))

                    if not y == 9 and not x == 0:
                        if  main_array[y + 1][x - 1] == 0:
                            open_list.append((y + 1, x - 1))  

                    open_list = list(set(open_list))

                for y,x in open_list:
                    if state_array[y][x] == 2:
                        bomb += 1 
                    state_array[y][x] = 0
                    
                    if not x == 0:
                        if not main_array[y][x - 1] == 0: 
                            if state_array[y][x - 1] == 2:
                                bomb += 1
                            state_array[y][x - 1] = 0
                            
                    if not x == 9:
                        if not main_array[y][x + 1] == 0:
                            if state_array[y][x + 1] == 2:
                                bomb += 1
                            state_array[y][x + 1] = 0
                            
                    if not y == 9:
                        if not main_array[y + 1][x] == 0:
                            if state_array[y + 1][x] == 2:
                                bomb += 1
                            state_array[y + 1][x] = 0
                            
                    if not y == 0:
                        if not main_array[y - 1][x] == 0:
                            if state_array[y - 1][x] == 2:
                                bomb += 1
                            state_array[y - 1][x] = 0

                    if not y == 0 and not x == 9:
                        if not main_array[y - 1][x + 1] == 0:
                            if state_array[y - 1][x + 1] == 2:
                                bomb += 1
                            state_array[y - 1][x + 1] = 0

                    if not y == 0 and not x == 0:
                        if not main_array[y - 1][x - 1] == 0:
                            if state_array[y - 1][x - 1] == 2:
                                bomb += 1
                            state_array[y - 1][x - 1] = 0

                    if not y == 9 and not x == 9:
                        if not main_array[y + 1][x + 1] == 0:
                            if state_array[y + 1][x + 1] == 2:
                                bomb += 1
                            state_array[y + 1][x + 1] = 0

                    if not y == 9 and not x == 0:
                        if not main_array[y + 1][x - 1] == 0:
                            if state_array[y + 1][x - 1] == 2:
                                bomb += 1
                            state_array[y + 1][x - 1] = 0                                
        else:
            state_array[mouse_y][mouse_x] = 0           
        
def show_board():
    print()
    for a in main_array:
        print(a)
    print()

def left_bomb():
    global bomb
    bomb = int(bomb)
    if bomb < 10:
        string_bomb = f"00{bomb}"
    elif bomb < 100:
        string_bomb = f"0{bomb}"
    for a,num in enumerate(str(string_bomb)):
        draw_num(45 + a*34,28, int(num))
    
game_set()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_h:
        #         for i,a in  enumerate(main_array):
        #             for j,b in enumerate(a):
        #                 if not b == 10:
        #                     state_array[i][j] = 0

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos() 
            if mouse_x > 145 and mouse_x < 205 and mouse_y > 23 and mouse_y < 83:
                game_set()
                replay_button = False
                win = False
                down_button = 10
            
            if not win and not gameover:
                if mouse_x > 30 and mouse_x < 325 and mouse_y > 100 and mouse_y < 400:
                    if start_time:
                        start = time.time()
                      
                        start_time = False

                    mouse_x = (mouse_x - 25) // 30
                    mouse_y = (mouse_y - 105) // 30 

                    state = state_array[mouse_y][mouse_x]

                    if event.button == 1:
                        update_main_array()

                    elif event.button == 3:
                        if  not gameover and not win:
                            if state == 2:
                                state_array[mouse_y][mouse_x] = 1
                                bomb += 1
                            else:
                                if bomb > 0:
                                    if state == 1:
                                        state_array[mouse_y][mouse_x] = 2
                                        bomb -= 1

                if check_win():
                    win = True
                    gameover = True
                    now = round((time.time() - start))
                    if int(now) > 999:
                        now = "999"
                    else:
                        if int(now) < 10:
                            now = f"00{now}"
                        elif int(now) <  100:
                            now = f"0{now}"
                        else:
                            now = str(now)
                       
    d_background()

    for i in range(10):
        for j in range(10):

            d_board(i,j)

            if gameover:

                d_all_bomb(i,j)

    d_line()
    d_time()
    left_bomb()
                   
    if win:
        screen.blit(win_game, (58 , 195))
     
    if down_button > 0:
        down_button -= 1
    else:
        replay_button = True

    pg.display.update()

    time.sleep(0.01)
                    