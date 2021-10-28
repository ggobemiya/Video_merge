import os
import cv2
import numpy as np
import sys

#합성 좌표영역안에 원하는 영상을 줄여서 합성하는 파일

#input
#파일경로
video_path = 'C:/Users/KMS/Documents/Coding/video/video_merge/'
#합성될 영상
video1 = video_path + 'fire1.mkv'
#배경 영상
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

print("frame1, frame2, fps = ",frame_cnt1, frame_cnt2, fps)

#영상 가로 세로 설정
w2 = round(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
h2 = round(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

w1 = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h1 = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("w1, h1 = ", w1,h1,"w2, h2 = ", w2,h2)

#합성좌표
x1, y1 = 22,123
x2, y2 = 1070, 841
video2_w = x2-x1
video2_h = y2-y1

resize_x = video2_w/w1
resize_y = video2_h/h1
print("resize_x, resize_y = ", resize_x, resize_y)

#비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter(video_path+ 'output1.avi', fourcc, fps, (w2,h2))

#1번 영상 열기
for i in range(frame_cnt1):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        break
    frame1 = cv2.resize(frame1, dsize=(0,0), fx=resize_x, fy=resize_y)
    if i ==0 :
        print(x2-x1, y2-y1, frame1.shape)
        #print(len(framex), len(framex[0]), type(frame1))
        cv2.imwrite(video_path + 'frame2.jpg',frame2)
        pass
    frame2[y1:y2, x1:x2] = frame1
    out.write(frame2)
    cv2.imshow('frame',frame2)
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