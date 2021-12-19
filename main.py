import cv2       as cv
import mediapipe as mp
import math
import ctypes
import time
from fbchat     import Client
from playsound  import playsound
from webbrowser import open_new_tab
from win32api   import keybd_event
from win32con   import VK_MEDIA_PLAY_PAUSE, VK_MEDIA_NEXT_TRACK, KEYEVENTF_EXTENDEDKEY, VK_MEDIA_PREV_TRACK


vs       = cv.VideoCapture(0)
distTh   = 0.05
debTime  = 0
debDelay = 2.5
mpHands  = mp.solutions.hands
mpDraw   = mp.solutions.drawing_utils
hands    = mpHands.Hands(static_image_mode        = False,
					 	 max_num_hands            =     1,
						 min_detection_confidence =   0.70,
						 min_tracking_confidence  =   0.70)
username = "****"
passw    = "****"
vName    = "****"
client   = Client(username, passw)

def exitApp(msg):
    vs.release()
    cv.destroyAllWindows()
    print(msg + " Exiting...")
    exit(-1)

def checkIntersect(p1, p2):
	return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2) <= distTh

if __name__ == '__main__':
	try:
		while vs.isOpened():
			ret, frame = vs.read()
			if not ret: exitApp("Can't receive frame. Is the camera connected?")

			results = hands.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
			if results.multi_hand_landmarks:
				for handLms in results.multi_hand_landmarks:
					lmCor = [lm for lm in handLms.landmark]

					'''if checkIntersect(lmCor[6], lmCor[8]) and checkIntersect(lmCor[14], lmCor[16]) and checkIntersect(lmCor[18], lmCor[20]):
						cv.imwrite("tmp.jpg", frame)

						friendID = client.searchForUsers(vName, limit=1)[0].uid
						client.sendLocalImage("tmp.png", message="Eik nx", thread_id=friendID)
						print("yeet")'''

					if time.time() - debTime < debDelay:
						if checkIntersect(lmCor[4], lmCor[8]):
							debTime = 0
							keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
						
						if checkIntersect(lmCor[4], lmCor[12]):
							debTime = 0
							keybd_event(VK_MEDIA_NEXT_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)

						if checkIntersect(lmCor[4], lmCor[16]):
							debTime = 0
							keybd_event(VK_MEDIA_PREV_TRACK, 0, KEYEVENTF_EXTENDEDKEY, 0)

						if checkIntersect(lmCor[4], lmCor[20]):
							debTime = 0
							open_new_tab("https://www.youtube.com/watch?v=Mvvsa5HAJiI&list=RDMM&start_radio=1")

						if checkIntersect(lmCor[4], lmCor[17]):
							ctypes.windll.user32.LockWorkStation()
							debTime = 0
					elif checkIntersect(lmCor[4], lmCor[5]):
						playsound("bep.wav")
						debTime = time.time();
					#mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)
			#cv.imshow("Image", frame)
			cv.waitKey(1)

		exitApp("Camera disconnected.")
	except KeyboardInterrupt:
		exitApp("Program exited by user.")