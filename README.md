# MoSy — Motion Sync Edge AI Engine

**MoSy** is a modular, high-performance Edge AI motion control framework designed for quadrupedal robots. It integrates real-time telemetry from an **HS-1 body suit** (ESP32-C3 + BNO055 IMU sensors) with an exported **PPO-RL ONNX policy** (`Ant-v3`) to execute real-time joint actuation at 50 Hz.

---

## Key Features

- **Ultra-Low Latency Inference:** Executes neural network policy decisions in **< 0.1 ms** using `onnxruntime`.
- **Decoupled Architecture:** Clean separation between telemetry ingestion, AI core execution, and physical kinematics mapping.
- **Hardware Telemetry Streaming:** Non-blocking UART/Serial parsing for incoming ESP32-C3 JSON packets.
- **Configurable Kinematics:** Joint offsets, inversion flags, and motion bounds managed via external JSON configuration (`config/joints.json`).
- **Edge Deployment Ready:** Operates entirely locally with zero internet dependency.

---

## System Architecture

```text
  [ HS-1 Body Suit ]            [ AI Core Engine ]           [ Physical Actuation ]
(ESP32-C3 + BNO055 IMU)        (ONNX Policy Execution)      (Servo Mapping / PWM)
          │                               │                            │
          ▼                               ▼                            ▼
  [ serial_reader ] ──► [ bno055_mapper ] ──► [ onnx_engine ] ──► [ servo_mapper ] ──► Servos
    (UART Data)          (Vector [1x112])       (Actions [1x8])     (PWM / Degrees)


```
## Project Structure
```
MoSy/
├── config/
│   └── joints.json           # Calibration offsets, limits, and servo inversions
├── models/
│   └── mosy_policy.onnx      # Exported PPO actor policy (< 1 MB)
├── src/
│   ├── ai_core/
│   │   └── onnx_engine.py    # ONNX Runtime inference wrapper
│   ├── telemetry/
│   │   ├── bno055_mapper.py  # Formats sensor telemetry into 112-dim state vector
│   │   └── serial_reader.py  # Non-blocking UART JSON packet reader for ESP32-C3
│   └── kinematics/
│       └── servo_mapper.py   # Maps [-1, 1] actions to degrees and PWM pulse widths
├── main.py                   # Main 50 Hz execution loop
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── CHANGELOG.md              # Version history
```



## Quick Start
1. Prerequisites
Ensure you have Python 3.11+ installed.

2. Installation
Clone the repository and install required packages:
```
git clone [https://github.com/Perry1231/MoSy.git](https://github.com/Perry1231/MoSy.git)
cd MoSy
pip install -r requirements.txt
```


## Running the EngineExecute the main control loop:Bashpython main.py
Hardware Specifications
 * Microcontroller: ESP32-C3 (UART / USB-Serial @ 115200 baud)

* IMU Sensor: Bosch BNO055 (Quaternions, Gyroscope, Accelerometer)

* Actuation Driver: PCA9685 16-Channel 12-bit PWM Controller (I2C)

* Actuators: 8× Digital Servos (500us – 2500us pulse width)


## License
Distributed under the APACHE 2.0-License. See LICENSE for more information.

##
Autor : Vladyslav Vytrykush
