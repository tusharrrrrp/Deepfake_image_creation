# Deepfake_image_creation
DeepSwapX is a face-swapping application with a secure user authentication system. It allows users to swap faces between two images for educational, research, and personal entertainment purposes only.

#Features:
1)Secure Authentication: Email verification with OTP
2)Face Swapping: Swap faces between source and target images
3)Hardware Options: Choose between CPU and GPU processing
4)Legal Compliance: Built-in legal notices and watermarking

#Installation

Clone the repository:
bash
git clone https://github.com/tusharrrrrp/Deepfake_image_creation.git
cd Deepfake_image_creation

#Install dependencies:
bash
pip install -r requirements.txt

#Configure email settings:
Open main.py
Replace EMAIL_ADDRESS and EMAIL_PASSWORD with your Gmail credentials
Update file paths for user data and logs


#Run the application:
bash
python main.py

#Required Models:
To use the face swapping feature, you need to download and provide an ONNX model. The application supports InsightFace models.

#Usage:
1)Register with email verification
2)Login to your account
3)Upload source image (face to use)
4)Upload target image (where to apply the face)
5)Upload the ONNX model
6)Select processing device (CPU/GPU)
7)Set output filename
8)Agree to legal terms
9)Run the face swap

#Legal Notice:
DeepSwapX is intended solely for educational, research, and personal entertainment purposes. All users must comply with legal requirements, including obtaining consent from individuals appearing in any media used with this software. See full legal notice in the application.

#Requirements:
Python 3.8+
CustomTkinter
OpenCV
InsightFace
ONNX Runtime
See requirements.txt for complete list

#License
This project is licensed under the MIT License - see the LICENSE file for details.

#Disclaimer
The developers of DeepSwapX disclaim all liability for any misuse of this software. Users are solely responsible for ensuring their use complies with all relevant laws and regulations.
