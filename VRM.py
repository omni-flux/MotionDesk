import cv2
from cvzone.HandTrackingModule import HandDetector
from SmoothingFILTERS import OneEuroFilter
import mouse
import numpy as np
import time
from Commons import VRKeyboard



class VRMouse:
    def __init__(self, screen_w=1920, screen_h=1080, cam_w=640, cam_h=480, frameR=100):
        self.running_m = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, cam_w)
        self.cap.set(4, cam_h)
        self.detector = HandDetector(detectionCon=0.95, maxHands=1)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.cam_w = cam_w
        self.cam_h = cam_h
        self.frameR = frameR
        self.l_delay_time = 0
        self.r_delay_time = 0
        self.double_delay_time = 0
        self.drag_start_time = None
        self.release_start_time = None
        self.dragging = False
        self.HOLD_DURATION = 0.5
        self.RELEASE_DURATION = 0.5
        self.filter_x = OneEuroFilter(min_cutoff=0.7, beta=0.01)
        self.filter_y = OneEuroFilter(min_cutoff=0.7, beta=0.01)
        self.CLICK_DELAY = 1
        self.DOUBLE_CLICK_DELAY = 2

    def start_mouse(self):
        """Begins processing hand gestures for controlling mouse actions."""
        self.running_m = True
        try:
            while self.running_m:
                success, img = self.cap.read()
                if success:
                    img = cv2.flip(img, 1)
                    hands, img = self.detector.findHands(img, flipType=False)
                    cv2.rectangle(img, (self.frameR, self.frameR),
                                  (self.cam_w - self.frameR, self.cam_h - self.frameR), (0, 0, 0), 2)

                    if hands:
                        lmlist = hands[0]['lmList']
                        ind_x, ind_y = lmlist[8][0], lmlist[8][1]  # Index finger tip
                        mid_x, mid_y = lmlist[12][0], lmlist[12][1]  # Middle fingertip
                        pnk_x, pnk_y = lmlist[16][0], lmlist[16][1]  # Pinky fingertip
                        rin_x, rin_y = lmlist[20][0], lmlist[20][1]  # Ring fingertip

                        fingers = self.detector.fingersUp(hands[0])

                        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
                            self.end_mouse()


                        if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 and fingers[0] == 0:
                            self.end_Mou_strtK()


                        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:  # Index finger up, middle down
                            smooth_x = self.filter_x(ind_x)
                            smooth_y = self.filter_y(ind_y)
                            conv_x = int(np.interp(smooth_x, (self.frameR, self.cam_w - self.frameR), (0, self.screen_w)))
                            conv_y = int(np.interp(smooth_y, (self.frameR, self.cam_h - self.frameR), (0, self.screen_h)))
                            mouse.move(conv_x, conv_y)

                        current_time = time.monotonic()

                        # Mouse button clicks
                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                            if abs(ind_x - mid_x) < 25:
                                if fingers[4] == 0 and (current_time - self.l_delay_time) > self.CLICK_DELAY:
                                    mouse.click(button="right")
                                    self.l_delay_time = current_time

                        # Left click
                        if fingers[1] == 1 and fingers[0] == 1 and fingers[3] == 0:
                            if fingers[4] == 1 and (current_time - self.r_delay_time) > self.CLICK_DELAY:
                                mouse.click(button="left")
                                self.r_delay_time = current_time

                        # Mouse scrolling
                        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                            if abs(ind_x - mid_x) < 25:
                                mouse.wheel(delta=-1 if fingers[4] == 0 else 1)

                        # Drag and Drop function
                        if fingers[1] == 1 and fingers[3] == 1 and fingers[4] == 1:
                            if abs(pnk_x - rin_x) < 30:
                                if not self.dragging:
                                    if self.drag_start_time is None:
                                        self.drag_start_time = time.time()
                                    elif time.time() - self.drag_start_time >= self.HOLD_DURATION:
                                        mouse.press(button='left')
                                        self.dragging = True
                                        self.release_start_time = None
                            elif abs(pnk_x - rin_x) > 30:
                                if self.dragging:
                                    if self.release_start_time is None:
                                        self.release_start_time = time.time()
                                    elif time.time() - self.release_start_time >= self.RELEASE_DURATION:
                                        mouse.release(button='left')
                                        self.dragging = False
                        else:
                            self.drag_start_time = None
                            self.release_start_time = None
                            if self.dragging:
                                mouse.release(button='left')
                                self.dragging = False

                        # Double click
                        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0 and fingers[4] == 0 and \
                                (current_time - self.double_delay_time) > self.DOUBLE_CLICK_DELAY:
                            mouse.double_click(button="left")
                            self.double_delay_time = current_time

                    cv2.imshow("Camera Feed", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        except KeyboardInterrupt:
            print("Keyboard Interrupt detected. Exiting gracefully.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
        finally:
            self.end_mouse()

    def end_mouse(self):
        self.running_m = False
        print("called")
        self.cap.release()
        cv2.destroyAllWindows()


    def end_Mou_strtK(self):
        self.end_mouse()
        vr_keyboard = VRKeyboard()
        vr_keyboard.start_keybord()



if __name__ == "__main__":
    vr_mouse_instance = VRMouse()
    vr_mouse_instance.start_mouse()
