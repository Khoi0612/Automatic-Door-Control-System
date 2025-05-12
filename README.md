# Automatic-Door-Control-System
🚪 An Automatic Door Control IoT System that allow for manual and automatic door control to enhance security.

🔧 Features
✅ Automatic and Manual Operation Modes
    Auto Mode:
        Opens the door during the day when a person is detected.
        Keeps the door closed and triggers an alarm at night if someone is detected.
    Manual Mode:
        Allows store owners to override the system and directly control door and alarm states.

👁 Sensor Integration
    Ultrasonic Sensor (HC-SR04) - Detects proximity and motion (digital input).
    Photoresistor (LDR) - Detects ambient light levels to distinguish between day and night (analog input).

⚙ Actuator Control
    Servo Motor (SG90) - Opens or closes the door based on logic conditions.
    LED Alarm Indicator - Lights up during night intrusions (manual or automatic mode).

🧠 Edge Computing with Raspberry Pi
    Processes sensor data.
    Logs data to a MySQL database.
    Hosts a Flask web server with a real-time dashboard.

🌐 Web-Based Dashboard
    Developed using Flask (Python) + HTML/CSS/JavaScript.
    Features:
        Real-time log display (distance, light, door state, alarm state, mode).
        Control toggles for manual/auto, door, and alarm.
        Customer traffic counter (based on door state transitions).
        Intuitive, responsive UI for remote access and control.

💾 Data Logging
    All sensor readings and actuator states are recorded into a MySQL database with timestamps.
    Enables future data analysis and store performance insights.

🗂 System Architecture
    Physical Layer: Sensors (Ultrasonic, Photoresistor), Actuators (Servo, LED), ELEGOO Uno (Arduino clone).
    Edge Layer: Raspberry Pi VM running Flask app, MySQL database, and serial communication with Arduino.
    Application Layer: Web dashboard built using HTML, CSS, JS.
    User Layer: Store owner interacting with system via browser.

🖼 Interface Overview
Auto Mode (Default): 	
![Auto Mode (Default)](image.png)
Manual Mode:
![Manual Mode](image-1.png)
With Traffic Count:
![With Traffic Count](image-2.png)

🚀 How to Use
    1. Open the Arduino IDE and upload the sketch located in /edge_device_controller/edge_device_controller.ino to your Arduino-compatible board.
    2. Upload the Arduino code: Plug the Arduino into your computer or Raspberry Pi. Use the Arduino IDE or ls /dev/tty* (on Linux) to identify the port it is connected to (e.g., /dev/ttyUSB0, /dev/ttyACM0).
    3. In the edge_server.py file change the serial port in this line:
        `ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)`
        Replace `'/dev/ttyACM0'` with the correct port identified in Step 2.
    4. Install the requirement libraries: In your terminal, navigate to the project directory and run:
        `pip install -r requirements.txt`
    5. Run the edge server: In your terminal, navigate to the project directory and run:
        `python edge_server.py`
    6. Access the Web Interface via the URL shown in your terminal. Use the dashboard to:
        View real-time system status.
        Switch between manual and automatic modes.
        Open/close the door or enable/disable the alarm manually.
        Count customer traffic between selected date-time ranges.

🛠 Technologies Used
Arduino (ELEGOO Uno) - Sensor reading & actuator control
Python (Flask) - Backend logic, routing, server
HTML/CSS/JavaScript - Web UI design and interactivity
MySQL - Database for logs and analytics
Serial Communication (UART) - Arduino ↔ Raspberry Pi data exchange

