# ACAV - Autonomous Construction Aid Vehicle

ACAV (Autonomous Construction Aid Vehicle) is a mini-project aimed at developing an AI-powered cyber truck-like robot capable of assisting with carrying heavy loads for workers on construction sites. The project utilizes computer vision and artificial intelligence to enable the robot to autonomously follow and assist workers.

## How It Works

The ACAV system operates as follows:

1. **Object Detection**: The ACAV system uses YOLOv3 (You Only Look Once) for real-time object detection to localize a worker within its vicinity.

2. **Worker Localization**: ArUco markers embedded in the worker's uniform are utilized for worker recognition and localization. These markers provide a unique identifier for each worker, enabling the robot to locate and track them accurately.

3. **Autonomous Following**: The robot follows predefined rules to trail the recognized worker. This includes maintaining a safe distance and adjusting its speed based on the worker's movement.

4. **Gesture-Based Communication**: Interaction between the robot and the worker is facilitated through hand gestures. A set of predefined gestures are established for communication, such as:
    - **Thumbs Up**: Command for the robot to follow the worker.
    - **High Five**: Command for the robot to stop and remain stationary.

## Features

- Real-time object detection and tracking using YOLOv3.
- Precise worker localization via ArUco markers.
- Autonomous following with predefined rules for safe interaction.
- Gesture-based communication for seamless interaction between the robot and the worker.

## Usage

To utilize the ACAV system, follow these steps:

1. Ensure the ACAV robot is powered on and connected to the necessary sensors and actuators.
2. Deploy the YOLOv3 object detection model on the robot's hardware.
3. Embed ArUco markers on the workers' uniforms for accurate localization.
4. Initiate the ACAV system and monitor its interaction with workers.
5. Utilize hand gestures according to the predefined commands for communication with the robot.

## Contributing

Contributions to ACAV are welcome! If you're interested in contributing to the project, please follow these guidelines:
- Fork the repository.
- Create your feature branch (`git checkout -b feature/YourFeature`).
- Commit your changes (`git commit -am 'Add some feature'`).
- Push to the branch (`git push origin feature/YourFeature`).
- Create a new Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
