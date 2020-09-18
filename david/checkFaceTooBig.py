import cv2
import sys

def find_biggest_face(img):
    face_cascade = cv2.CascadeClassifier("haarcascade.xml")
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    size = 0
    biggest_face = None
    for face in faces:
        face_size = face[2] * face[3]
        if  face_size > size:
            size = face_size
            biggest_face = face
    
    return biggest_face



def checkFaceTooBigMain():
    img_path = sys.argv[1]
    try:
        img = cv2.imread(img_path)
    except:
        print("Face-too-big-checker could not read image file..")
        return
    face = find_biggest_face(img)
    img_size = img.shape
    print(img_size)
    if face[2] / img_size[0] > 0.3 or face[3] / img_size[1] > 0.3:
        return("Face is too big..")
    else:
        return 0
    

