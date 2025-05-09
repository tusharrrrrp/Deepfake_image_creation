# DeepSwapX

DeepSwapX is a face-swapping application with a secure user authentication system. It allows users to swap faces between two images for educational, research, and personal entertainment purposes only.


## Features

- **Secure Authentication**: Email verification with OTP
- **Face Swapping**: Swap faces between source and target images
- **Hardware Options**: Choose between CPU and GPU processing
- **Legal Compliance**: Built-in legal notices and watermarking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/DeepSwapX.git
cd DeepSwapX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure email settings:
   - Open `ShaktiyaKshama.py`
   - Replace `EMAIL_ADDRESS` and `EMAIL_PASSWORD` with your Gmail credentials
   - Update file paths for user data and logs

4. Run the application:
```bash
python ShaktiyaKshama.py
```

## Required Models

To use the face swapping feature, you need to download and provide an ONNX model. The application supports InsightFace models.

## Usage

1. Register with email verification
2. Login to your account
3. Upload source image (face to use)
4. Upload target image (where to apply the face)
5. Upload the ONNX model
6. Select processing device (CPU/GPU)
7. Set output filename
8. Agree to legal terms
9. Run the face swap

## Legal Notice

DeepSwapX is intended solely for educational, research, and personal entertainment purposes. All users must comply with legal requirements, including obtaining consent from individuals appearing in any media used with this software. See full legal notice in the application.

## Screenshots

[Login Screen]

![WhatsApp Image 2025-05-02 at 19 22 55_4244e344](https://github.com/user-attachments/assets/4e722d5a-df20-4f47-b09c-8c06e4bc3008)


[DeepSwap Interface]


![WhatsApp Image 2025-05-02 at 19 25 13_f4b1a0b7](https://github.com/user-attachments/assets/d8f1bb81-a6fa-400d-aea0-b9c4ae73a2d5)

![WhatsApp Image 2025-05-02 at 19 26 01_9d6e1f3c](https://github.com/user-attachments/assets/f7629d63-088b-405a-8b58-07b8cf04e3a5)


## Requirements

- Python 3.8+
- CustomTkinter
- OpenCV
- InsightFace
- ONNX Runtime
- See requirements.txt for complete list

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

The developers of DeepSwapX disclaim all liability for any misuse of this software. Users are solely responsible for ensuring their use complies with all relevant laws and regulations.
