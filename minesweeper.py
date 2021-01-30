import pygame as pg
import random as rd
import time
import sys

pg.init()

if len(sys.argv) > 1:
    row = int(sys.argv[1])
    if row < 10:
        row = 10
    if row > 30:
        row = 30
else:
    row = 10

if len(sys.argv) > 2:
    column = int(sys.argv[2])
    if column < 10:
        column = 10
    elif column > 30:
        column = 30
else:
    column = 10

if len(sys.argv) > 3:
    all_bomb = int(sys.argv[3])
    if all_bomb > row*column-1:
        all_bomb = row*column-1
else:
    all_bomb = 10

screen = pg.display.set_mode((50+row*30, 130+column*30))
pg.display.set_caption("minesweeper")

try:
    load_image = pg.image.load("mine.png")
    icon_image = pg.transform.scale(load_image, (32, 32))
    mine_image = pg.transform.scale(load_image, (22, 22))
    pg.display.set_icon(icon_image)
    load_mine = True
except :
    load_mine = False

num_font = pg.font.SysFont("Viga",35 ,bold=100)

white = (255,255,255)

pg.key.set_repeat(1, 1)

down_button = 0

running = True
replay_button = True

win_game = pg.font.SysFont("Viga", 150).render("WIN!", True, (255,255,255,128))

color_list = [(0,0,255), (0,128,0), (255,0,0),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124)]

index_list = [(0, - 1), (0,  1), (1, 0), ( -1, 0), (-1, 1), (- 1, - 1), (1,1), (1, -1)]

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
text_list = []

for a in range(8):
    text_list.append(num_font.render(str(a+1), True,color_list[a]))

def d_block(x1,y1, width, height, center_color, side_gap,ud_gap, flip):
    block_color = [ (128,128,128), white]
    if flip:
        block_color.reverse()
    pg.draw.polygon(screen, block_color[0], [(x1, y1), (x1 + width, y1), (x1, y1 + height)])
    pg.draw.polygon(screen, block_color[1], [(x1 + width, y1), (x1, y1 + height),(x1 + width, y1 + height )])
    pg.draw.rect(screen,  center_color, [ x1 + side_gap,y1 + ud_gap,  width - side_gap*2, height - ud_gap*2])

def set_array():
    global main_array, state_array
    state_array = [[1 for a in range(row)] for b in range(column)]
    main_array =  [[0 for a in range(row)] for b in range(column)] 


    random = 0
    while not random == all_bomb:
        random_raw = rd.randint(0,column-1)
        random_column = rd.randint(0,row-1)
        if not main_array[random_raw][random_column] == 10:
            main_array[random_raw][random_column] = 10
            random += 1
    for y in range(column):
        for x in range(row):

            around_bomb = 0
            if not main_array[y][x] == 10:
                check_list = [ x != 0, x !=row-1, y != column-1, y != 0, y != 0 and x != row-1, y != 0 and x != 0, y != column-1 and x != row-1, y != column-1 and x != 0]
                for check, index in zip(check_list, index_list):
                    if check:
                        if main_array[y + index[0]][x + index[1]] == 10:
                            around_bomb += 1

                main_array[y][x] = around_bomb

def change_color(index):
    global light_color
    light_color = (96,0,0)
    if light[index]:
        light_color = (255,0,0)

def draw_num(x,y,num):
    global light_color, light
    
    light = num_light_list[num]

    num_xy_list =[
        (0,0,10,6,0,0,  -5, 0, 0, 5, 10, 0, 15,0, 10, 5),
        ( -6,8,6,9,-6,8,-1,8,-6,3,-6,17,-1,17,-6,22), 
        (-6,31,6,9,-6,30,-1,30,-6,24,-6,40,-1,40,-6,45),
        (12,8,6,9,17,8,12,8,17,3,17,17,12,17,17,22),
        (12,31,6,9,17,30,12,30,17,24,17,40,12,40,17,45),
        (1,42,9,6,1,42,-4,47,0,47,10,42,15,47,10,47),
        (0,20,11,7,0,20,-5,23,0,26,10,20,15,23,10,26),
    ]
    for num in range(7):
        change_color(num)
        xy_list = num_xy_list[num]
        pg.draw.rect(screen, light_color, [x + xy_list[0] , y + xy_list[1], xy_list[2],xy_list[3]])
        pg.draw.polygon(screen, light_color, [(x + xy_list[4], y + xy_list[5]), (x + xy_list[6], y + xy_list[7] ), (x + xy_list[8], y + xy_list[9])])
        pg.draw.polygon(screen, light_color, [(x + xy_list[10],y + xy_list[11]), (x  + xy_list[12], y+ xy_list[13] ), (x + xy_list[14], y + xy_list[15])])

def game_set():
    global main_array, state_array, gameover, bomb, start_time, start, win, red_block
    bomb = all_bomb
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
            draw_num(-76+30*row+a*34,28, int(num))
    else:
        if start == 0:
            for a in range(3):
                draw_num(-76+30*row+a*34,28, 0)
        else:
            now = round(time.time() - start)
            if int(now) > 999:
                now = "999"
            else:
                if int(now) < 10:
                    now = f"00{now}"
                elif int(now) < 100:
                    now = f"0{now}"
                else:
                    now = str(now)
            for a,num in enumerate(now):
                draw_num(-76+30*row+a*34,28, int(num))

def d_background():
    d_block(0,0,50+30*row,130+30*column,(192,192,192),4,4,True)
    d_block(20 , 13 , 11+30*row , 80,(198,198,198),5,2, False) # 점수판

    d_block(20, 100, 10+30*row,10+30*column,(0,0,0),5,5 ,False)

    d_block(30 , 23 , 110 , 60, (0,0,0),3,3, False)
    d_block( -91+30*row , 23 , 110 , 60, (0,0,0),3,3, False)

    d_block(-5+15*row, 23 , 60,60 ,  (198,198,198),5,5, replay_button)

    pg.draw.circle(screen, (248,253,34), (25+15*row,53), 20)
    
    if not gameover and not win:
        pg.draw.circle(screen, (0,0,0), (18+15*row , 48), 3)
        pg.draw.circle(screen, (0,0,0), (33+15*row , 48), 3)
        pg.draw.ellipse(screen, (0,0,0), [15+15*row,57, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [15+15*row,53, 21, 10]) 
    elif gameover and not win:
        pg.draw.line(screen, (0,0,0),(15+15*row, 45), (20+15*row, 50) ,3)
        pg.draw.line(screen, (0,0,0),(20+15*row, 45), (15+15*row, 50) ,3)
        pg.draw.line(screen, (0,0,0),(30+15*row, 45), (35+15*row, 50) ,3)
        pg.draw.line(screen, (0,0,0),(35+15*row, 45), (30+15*row, 50) ,3)
        pg.draw.ellipse(screen, (0,0,0), [15+15*row,59, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [15+15*row,63, 21, 10])
    else:
        pg.draw.rect(screen, (0,0,0), [13+15*row, 44, 9, 7])
        pg.draw.rect(screen, (0,0,0), [28+15*row, 44, 9, 7])
        pg.draw.line(screen, (0,0,0),(13+15*row, 46), (35+15*row, 46) ,2)
        pg.draw.line(screen, (0,0,0),(13+15*row, 46), (7+15*row, 43) ,2)
        pg.draw.line(screen, (0,0,0),(37+15*row, 46), (42+15*row, 43) ,2)
        pg.draw.ellipse(screen, (0,0,0), [15+15*row,57, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [15+15*row,53, 21, 10]) 
    
def d_line():
    for x in range(row):
        pg.draw.line(screen, (128,128,128),(55+30*x, 105),(55+30*x, 104+30*column),  1)
    for y in range(column):
        pg.draw.line(screen, (128,128,128),(25, 104+30*y),(25+30*row, 104+30*y),  1)

def check_win():
    find = 0
    for y in range(column):
        for x in range(row):
            if state_array[y][x] == 0:
                find += 1
    if (row*column - all_bomb) == find:
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
        pg.draw.line(screen, (0,0,0), (34+j*30, 108 +i*30), (34+j*30, 128 +i*30), 3)

def d_all_bomb(i,j):
    if main_array[i][j] == 10:
        if (i, j) in red_block:
            pg.draw.rect(screen, (255,0,0), [25+j*30, 105+i*30, 30,30])
        else:
            pg.draw.rect(screen, (196,196,196), [25+j*30, 105+i*30, 30,30])
        if load_mine:
            screen.blit(mine_image, (29+j*30, 107+i*30))
        else:
            pg.draw.line(screen, (255,0,0),(35+j*30, 120+i*30),(45+j*30, 108+i*30),  2)
            pg.draw.circle(screen, (0,0,0), (40+j*30, 120+i*30), 10)

def die(red_block_list):
    global gameover, main_array, open_list, state_array, red_block, start, now, bomb
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
    red_block =red_block_list

def update_main_array():
    global gameover, main_array, open_list, state_array, red_block, start, now, bomb
    if main_array[mouse_y][mouse_x] == 10:
        die([(mouse_y ,mouse_x)])

    elif state == 0:
        if main_array[mouse_y][mouse_x] != 0:
            check_list = [ mouse_x != 0, mouse_x !=row-1, mouse_y != column-1, mouse_y != 0, mouse_y != 0 and mouse_x != row-1, mouse_y != 0 and mouse_x != 0, mouse_y != column-1 and mouse_x != row-1, mouse_y != column-1 and mouse_x != 0]
            around_flag = 0
            for (index_y, index_x), check in zip(index_list, check_list):
                if check:
                    if state_array[mouse_y + index_y][mouse_x + index_x] == 2:
                        around_flag+=1

            if around_flag == main_array[mouse_y][mouse_x]:
                red_block_list = []
            
                for (index_y, index_x), check in zip(index_list, check_list):
                    if check:
                        if main_array[mouse_y + index_y][mouse_x + index_x] == 10:
                            if state_array[mouse_y + index_y][mouse_x + index_x] != 2:
                                red_block_list.append((mouse_y + index_y, mouse_x + index_x))
                        elif main_array[mouse_y + index_y][mouse_x + index_x] == 0:
                            open_list = [(mouse_y+ index_y, mouse_x+ index_x)]         
                            for a in range(20):
                                copy_list = open_list[:]
                                for y,x in copy_list: 
                                    check_list = [ x != 0, x !=row-1, y != column-1, y != 0, y != 0 and x != row-1, y != 0 and x != 0, y != column-1 and x != row-1, y != column-1 and x != 0]
                                    for check,index in zip(check_list, index_list):
                                        if check:
                                            if main_array[y + index[0]][x + index[1]] == 0:
                                                open_list.append((y + index[0], x + index[1])) 

                                    open_list = list(set(open_list))

                            for y,x in open_list:
                                if state_array[y][x] == 2:
                                    bomb += 1 
                                state_array[y][x] = 0

                                check_list = [ x != 0, x !=row-1, y != column-1, y != 0, y != 0 and x != row-1, y != 0 and x != 0, y != column-1 and x != row-1, y != column-1 and x != 0]

                                for check, index in zip(check_list, index_list):
                                    if check:
                                        if not main_array[y + index[0]][x + index[1]] == 0:
                                            if state_array[y + index[0]][x + index[1]] == 2:
                                                bomb += 1
                                            state_array[y + index[0]][x + index[1]] = 0


                        else:
                            if state_array[mouse_y + index_y][mouse_x + index_x] != 2:
                                state_array[mouse_y +index_y][mouse_x + index_x] = 0

                if red_block_list != []:
                    die(red_block_list)

    elif state == 1 or state == 2:
        if state == 2:
            bomb += 1
        if main_array[mouse_y][mouse_x] == 0:
            open_list = [(mouse_y, mouse_x)]         
            for a in range(20):
                copy_list = open_list[:]
                for y,x in copy_list: 
                    check_list = [ x != 0, x !=row-1, y != column-1, y != 0, y != 0 and x != row-1, y != 0 and x != 0, y != column-1 and x != row-1, y != column-1 and x != 0]
                    for check,index in zip(check_list, index_list):
                        if check:
                            if main_array[y + index[0]][x + index[1]] == 0:
                                open_list.append((y + index[0], x + index[1])) 

                    open_list = list(set(open_list))

            for y,x in open_list:
                if state_array[y][x] == 2:
                    bomb += 1 
                state_array[y][x] = 0

                check_list = [ x != 0, x !=row-1, y != column-1, y != 0, y != 0 and x != row-1, y != 0 and x != 0, y != column-1 and x != row-1, y != column-1 and x != 0]

                for check, index in zip(check_list, index_list):
                    if check:
                        if not main_array[y + index[0]][x + index[1]] == 0:
                            if state_array[y + index[0]][x + index[1]] == 2:
                                bomb += 1
                            state_array[y + index[0]][x + index[1]] = 0
                                                  
        else:
            state_array[mouse_y][mouse_x] = 0           

def left_bomb():
    global bomb
    bomb = int(bomb)
    if bomb < 10:
        string_bomb = f"00{bomb}"
    elif bomb < 100:
        string_bomb = f"0{bomb}"
    else:
        string_bomb = str(bomb)
    for a,num in enumerate(str(string_bomb)):
        draw_num(45 + a*34,28, int(num))
    
game_set()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos() 
            if mouse_x > row*15 and mouse_x < 95+row*15 and mouse_y > 23 and mouse_y < 83:
                game_set()
                replay_button = False
                win = False
                down_button = 10
            
            if not win and not gameover:
                if mouse_x > 32 and mouse_x < 25+30*row and mouse_y > 107 and mouse_y < 104+30*column:
                    if start_time:
                        start = time.time()
                      
                        start_time = False

                    mouse_x, mouse_y = (mouse_x - 25) // 30 ,(mouse_y - 105) // 30

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
                    bomb = 0
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

    for i in range(column):
        for j in range(row):

            d_board(i,j)

            if gameover:

                d_all_bomb(i,j)

    d_line()
    d_time()
    left_bomb()
                   
    if win:
        screen.blit(win_game, (-92+15*row , 35+15*column))
     
    if down_button > 0:
        down_button -= 1
    else:
        replay_button = True

    pg.display.update()

    time.sleep(0.01)
