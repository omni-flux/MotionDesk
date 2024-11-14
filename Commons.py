import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time
import cv2
from cvzone.HandTrackingModule import HandDetector
from SmoothingFILTERS import OneEuroFilter
import mouse
import numpy as np
import time



class Button:
    def __init__(self, pos, label, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.label = label


class VRKeyboard:
    def __init__(self, cam_w=1280, cam_h=720):
        # Camera and keyboard setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, cam_w)
        self.cap.set(4, cam_h)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.keyboard = Controller()
        self.final_text = ""
        self.caps_on = False
        self.numeric_mode = False
        self.buttons = self.create_buttons(self.alpha_keys)

        # Timing variables
        self.last_click_time = 0
        self.click_delay = 1.0

    # Define keyboard layouts
    alpha_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                  ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                  ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
                  ["Caps", "Space", "Enter", "Bksp", "123"]]
    num_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
                ["#", "%", "*", "+", "=", "^", "!", "?", "_", "\\"],
                ["ABC"]]

    def create_buttons(self, layout):
        buttons = []
        for i, row in enumerate(layout):
            for j, key in enumerate(row):
                buttons.append(Button([100 * j + 50, 100 * i + 50], key))
        return buttons

    def draw_keyboard(self, img):
        for button in self.buttons:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)
            label = button.label.upper() if self.caps_on else button.label.lower()
            cv2.putText(img, label, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        return img

    def start_keybord(self):
        """Main loop to run the virtual keyboard."""
        try:
            while True:
                success, img = self.cap.read()
                if not success:
                    break
                img_flipped = cv2.flip(img, 1)
                hands, img_flipped = self.detector.findHands(img_flipped, flipType=False)
                img_flipped = self.draw_keyboard(img_flipped)

                if hands:
                    lm_list = hands[0]['lmList']
                    ind_x, ind_y = lm_list[8][0], lm_list[8][1]
                    fingers = self.detector.fingersUp(hands[0])


                    if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1 and fingers[0] == 0:
                        self.end_keyB_strM()


                    if fingers[1] == 1:
                        for button in self.buttons:
                            x, y = button.pos
                            w, h = button.size
                            if x < ind_x < x + w and y < ind_y < y + h:
                                cv2.rectangle(img_flipped, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175),
                                              cv2.FILLED)
                                label = button.label.upper() if self.caps_on else button.label.lower()
                                cv2.putText(img_flipped, label, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                            (255, 255, 255), 2)

                                current_time = time.time()
                                if fingers[1] == 1 and fingers[4] == 1 and (
                                        current_time - self.last_click_time > self.click_delay):
                                    self.last_click_time = current_time

                                    # Handle key press logic here
                                    if button.label == "Space":
                                        self.final_text += " "
                                        self.keyboard.press(Key.space)
                                    elif button.label == "Enter":
                                        self.final_text += "\n"
                                        self.keyboard.press(Key.enter)
                                    elif button.label == "Bksp":
                                        self.final_text = self.final_text[:-1]
                                        self.keyboard.press(Key.backspace)
                                    elif button.label == "Caps":
                                        self.caps_on = not self.caps_on
                                    elif button.label == "123":
                                        self.numeric_mode = True
                                        self.buttons = self.create_buttons(self.num_keys)
                                    elif button.label == "ABC":
                                        self.numeric_mode = False
                                        self.buttons = self.create_buttons(self.alpha_keys)
                                    else:
                                        key_to_type = button.label.upper() if self.caps_on else button.label.lower()
                                        self.keyboard.press(key_to_type)


                cv2.imshow("Virtual Keyboard", img_flipped)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.end_keyboard()

    def end_keyboard(self):
        self.cap.release()
        cv2.destroyAllWindows()


    def end_keyB_strM(self):
        self.end_keyboard()
        vr_mouse = VRMouse()
        vr_mouse.start_mouse()






class VRMouse:
    def __init__(self, screen_w=1920, screen_h=1080, cam_w=640, cam_h=480, frameR=100):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, cam_w)
        self.cap.set(4, cam_h)
        self.detector = HandDetector(detectionCon=0.95, maxHands=1)

        # Initialize variables
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
        try:
            while True:
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
        self.cap.release()
        cv2.destroyAllWindows()


    def end_Mou_strtK(self):
        self.end_mouse()
        vr_keyboard = VRKeyboard()
        vr_keyboard.start_keybord()

