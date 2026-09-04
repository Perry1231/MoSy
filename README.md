
# MoSy — Motion Sync Edge AI Engine

**MoSy** is a high-performance, ultra-low latency Edge AI motion control framework designed for quadrupedal robots. It bridges the gap between real-time body motion capture telemetry from the **HS-1 suit** (ESP32-C3 + BNO055 IMU sensors) and physical quadruped robot actuation via a 16-channel PCA9685 I2C servo controller running a strict 50 Hz control loop.

---

## Key Features

- **Ultra-Low Latency Inference:** Executes neural network policy decisions in **< 0.1 ms** using `onnxruntime`.
- **HS-1 Suit Telemetry Support:** Native parsing and normalization of multi-segment Euler angle data (`shoulder`, `forearm`, `hand`) over UART/Serial.
- **Hardware Agnostic & Dry-Run Fallback:** Seamlessly operates with or without physical I2C/UART hardware connected for rapid simulation and benchmarking.
- **Configurable Kinematics:** Joint offsets, motion bounds, and servo inversion flags are decoupled into external JSON configurations (`config/joints.json`).
- **Fully Offline & Edge Ready:** Operates completely on local embedded hardware with zero internet dependency.

---

## System Architecture

```text
  [ HS-1 Motion Suit ]           [ MoSy Edge Core ]          [ Physical Actuation ]
(ESP32-C3 + BNO055 IMUs)        (50 Hz AI Control Loop)      (16-Ch I2C Controller)
          │                               │                            │
          ▼                               ▼                            ▼
  [ serial_reader ] ──► [ bno055_mapper ] ──► [ onnx_engine ] ──► [ servo_mapper ] ──► [ pca9685_driver ]
   (UART JSON)            (Vector [1x112])      (Actions [1x8])      (PWM Pulse us)       (8x Servos)

```

---

## Repository Structure

```text
MoSy/
├── config/
│   └── joints.json           # Calibration offsets, limits, and servo inversions
├── models/
│   └── mosy_policy.onnx      # Exported PPO actor policy (< 1 MB)
├── src/
│   ├── ai_core/
│   │   └── onnx_engine.py    # ONNX Runtime inference wrapper
│   ├── telemetry/
│   │   ├── bno055_mapper.py  # Formats HS-1 suit Euler telemetry into 112-dim state vector
│   │   └── serial_reader.py  # Non-blocking UART JSON packet reader for ESP32-C3
│   └── kinematics/
│       ├── servo_mapper.py   # Maps [-1, 1] actions to degrees and PWM microsecond pulses
│       └── pca9685_driver.py # I2C hardware driver for PCA9685 PWM servo controller
├── main.py                   # Main 50 Hz execution loop and benchmark suite
├── requirements.txt          # Core Python dependencies
├── README.md                 # Project documentation
└── CHANGELOG.md              # Version history

```

---

## Hardware Specifications

* **Microcontroller:** ESP32-C3 (UART / USB-Serial @ 115200 baud)
* **IMU Sensors:** Bosch BNO055 (Orientation tracking on `shoulder`, `forearm`, `hand`)
* **Actuation Driver:** PCA9685 16-Channel 12-bit PWM Controller (I2C address `0x40`)
* **Actuators:** 8× High-Torque Digital Servos (500us – 2500us pulse width)

### HS-1 Suit Telemetry Format (UART JSON)

```json
{
  "shoulder": {"p": 12.5, "y": 45.0, "r": -3.2},
  "forearm":  {"p": 8.1,  "y": 42.1, "r": -1.0},
  "hand":     {"p": 0.5,  "y": 40.0, "r": 0.0}
}

```

---

## Quick Start Guide

### 1. Requirements

Ensure **Python 3.10+** is installed on your system.

### 2. Installation

Clone the repository and install all required dependencies:

```bash
git clone [https://github.com/Perry1231/MoSy.git](https://github.com/Perry1231/MoSy.git)
cd MoSy
pip install -r requirements.txt

```

### 3. Execution & Testing

Run the main 50 Hz control pipeline:

```bash
python main.py

```

*If no physical ESP32-C3 or PCA9685 hardware is connected, the engine automatically runs in **Simulation / Benchmark Mode**, logging latency metrics.*

---

## License

Distributed under the APACHE-2.0 License. See `LICENSE` for details.
