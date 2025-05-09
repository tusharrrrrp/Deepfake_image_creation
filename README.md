# Deepfake_image_creation
# DeepSwapX

DeepSwapX is a face-swapping application with a secure user authentication system. It allows users to swap faces between two images for educational, research, and personal entertainment purposes only.

![DeepSwapX Banner](https://via.placeholder.com/800x200?text=DeepSwapX)

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

![Login Screen](![WhatsApp Image 2025-05-02 at 19 24 49_cf9b56b4](https://github.com/user-attachments/assets/1f5a35e0-e7d0-4adb-ac33-5a47f41ee7d2)
)
![DeepSwap Interface](https://via.placeholder.com/400x300?text=DeepSwap+Interface)

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
