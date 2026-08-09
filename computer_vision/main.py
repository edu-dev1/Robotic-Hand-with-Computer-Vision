import cv2
from mediapipe.python.solutions.hands import Hands, HAND_CONNECTIONS
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from serial import Serial
from extra_functions import mapping

arduino = Serial("COM3", 9600) 
capture = cv2.VideoCapture(0)
#landmarks
fingers_tip_pip = [("thumb", 4, 3), ("index", 8, 6), ("middle", 12, 10), ("ring", 16, 14), ("pinky", 20, 18)]
degrees = []

with Hands(min_detection_confidence = 0.5, min_tracking_confidence = 0.5, max_num_hands = 1) as hand:
    while capture.isOpened():
        returned, frame =  capture.read()
        height, width, _ = frame.shape

        if not returned or cv2.waitKey(1) & 0xff == 27:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hand.process(rgb_frame)
        if results.multi_hand_landmarks: # Si hay mano en la imagen
            for hand_landmark in results.multi_hand_landmarks: # Por cada punto de dedos...
                draw_landmarks(frame, hand_landmark, HAND_CONNECTIONS) # ... los dibuja

                for finger, tip, pip in fingers_tip_pip: # Por cada dedo, punta del dedo y mitad del dedo
                    if finger == "thumb": # Si el dedo es el pulgar ...
                        tip_x = int(hand_landmark.landmark[tip].x * width)
                        pip_x = int(hand_landmark.landmark[pip].x * width)
                        dist = tip_x - pip_x

                        degree = mapping(dist, (-45, 45), (0, 180))

                    else: # Si son los demás dedos
                        
                        tip_y = int(hand_landmark.landmark[tip].y * height)
                        pip_y = int(hand_landmark.landmark[pip].y * height)
                        dist = tip_y - pip_y
                        
                        if finger == "index":
                            range_var = (-85, 85)
                            
                        elif finger == "ring":
                            range_var = (70, -80)
                        
                        elif finger == "pink":
                            range_var = (45, 15)

                        else:
                            range_var = (-95, 80)
                        
                        range_degrees = (180, 0)
                        degree = mapping(dist, range_var, range_degrees)

                        if degree > 180: degree = 180
                        if degree < 0: degree = 0

                    degrees.append(degree)
            if any(val > 256 or val < 0 for val in degrees):
                pass
            else:
                arduino.write(bytes(degrees)) # envía al arduino los grados para el servo
    
        cv2.imshow("Robotic Hand with Computer Vision", frame)
        degrees.clear()

capture.release()
arduino.close()
cv2.destroyAllWindows()
