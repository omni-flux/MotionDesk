import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import time

# Define keyboard layouts
alpha_keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
              ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
              ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
              ["Caps", "Spac", "Entr", "Bksp", "123"]]
num_keys = [["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["-", "/", ":", ";", "(", ")", "$", "&", "@", "\""],
            ["#", "%", "*", "+", "=", "^", "!", "?", "_", "\\"],
            ["ABC"]]

# Initialize variables
final_text = ""
keyboard = Controller()
caps_on = False
numeric_mode = False

# Camera setup
cam_w, cam_h = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


# Button class
class Button:
    def __init__(self, pos, label, size=None):
        if size is None:
            size = [85, 85]
        self.pos = pos
        self.size = size
        self.label = label


# Function to create buttons
def create_buttons(layout):
    buttons = []
    for i, row in enumerate(layout):
        for j, key in enumerate(row):
            buttons.append(Button([100 * j + 50, 100 * i + 50], key))
    return buttons


# Function to draw buttons
def draw_keyboard(img, buttons):
    for button in buttons:
        x, y = button.pos
        w, h = button.size
        # Draw button
        cv2.rectangle(img, (x, y), (x + w, y + h), (50, 50, 50), cv2.FILLED)
        label = button.label.upper() if caps_on else button.label.lower()
        cv2.putText(img, label, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    return img

# Initialize button list with alphabetic keys
buttons = create_buttons(alpha_keys)

# Timing variables
last_click_time = 0
click_delay = 1.0

try:
    while True:
        success, img = cap.read()
        if not success:
            break

        # Flip the image for hand tracking
        img_flipped = cv2.flip(img, 1)

        # Detect hands
        hands, img_flipped = detector.findHands(img_flipped, flipType=False)

        # Draw the keyboard
        img_flipped = draw_keyboard(img_flipped, buttons)

        if hands:
            lm_list = hands[0]['lmList']
            ind_x, ind_y = lm_list[8][0], lm_list[8][1]  # Index finger tip
            fingers = detector.fingersUp(hands[0])

            # Check for key presses
            if fingers[1] == 1:  # Index finger up
                for button in buttons:
                    x, y = button.pos
                    w, h = button.size
                    if x < ind_x < x + w and y < ind_y < y + h:
                        # Highlight button
                        cv2.rectangle(img_flipped, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                        label = button.label.upper() if caps_on else button.label.lower()
                        cv2.putText(img_flipped, label, (x + 10, y + 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                        # Check delay and press key
                        current_time = time.time()
                        if fingers[1] == 1 and fingers[4] == 1 and (current_time - last_click_time > click_delay):
                            last_click_time = current_time

                            try:
                                if button.label == "Space":
                                    final_text += " "
                                    keyboard.press(Key.space)
                                elif button.label == "Enter":
                                    final_text += "\n"
                                    keyboard.press(Key.enter)
                                elif button.label == "Bksp":
                                    final_text = final_text[:-1]
                                    keyboard.press(Key.backspace)
                                elif button.label == "Caps":
                                    caps_on = not caps_on
                                elif button.label == "123":
                                    numeric_mode = True
                                    buttons = create_buttons(num_keys)
                                elif button.label == "ABC":
                                    numeric_mode = False
                                    buttons = create_buttons(alpha_keys)
                                else:
                                    key_to_type = button.label.upper() if caps_on else button.label.lower()
                                    try:
                                        keyboard.press(key_to_type)
                                    except ValueError as e:
                                        print(f"Exitrror pressing key: {key_to_type} - {e}")
                                        # Handle invalid key (optional, e.g., log or ignore)
                                        continue  # Skip this iteration if key press fails
                            except Exception as e:
                                print(f"Unexpected error: {e}")
                                continue  # Skip this iteration if any unexpected error occurs


        # Display the image
        cv2.imshow("Virtual Keyboard", img_flipped)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()




