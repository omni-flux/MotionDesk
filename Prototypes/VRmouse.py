import cv2
from cvzone.HandTrackingModule import HandDetector
from SmoothingFILTERS import OneEuroFilter
import mouse
import numpy as np
import time


screen_w, screen_h = 1920, 1080

frameR = 100
cam_w, cam_h = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

detector = HandDetector(detectionCon=0.95, maxHands=1)

l_delay_time = 0
r_delay_time = 0
double_delay_time = 0

# drag n drop vs
drag_start_time = None
release_start_time = None
dragging = False
HOLD_DURATION = 0.5
RELEASE_DURATION = 0.5

# One-euro filter variables
filter_x = OneEuroFilter(min_cutoff=0.7, beta=0.01)
filter_y = OneEuroFilter(min_cutoff=0.7, beta=0.01)

CLICK_DELAY = 1
DOUBLE_CLICK_DELAY = 2

try:
    while True:
        success, img = cap.read()
        if success:
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)
            cv2.rectangle(img, (frameR, frameR), (cam_w - frameR, cam_h - frameR), (0, 0, 0), 2)

            if hands:
                lmlist = hands[0]['lmList']
                ind_x, ind_y = lmlist[8][0], lmlist[8][1]  # Index finger tip
                mid_x, mid_y = lmlist[12][0], lmlist[12][1]  # Middle finger tip
                pnk_x, pnk_y = lmlist[16][0], lmlist[16][1]  # Pinky finger tip
                rin_x, rin_y = lmlist[20][0], lmlist[20][1]  # Ring finger tip

                # cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
                # cv2.circle(img, (mid_x, mid_y), 5, (0, 255, 255), 2)

                fingers = detector.fingersUp(hands[0])

                if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:  # Index finger up, middle down

                    smooth_x = filter_x(ind_x)
                    smooth_y = filter_y(ind_y)

                    conv_x = int(np.interp(smooth_x, (frameR, cam_w - frameR), (0, screen_w)))
                    conv_y = int(np.interp(smooth_y, (frameR, cam_h - frameR), (0, screen_h)))
                    mouse.move(conv_x, conv_y)

                current_time = time.monotonic()

                # Mouse button clicks
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:  # Both index and middle fingers up
                    if abs(ind_x - mid_x) < 25:
                        # right click (if thumb is down and delay has passed)
                        if fingers[4] == 0 and (current_time - l_delay_time) > CLICK_DELAY:
                            mouse.click(button="right")
                            l_delay_time = current_time
                            # print("right click")

                # left click (if thumb is up and delay has passed)
                if fingers[1] == 1 and fingers[0] == 1 and fingers[3] == 0:
                  if fingers[4] == 1 and (current_time - r_delay_time) > CLICK_DELAY:
                    mouse.click(button="left")
                    r_delay_time = current_time
                    # print("left click")

                # Mouse scrolling
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:  # Index and middle fingers up, thumb down
                    if abs(ind_x - mid_x) < 25:
                        if fingers[4] == 0:
                            mouse.wheel(delta=-1)  # Scroll down
                            # print("Scroll down")
                        elif fingers[4] == 1:
                            mouse.wheel(delta=1)  # Scroll up
                            # print("Scroll up")

                # Drag and Drop function
                if fingers[1] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    if abs(pnk_x - rin_x) < 30:
                        # Start drag if held for HOLD_DURATION
                        if not dragging:
                            if drag_start_time is None:
                                drag_start_time = time.time()  # Start timing hold
                            elif time.time() - drag_start_time >= HOLD_DURATION:
                                # print("Starting drag...")
                                mouse.press(button='left')
                                dragging = True  # Set dragging state to True
                                release_start_time = None  # Reset release timer
                        else:
                            drag_start_time = None  # Reset drag start timer
                    elif abs(pnk_x - rin_x) > 30:
                        # Start release timer when moving fingers apart
                        if dragging:
                            if release_start_time is None:
                                release_start_time = time.time()
                            elif time.time() - release_start_time >= RELEASE_DURATION:
                                # print("Stopping drag...")
                                mouse.release(button='left')
                                dragging = False  # Reset dragging state
                                drag_start_time = None  # Reset drag start timer
                else:
                    # Reset if gesture is completely lost
                    drag_start_time = None
                    release_start_time = None
                    if dragging:
                        # print("Gesture lost; stopping drag.")
                        mouse.release(button='left')
                        dragging = False

                # Double mouse click
                if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[4] == 0 and (
                        current_time - double_delay_time) > DOUBLE_CLICK_DELAY:
                    mouse.double_click(button="left")
                    double_delay_time = current_time
                    # print("Double click")

            cv2.imshow("Camera Feed", img)

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    cap.release()
    cv2.destroyAllWindows()


