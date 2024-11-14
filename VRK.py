import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time
from Commons import VRMouse


class Button:
    def __init__(self, pos, label, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.label = label


class VRKeyboard:
    def __init__(self, cam_w=1280, cam_h=720):
        self.running_k = False
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, cam_w)
        self.cap.set(4, cam_h)
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)
        self.keyboard = Controller()
        self.final_text = ""
        self.caps_on = False
        self.numeric_mode = False
        self.buttons = self.create_buttons(self.alpha_keys)
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

    def start_keyboard(self):
        """Main loop to run the virtual keyboard."""
        self.running_k = True
        try:
            while self.running_k:
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

                    if fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0:
                        self.end_keyboard()


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
        self.running_k = False
        self.cap.release()
        cv2.destroyAllWindows()


    def end_keyB_strM(self):
        self.end_keyboard()
        vr_mouse = VRMouse()
        vr_mouse.start_mouse()


if __name__ == "__main__":
    vr_keyboard = VRKeyboard()
    vr_keyboard.start_keyboard()
