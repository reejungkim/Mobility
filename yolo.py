
import streamlit as st
import pandas as pd
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os
#import tensorflow as tf
#import tensorflow_hub as hub
import time
import sys
from streamlit_embedcode import github_gist
import urllib.request
import urllib
import moviepy.editor as moviepy
import cv2
import numpy as np
import time
import sys


def main():
    new_title = '<p style="font-size: 42px;">Welcome to my Object Detection App!</p>'
    read_me_0 = st.markdown(new_title, unsafe_allow_html=True)

    read_me = st.markdown("""
    This project was built using Streamlit and OpenCV 
    to demonstrate YOLO Object detection in both videos(pre-recorded)
    and images.
    
    
    This YOLO object Detection project can detect 80 objects(i.e classes)
    in either a video or image. The full list of the classes can be found 
    [here](https://github.com/KaranJagtiani/YOLO-Coco-Dataset-Custom-Classes-Extractor/blob/main/classes.txt)"""
                          )
    st.sidebar.title("Select Activity")
    choice = st.sidebar.selectbox(
        "MODE", ("About", "Object Detection(Image)", "Object Detection(Video)"))
    # ["Show Instruction","Landmark identification","Show the #source code", "About"]

    if choice == "Object Detection(Image)":
        #st.subheader("Object Detection")
        read_me_0.empty()
        read_me.empty()
        #st.title('Object Detection')
        object_detection_image()
    elif choice == "Object Detection(Video)":
        read_me_0.empty()
        read_me.empty()
        #object_detection_video.has_beenCalled = False
        object_detection_video()
        # if object_detection_video.has_beenCalled:
        try:

            clip = moviepy.VideoFileClip('detected_video.mp4')
            clip.write_videofile("myvideo.mp4")
            st_video = open('myvideo.mp4', 'rb')
            video_bytes = st_video.read()
            st.video(video_bytes)
            st.write("Detected Video")
        except OSError:
            ''

    elif choice == "About":
        print()


if __name__ == '__main__':
    main()


def object_detection_image():
    st.title('Object Detection for Images')
    st.subheader("""
    This object detection project takes in an image and outputs the image with bounding boxes created around the objects in the image
    """)
    file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])
    if file != None:
        img1 = Image.open(file)
        img2 = np.array(img1)

        st.image(img1, caption="Uploaded Image")
        my_bar = st.progress(0)
        confThreshold = st.slider('Confidence', 0, 100, 50)
        nmsThreshold = st.slider('Threshold', 0, 100, 20)
        #classNames = []
        whT = 320
        url = "https://raw.githubusercontent.com/zhoroh/ObjectDetection/master/labels/coconames.txt"
        f = urllib.request.urlopen(url)
        classNames = [line.decode('utf-8').strip() for line in f]
        #f = open(r'C:\Users\Olazaah\Downloads\stream\labels\coconames.txt','r')
        #lines = f.readlines()
        #classNames = [line.strip() for line in lines]
        config_path = r'config_n_weights\yolov3.cfg'
        weights_path = r'config_n_weights\yolov3.weights'
        net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        def findObjects(outputs, img):
            hT, wT, cT = img2.shape
            bbox = []
            classIds = []
            confs = []
            for output in outputs:
                for det in output:
                    scores = det[5:]
                    classId = np.argmax(scores)
                    confidence = scores[classId]
                    if confidence > (confThreshold/100):
                        w, h = int(det[2]*wT), int(det[3]*hT)
                        x, y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                        bbox.append([x, y, w, h])
                        classIds.append(classId)
                        confs.append(float(confidence))

            indices = cv2.dnn.NMSBoxes(
                bbox, confs, confThreshold/100, nmsThreshold/100)
            obj_list = []
            confi_list = []
            # drawing rectangle around object
            for i in indices:
                i = i
                box = bbox[i]
                x, y, w, h = box[0], box[1], box[2], box[3]
                # print(x,y,w,h)
                cv2.rectangle(img2, (x, y), (x+w, y+h), (240, 54, 230), 2)
                # print(i,confs[i],classIds[i])
                obj_list.append(classNames[classIds[i]].upper())

                confi_list.append(int(confs[i]*100))
                cv2.putText(img2, f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (240, 0, 240), 2)
            df = pd.DataFrame(list(zip(obj_list, confi_list)),
                              columns=['Object Name', 'Confidence'])
            if st.checkbox("Show Object's list"):

                st.write(df)
            if st.checkbox("Show Confidence bar chart"):
                st.subheader('Bar chart for confidence levels')

                st.bar_chart(df["Confidence"])

        blob = cv2.dnn.blobFromImage(
            img2, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        layersNames = net.getLayerNames()
        outputNames = [layersNames[i-1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        findObjects(outputs, img2)

        st.image(img2, caption='Proccesed Image.')

        cv2.waitKey(0)

        cv2.destroyAllWindows()
        my_bar.progress(100)
