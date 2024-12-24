# MotionDesk

 [![Python](https://img.shields.io/badge/python-3.12.6-blue.svg)](https://www.python.org/downloads/)  [![Platform](https://img.shields.io/badge/platform-windows-green.svg)](https://www.microsoft.com/en-in/windows?r=1) 

**MotionDesk** is a cutting-edge application that revolutionizes the way users interact with their desktop environments through *gesture control*. By utilizing advanced technologies such as [**OpenCV**](https://github.com/opencv/opencv) and [**MediaPipe**](https://github.com/google/mediapipe), MotionDesk enables a completely hands-free workflow, allowing users to navigate their systems using intuitive hand gestures.

## Key Features

- **Gesture-Controlled Interface**: MotionDesk employs sophisticated gesture recognition to control mouse movements and keyboard inputs without the need for physical devices. This allows for a seamless and efficient user experience.

- **Graphical User Interface (GUI)**: Built with [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter), the application features a user-friendly GUI that simplifies the configuration and customization of gesture controls, making it accessible for users of all technical levels.

- **Real-Time Processing**: Utilizing OpenCV's robust computer vision capabilities, MotionDesk processes motion data in real-time, ensuring that gestures are recognized and executed instantly.

- **MediaPipe Integration**: By leveraging MediaPipe's powerful hand tracking and gesture recognition models, MotionDesk accurately detects user movements and translates them into actionable commands on the desktop.

## Getting started 

Follow the steps below to set up and run MotionDesk on your local machine.

### 1. Clone the Repository
First, clone the repository to your local IDE or directory of choice.

**Command:**
```bash
git clone https://github.com/omni-flux/MotionDesk.git
cd MotionDesk
```

### 2. Install Dependencies
Make sure you have Python installed on your system (preferably version 3.7 or higher). Then, use `pip` to install the required dependencies listed in `requirements.txt`.

**Command:**
```bash
pip install -r requirements.txt
```


### 3. Run the Application
You can run MotionDesk in different modes depending on your use case:

#### **A. Run the GUI**
To launch the graphical user interface (GUI), execute the following:

**Command:**
```bash
python GUI/CTk_GUI.py
```

This will start the Control Panel interface for MotionDesk.

#### **B. Run Modules Individually**
To run specific modules as standalone applications:
- **For the Keyboard Module**:
  ```bash
  python VRK.py
  ```
- **For the Mouse Module**:
  ```bash
  python VRM.py
  ```

### Notes

- Ensure that all required dependencies are installed before running any scripts.
- If you encounter issues, verify that your Python version and the installed libraries are compatible.

For further details, refer to the repository's documentation or raise an issue in the GitHub repository.


## GUI
<img src="https://github.com/user-attachments/assets/07c47f26-ee97-4379-94c5-aad640260f9b" alt="Screenshot 2024-11-15 103904 - Copy" width="400" height="380">

## Gestures

<h3>Watch this video with all gestures timestamped to know more about them:</h3>
<p style="font-size: 2;">(Tip: Right-click the thumbnail and select "Open link in new tab" for convenience.)</p>
<a href="https://youtu.be/use8VZmdueE?si=Vq4FUZrzS1wHzkCU">
  <img src="https://img.youtube.com/vi/use8VZmdueE/0.jpg" alt="YouTube Video" width="400">
</a>

## Real World Applications
MotionDesk has a wide range of real-world applications across multiple industries. Below are a few examples of how the technology can be applied:

### 1. Healthcare - Hands-Free Interaction for Hygiene and Contamination Prevention
MotionDesk can be implemented in healthcare settings to enable hands-free interaction with devices, minimizing physical contact and reducing the risk of contamination. For example, doctors and nurses can control medical equipment, access patient records, or adjust settings without touching devices, which is particularly important in maintaining hygiene in sterile environments like operating rooms and ICUs.

<img src="https://github.com/user-attachments/assets/a310f53c-9dfe-45f4-a830-00a7ae0f8168" alt="Screenshot 2024-12-21 220456" width="300" height="280">


### 2. Gaming - Immersive and Natural User Interaction
In the gaming industry, MotionDesk enhances user experience by enabling gesture-based controls, providing a more immersive and interactive environment. Gamers can control characters, navigate through virtual worlds, and interact with the game environment using their body movements, similar to motion-sensing controllers but with a broader range of capabilities.

<img src="https://github.com/user-attachments/assets/e25735ba-e5ce-48fa-87ed-d7615d73574d" alt="Screenshot 2024-12-24 173902" width="300" height="280">


### 3. Smart Home Automation - Gesture-Controlled Device Management
MotionDesk can be integrated into smart home systems to enable gesture-based control of household devices. From adjusting lighting to controlling entertainment systems or appliances, users can interact with their home environment effortlessly, using natural hand gestures instead of physical switches, remotes, or voice commands.


<img src="https://github.com/user-attachments/assets/97296b28-a532-4aaa-8a47-1160f160e652" alt="Screenshot 2024-12-24 184235" width="300" height="280">


## Contribution

Contributions are encouraged! If you would like to enhance MotionDesk or report any issues, please submit pull requests or open issues on GitHub.

## Author & Socials

Created by Omkar Nayak. Connect with me:

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)](https://github.com/omni-flux)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/omkar-nayak-developer/)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](https://mail.google.com/mail/?view=cm&fs=1&to=omkarnayak.work@gmail.com)



