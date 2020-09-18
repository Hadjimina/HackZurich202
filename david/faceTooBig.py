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
    
    cv2.rectangle(img, (biggest_face[0], biggest_face[1]), (biggest_face[0] + biggest_face[2], biggest_face[1] + biggest_face[3]), (0,255,0), 2)

    cv2.imshow("Hello", img)
    cv2.waitKey(0)
    return (len(faces), biggest_face)



def checkFaceTooBigMain():
    # Returns a tuple (Number of faces -> Integer, Is face too big -> Boolean)
    img_path = sys.argv[1]
    try:
        img = cv2.imread(img_path)
    except:
        print("Face-too-big-checker could not read image file..")
        return
    result = find_biggest_face(img)
    face = result[1]
    img_size = img.shape
    face_too_big = False
    if face[2] / img_size[0] > 0.3 or face[3] / img_size[1] > 0.3:
        face_too_big = True
    return (result[0, face_too_big])
    

