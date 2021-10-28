import os
import cv2
import numpy as np
import sys

#두 비디오를 이어붙이는 파일

#input
#폴더 경로
video_path = 'C:/Users/KMS/Documents/Coding/videosum/video_merge/'
#합칠 파일명 1
video1 = video_path + 'fire1.mkv'
#합칠 파일명2
video2 = video_path + 'fire1_jb.mp4'



cap1 = cv2.VideoCapture(video1)
cap2 = cv2.VideoCapture(video2)

if not cap1.isOpened() or not cap2.isOpened():
    print("Not open video!")
    sys.exit()
else:
    print("Video open")
    
#각 영상 프레임 수
frame_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap1.get(cv2.CAP_PROP_FPS)
effect_frames = int(fps*2)
delay = int(1000/fps)

print(frame_cnt1, frame_cnt2, fps, effect_frames)

#영상 가로 세로 설정
w2 = round(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
h2 = round(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

w1 = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h1 = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("w1, h1 = ", w1,h1,"w2, h2 = ", w2,h2)

#비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(video_path+ 'output.avi', fourcc, fps, (w2,h2))

#1번 영상 열기
for i in range(frame_cnt1 - effect_frames):
    ret1, frame1 = cap1.read()
    if not ret1:
        break
    frame1 = frame1[:h2, :w2]
    if i ==0 :
        #print(framex.shape)
        #print(len(framex), len(framex[0]), type(frame1))
        pass
    out.write(frame1)
    cv2.imshow('frame',frame1)
    cv2.waitKey(delay)
    
#합성하기
for i in range(effect_frames):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    frame1 = frame1[:h2, :w2]
    if i == 0 :
        print(frame1.shape, frame2.shape)
    
    #가중치 계산
    #만약 i가 1인경우 alpha는 1- 1/48 , 1-alpha는 0에 가까운 값
    alpha = 1.0 - i / effect_frames
    frame = cv2.addWeighted(frame1, alpha, frame2, 1-alpha,0)
    out.write(frame)
    
for i in range(effect_frames, frame_cnt2):
    ret2, frame2 = cap2.read()
    if not ret2:
    	break
        
    out.write(frame2)
    cv2.imshow('frame', frame2)
    cv2.waitKey(delay)
