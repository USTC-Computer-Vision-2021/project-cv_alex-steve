import cv2
import glob
import os
import re
import numpy as np
from datetime import datetime

def video_to_frames(video_path, frames_path, resize=True, cut_begin = 0, transpose=True):
     '''
     将视频转为一帧一帧的图片，保存到my-images、result（resize为256*480）和STM数据集处（480*854）
     resize: 是否将图片大小调整为 480*854
     cut_begin: 是否视频前面几帧，参数即去除的帧数
     '''
     videoCapture = cv2.VideoCapture()
     videoCapture.open(video_path)
     fps = videoCapture.get(cv2.CAP_PROP_FPS)
     frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
     print("fps=", int(fps), "frames=", int(frames))
     for i in range(int(frames)):
          ret, frame = videoCapture.read()
          frame = frame.transpose(1, 0, 2)
          if resize:
               frame = frames_resize(frame, 854, 480, False)
          if i >= cut_begin:
               cv2.imwrite(os.path.join(frames_path, "%05d.jpg"%(i - cut_begin)), frame)
               cv2.imwrite(os.path.join("./DAVIS/JPEGImages/480p/blackswan", "%05d.jpg"%(i - cut_begin)), frame)
               frame = frames_resize(frame, 480, 256)
               cv2.imwrite(os.path.join("./result/frame_copytoFGVC", "%05d.jpg"%(i - cut_begin)), frame)

def frames_resize(frame, width, height,dotranspose=False):
     '''
     resize frame to height*width
     '''
     if dotranspose:
          newsize = cv2.resize(frame.transpose(1, 0, 2), (width, height))
          return newsize
     else:
          newsize = cv2.resize(frame, (width, height))
          return newsize
     

'''def vtf(path):
     topath = 'D:\Desktop\CV_course_2021'
     t1 = datetime.now()
     z = topath+'/'+re.findall('.([^/]*)$',path)[0][:-4]
     print(z)
     os.mkdir(z)
     videoCapture = cv2.VideoCapture()
     videoCapture.open(path)
     fps = videoCapture.get(cv2.CAP_PROP_FPS)
     frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
     ze = {"fps":int(fps),"frames":int(frames)}
     for i in range(int(frames)):
          ret, frame = videoCapture.read()
          cv2.imwrite(z+"/%d.jpg"%(i), frame)
     t2 = datetime.now()
     ze['time'] = str(t2 - t1)
     return ze'''

def mask_proc(mask_path):
     '''
     将抠出的第一帧mask从黑白转为黑红，方便输入到STM
     '''
     mask = cv2.imread(mask_path)
     # mask = 255 - mask  # 视情况而定
     mask = (mask > 1).astype(np.uint8) * 128  # 刷为128
     mask[:,:,0:2] = 0  # 去除B,G通道
     mask = mask.astype(np.uint8)  # 转为uint8
     cv2.imwrite("./result/mask_to_red/00000.png", mask)
     cv2.imwrite("./DAVIS/Annotations/480p/blackswan/00000.png", mask)


if __name__ == '__main__':

     t1 = datetime.now()

     # 预先将视频分割为帧，处理完后注释掉该部分
     # vidoe to frames
     video_to_frames("./my-video/xia2/xia.mp4", "./my-images/xia2", resize=True, cut_begin=64, transpose=True)

     # # mask processing
     # mask = cv2.imread("./my-video-mask/ow/blackwhite/ow.png")
     # mask = mask_proc(mask)
     # cv2.imwrite("./my-video-mask/ow/raw/ow.png", mask)
     # print()

     # # mask transformation (red -> white)
     # mask_dir = glob.glob("./my-video-mask/ow/blackwhite/*.png")
     # for dir in mask_dir:
     #      mask = cv2.imread(dir)
     #      mask = mask > 0
     #      mask[:,:,0] = mask[:,:,2]
     #      mask[:,:,1] = mask[:,:,2]
     #      mask = mask.astype(np.uint8) * 255
     #      cv2.imwrite(dir, mask)

     # # image resize
     # image_dir = glob.glob("./my-video-mask/ow/resized/*.jpg")
     # for dir in image_dir:
     #      im = cv2.imread(dir)
     #      im = frames_resize(im, 480, 256)
     #      cv2.imwrite(dir, im)
          
     t2 = datetime.now()
     print("Time cost = ", (t2 - t1))