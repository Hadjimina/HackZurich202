import cv2
import sys

def find_biggest_face(img):
    face_cascade = cv2.CascadeClassifier("haarcascade.xml")
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    size = 0
    biggest_face = None
    for face in faces:
        cv2.rectangle(img, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0,255,0), 2)
        face_size = face[2] * face[3]
        if  face_size > size:
            size = face_size
            biggest_face = face
    cv2.imshow("Hello", img)
    cv2.waitKey(0)
    return biggest_face



def main():
    img_path = sys.argv[1]
    try:
        img = cv2.imread(img_path)
    except:
        print("Face-too-big-checker could not read image file..")
        return
    face = find_biggest_face(img)
    
    

if __name__ == "__main__":
    main()
