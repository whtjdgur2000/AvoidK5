import pygame
from pygame.locals import *
import math
import random

#게임초기화
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('폭주족 피하기')

#bgm
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
FPS = 60
fpsClock = pygame.time.Clock()
playerpos=[100,100] #처음 플레이어위치
badguys=[[640,100]] #적 들의 좌표 리스트
badtimer=100 #적 생성 타이머. 0이 되면 적 생성
badtimer1=0 #이 값만큼 badtimer 값을 줄인다.
healthvalue =194
keys = [False, False, False, False]# 키 입력 체크

 
#사진파일
player = pygame.image.load("car.png")
road = pygame.image.load("road.png")
emptyhole = pygame.image.load("emptyhole.png")
k5 = pygame.image.load("k5.png")
timebar = pygame.image.load("timebar.png")
time = pygame.image.load("time.png")
gameover = pygame.image.load("gameover.png")
youwin = pygame.image.load("youwin.png")

# 무한 루프
running = 1 #게임 진행 여부 체크
exitcode = 0 #승리 / 패배 체크
exitcode = 2
while running:
    badtimer-=1
    #화면 준비
    screen.fill(0)

    #도로
    for x in range( int(width/road.get_width()) ):
        for y in range( int(height/road.get_height()) ):
            screen.blit(road,(x*100,y*100))

    #플레이어를 (100, 100)에 배치
    screen.blit(player, playerpos)

    #빈공간 배치
    screen.blit(emptyhole,(0,30))
    screen.blit(emptyhole,(0,135))
    screen.blit(emptyhole,(0,240))
    screen.blit(emptyhole,(0,345))

    #적 생성
    if badtimer==0:
        badguys.append([640, random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5

    #적이 빈공간으로 가면 제거
    index=0
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=7
        playerect=pygame.Rect(player.get_rect())
        badrect=pygame.Rect(k5.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        index1=0

        #충돌체크
        if playerect.colliderect(badrect):
            running=0
            exitcode=0
            if exitcode==0:
                screen.blit(gameover,(0,0))
        
        #다음 적    
        index+=1    

    #적 그리기
    for badguy in badguys:
        screen.blit(k5, badguy)
        
    #시간 게이지
    screen.blit(timebar, (5,5))
    for time1 in range(healthvalue):
        screen.blit(time, (time1+8,8))

    #화면 업데이트
    pygame.display.update()
    fpsClock.tick(FPS)

    #발생한 이벤트들을 가져와 처리하는 루프
    for event in pygame.event.get():

        #x 버튼을 클릭하여 종료하려고 하면
        if event.type==pygame.QUIT:
            #pygame 라이브러리 종료 후 프로그램 종료
            pygame.quit() 
            exit(0)

        #키를 누르면
        if event.type == pygame.KEYDOWN:
            if event.key==K_UP:
                keys[0]=True
            elif event.key==K_LEFT:
                keys[1]=True
            elif event.key==K_DOWN:
                keys[2]=True
            elif event.key==K_RIGHT:
                keys[3]=True

        #키를 떼면
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_UP:
                keys[0]=False
            elif event.key==pygame.K_LEFT:
                keys[1]=False
            elif event.key==pygame.K_DOWN:
                keys[2]=False
            elif event.key==pygame.K_RIGHT:
                keys[3]=False

    #플레이어를 움직인다.
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5

    #막대바가 줄어들면 게임 종료
    if healthvalue<=0:
        running=0
        exitcode=2
    if exitcode==2: 
        screen.blit(youwin, (0,0))
    
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()