#pip install pygame
import pygame as pg
import serial
import sys,os

pg.init()
ser = serial.Serial('COM4', 38400)

size = [400,300]
screen = pg.display.set_mode(size)
pg.display.set_caption("Hit the ball")
done = False
clock = pg.time.Clock()

BLACK= ( 0,  0,  0)
WHITE= (255,255,255)
BLUE = ( 0,  0,255)
GREEN= ( 0,255,  0)
RED  = (255,  0,  0)

x1 = 200
y1 = 150
x2 = 200
y2 = 300

chance = 10
score = 0
hit = False
ready = True
stick_color = GREEN

line_list = [[0,10],[-100,10],[-200,10],[-300,10]]
boom_list = [False,False,False,False]
while not done:
    #시리얼통신 값 받아오기
    if ser.readable():
        val = ser.readline()
        val = val.decode("cp949")[:len(val)-3]
        val = val.split(',')
        val = int(float(val[1])*6000)

    #60프레임으로 제한    
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    #막대기와 공의 움직임 제어
    if(y2-50-val >= 200):
        ready = True
        stick_color = GREEN
    if(y2-50-val <= y1+5 and ready):
        hit = True
        ready = False
        stick_color = RED
    if(hit):
        y1-=10
    if(y1 < -100):
        k=0
        x1 = 200
        y1 = 150
        x2 = 200
        y2 = 300
        hit = False

    screen.fill(WHITE)#배경
    for idx,x in enumerate(line_list):
        if(x[0] > 400):
            chance-=1
            x[0]=0
            boom_list[idx] = False
        if(x1>x[0] and x1<x[0]+20 and y1 == x[1] and boom_list[idx]==False):
            boom_list[idx] = True
            score += 1
        if(boom_list[idx] == False and chance > 0):
            pg.draw.line(screen, BLACK, x, [x[0]+20,x[1]], 5)#맞출 막대기 그리기
        x[0]=x[0]+1
    if(chance < 0):
        chance = 0
    a = pg.draw.circle(screen,BLUE,(x1,y1),5,2)#공
    pg.draw.line(screen, stick_color, [x2,y2-val], [x2,y2-50-val], 5)#막대기
    font = pg.font.Font(None,30)  #폰트 설정
    text1 = font.render("Chance : "+str(chance),True,(28,0,0))  #텍스트가 표시된 Surface 를 만듬
    screen.blit(text1,(0,250))              #화면에 표시
    text2 = font.render("Score : "+str(score),True,(28,0,0))  #텍스트가 표시된 Surface 를 만듬
    screen.blit(text2,(0,280))              #화면에 표시

    pg.display.flip()
sys.exit()
