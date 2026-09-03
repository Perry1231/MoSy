---

## [0.1.0] - 2026-09-02

### Added
- Exported and validated `mosy_policy.onnx` policy generated from the `sb3/ppo-Ant-v3` Reinforcement Learning model.
- Created `test_onnx.py` verification script for runtime verification of input (`[1, 112]`) and output (`[1, 8]`) tensors using `onnxruntime`.
- Built project documentation infrastructure, including English `README.md`, `CHANGELOG.md`, and initial GitHub Wiki pages.

### Changed
- Refactored `download_and_convert.py` to extract only the deterministic actor policy (`action_net`), isolating inference from stochastic probability distributions (`Normal`).
- Isolated Python runtime dependencies on drive `D:\` to optimize disk I/O and build footprint.

### Fixed
- Bypassed PyTorch `torch.export` dynamic graph export failure (`GuardOnDataDependentSymNode`) by enforcing `dynamo=False` legacy TorchScript export.
- Resolved `ModuleNotFoundError: No module named 'gym'` compatibility error by installing `shimmy` and legacy `gym<0.26.0` bindings.
- Fixed Windows disk space allocation failure (`OSError: [Errno 28] No space left on device`) by redirecting pip cache and temporary directories to `D:\Python311\temp`.
---

## [0.2.0] - 2026-09-03

### Added
- Created `src/kinematics/servo_mapper.py` module to convert normalized action values `[-1.0, 1.0]` into physical joint degrees (`0° - 180°`) and PWM pulse widths (`500us - 2500us`).
- Integrated `ServoMapper` into `main.py` execution pipeline for real-time actuation command generation.
- Added package initialization files (`src/__init__.py`, `src/ai_core/__init__.py`, `src/telemetry/__init__.py`, `src/kinematics/__init__.py`).

### Fixed
- Resolved `ModuleNotFoundError: No module named 'src'` in `main.py` by adding explicit project root directory resolution to `sys.path`.

---

## [0.3.0] - 2026-09-03

### Added
- Implemented `main.py` execution loop integrating telemetry formatting and ONNX inference.
- Verified real-time performance (< 0.1 ms inference latency at 50 Hz target control frequency).

---

## [0.4.0] - 2026-09-03

### Added
- Installed `onnxruntime` and `pyserial` dependencies on isolated drive `D:\`.
- Created `src/ai_core/onnx_engine.py` for modular ONNX policy inference wrapper.
- Created `src/telemetry/bno055_mapper.py` to format BNO055 IMU streams into 112-element observation vectors.

---

## [0.5.0] - 2026-09-02

### Added
- Exported and validated `mosy_policy.onnx` policy generated from the `sb3/ppo-Ant-v3` Reinforcement Learning model.
- Created `test_onnx.py` verification script for runtime verification of input (`[1, 112]`) and output (`[1, 8]`) tensors using `onnxruntime`.
- Built project documentation infrastructure, including English `README.md`, `CHANGELOG.md`, and initial GitHub Wiki pages.

### Changed
- Refactored `download_and_convert.py` to extract only the deterministic actor policy (`action_net`), isolating inference from stochastic probability distributions (`Normal`).
- Isolated Python runtime dependencies on drive `D:\` to optimize disk I/O and build footprint.

### Fixed
- Bypassed PyTorch `torch.export` dynamic graph export failure (`GuardOnDataDependentSymNode`) by enforcing `dynamo=False` legacy TorchScript export.
- Resolved `ModuleNotFoundError: No module named 'gym'` compatibility error by installing `shimmy` and legacy `gym<0.26.0` bindings.
- Fixed Windows disk space allocation failure (`OSError: [Errno 28] No space left on device`) by redirecting pip cache and temporary directories to `D:\Python311\temp`.

---

## [0.6.0] - 2026-09-03
### Added
- Implemented `src/telemetry/serial_reader.py` for non-blocking UART telemetry packet parsing from ESP32-C3 microcontrollers over USB/Serial.
- Added `config/joints.json` to manage joint calibration offsets, inversion flags, and motion bounds.
- Added `requirements.txt` to define core Python dependencies (`onnxruntime`, `pyserial`, `numpy`).

### Changed
- Updated `README.md` with complete system architecture, clean hardware specifications, and project setup instructions.
- Cleaned up local Git history and repository structure to prevent cache artifacts.