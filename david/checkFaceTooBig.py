import cv2
import sys
from keras.models import load_model
import numpy as np
from imageai.Detection import ObjectDetection

def find_biggest_face(img, casc_path):
    face_cascade = cv2.CascadeClassifier(casc_path)
    faces = face_cascade.detectMultiScale(img, 1.1, 8)
    size = 0
    biggest_face = None
    for face in faces:
        face_size = face[2] * face[3]
        if  face_size > size:
            size = face_size
            biggest_face = face
    
    return (len(faces), biggest_face)

def check_emotion(img):
    emotion_dict= {'Angry': 0, 'Sad': 5, 'Neutral': 4, 'Disgust': 1, 'Surprise': 6, 'Fear': 2, 'Happy': 3}
    img = cv2.resize(img, (48,48))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("derp", img)
    cv2.waitKey(0)
    img = np.reshape(img, [1, img.shape[0], img.shape[1], 1])


    model = load_model("model_v6_23.hdf5")
    print(model.predict(img))
    predicted_class = np.argmax(model.predict(img))
    label_map = dict((v,k) for k,v in emotion_dict.items()) 
    predicted_label = label_map[predicted_class]
    print(predicted_label)

def check_people(img_path):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath('yolo.h5')
    detector.loadModel()
    peopleOnly = detector.CustomObjects(person=True)
    detectedImage, detections = detector.detectCustomObjectsFromImage(custom_objects=peopleOnly, output_type="array", input_image=img_path, minimum_percentage_probability=30)
    return len(detections)


def checkFaceTooBigMain(img_path, casc_path):
    # Returns a tuple (Number of people -> Integer, Is face too big -> Boolean)
    try:
        img = cv2.imread(img_path)
    except:
        print("Face-too-big-checker could not read image file..")
        return
    num_people = check_people(img_path)
    if num_people == 0:
        return (num_people, False)
    faces_result = find_biggest_face(img, casc_path)
    if faces_result[0] == 0:
        return (num_people, False)
    face = faces_result[1]
    sub_image = img[face[1]:face[1]+face[3], face[0]:face[0]+face[2]]
    #check_emotion(sub_image)

    face_too_big = False
    if (face[2] * face[3]) / (img.shape[0]*img.shape[1]) > 0.25:
        face_too_big = True
    return (num_people, face_too_big)


def main():
    print(checkFaceTooBigMain(sys.argv[1], sys.argv[2]))

if __name__ == "__main__":
    main()