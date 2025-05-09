import customtkinter as ctk
import tkinter.messagebox as messagebox
import smtplib
import random
import json
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP credentials
EMAIL_ADDRESS = "YOUR_MAIL_ACCOUNT"
EMAIL_PASSWORD = "GIVEN_IN_YOUR_MAIL_SECURITY"

USERS_DATA_FILE = " "# ADD YOUR DESKTOP PATH
OTP_LOG_FILE = " " # ADD YOUR DESKTOP PATH 
EMAIL_LOG_FILE = " " # ADD YOUR DESKTOP PATH

pending_otps = {}

def load_users_data():
    if os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users_data(data):
    with open(USERS_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_otp_sent(email, otp):
    log_entry = {"email": email, "otp": otp, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    logs = json.load(open(OTP_LOG_FILE)) if os.path.exists(OTP_LOG_FILE) else []
    logs.append(log_entry)
    json.dump(logs, open(OTP_LOG_FILE, "w"), indent=4)

def log_email_status(email, status, error_message=None):
    log_entry = {"email": email, "status": status, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    if error_message:
        log_entry["error"] = error_message
    logs = json.load(open(EMAIL_LOG_FILE)) if os.path.exists(EMAIL_LOG_FILE) else []
    logs.append(log_entry)
    json.dump(logs, open(EMAIL_LOG_FILE, "w"), indent=4)

class RegistrationPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_login):
        super().__init__(master)
        self.switch_to_login = switch_to_login
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Register", font=("Arial", 24)).pack(pady=12)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email"); self.email_entry.pack(pady=6)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*"); self.password_entry.pack(pady=6)
        self.otp_entry = ctk.CTkEntry(self, placeholder_text="Enter OTP"); self.otp_entry.pack(pady=6)
        ctk.CTkButton(self, text="Send OTP", command=self.send_otp).pack(pady=6)
        ctk.CTkButton(self, text="Register", command=self.register_user).pack(pady=6)
        ctk.CTkButton(self, text="Already have an account? Login", command=self.switch_to_login).pack(pady=10)

    def send_otp(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Error", "Email and password required."); return
        otp = str(random.randint(100000, 999999))
        pending_otps[email] = {"otp": otp, "password": password}
        log_otp_sent(email, otp)
        try:
            msg = MIMEMultipart(); msg['From'] = EMAIL_ADDRESS; msg['To'] = email; msg['Subject'] = "Your OTP Code"
            msg.attach(MIMEText(f"Your OTP code is: {otp}", 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587); server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD); server.send_message(msg); server.quit()
            log_email_status(email, status="Success")
            messagebox.showinfo("Success", f"An OTP has been successfully sent from shaktiyakshama@gmail.com to {email}. Please check your inbox (and spam folder if necessary) to retrieve the code and proceed with verification. Thank you for using our application — we appreciate your trust and are committed to keeping your experience secure and smooth.")
        except Exception as e:
            log_email_status(email, status="Failed", error_message=str(e))
            messagebox.showerror("Error", f"Failed to send email: {str(e)}")

    def register_user(self):
        email = self.email_entry.get(); otp_input = self.otp_entry.get()
        if email not in pending_otps:
            messagebox.showerror("Error", "Please send OTP first."); return
        if otp_input == pending_otps[email]['otp']:
            users = load_users_data()
            if email in users:
                messagebox.showerror("Error", "User already registered.")
            else:
                users[email] = pending_otps[email]['password']
                save_users_data(users); del pending_otps[email]
                messagebox.showinfo("Success", "Registration successful."); self.switch_to_login()
        else:
            messagebox.showerror("Error", "Invalid OTP.")

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_register, switch_to_deepswap):
        super().__init__(master)
        self.switch_to_register = switch_to_register
        self.switch_to_deepswap = switch_to_deepswap
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Login", font=("Arial", 24)).pack(pady=12)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email"); self.email_entry.pack(pady=6)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*"); self.password_entry.pack(pady=6)
        ctk.CTkButton(self, text="Login", command=self.login_user).pack(pady=6)
        ctk.CTkButton(self, text="Don't have an account? Register", command=self.switch_to_register).pack(pady=10)

    def login_user(self):
        email = self.email_entry.get(); password = self.password_entry.get(); users = load_users_data()
        if email in users and users[email] == password:
            messagebox.showinfo("Success", f"Welcome back, {email}!")
            self.switch_to_deepswap()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

class AuthApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login System")
        self.geometry("400x400")
        self.switch_to_login()

    def switch_to_register(self):
        self.clear_widgets()
        self.registration_page = RegistrationPage(self, self.switch_to_login)
        self.registration_page.pack(fill="both", expand=True)

    def switch_to_login(self):
        self.clear_widgets()
        self.login_page = LoginPage(self, self.switch_to_register, self.launch_deepswap_app)
        self.login_page.pack(fill="both", expand=True)

    def clear_widgets(self):
        for widget in self.winfo_children(): widget.destroy()

    def launch_deepswap_app(self):
        self.destroy()
        DeepSwapApp().mainloop()

# === DEEPFAKE APP ===
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import cv2
import numpy as np
import os
import psutil
import GPUtil
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model
import threading
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DeepSwapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DeepSwapX - Face Swapping Lab")
        self.geometry("700x600")
        self.resizable(False, False)

        self.source_path = None
        self.target_path = None
        self.model_path = None
        self.output_name = ctk.StringVar(value="swapped.jpg")
        self.device = tk.StringVar(value="CPU")
        self.sys_label = None

        self.build_ui()
        self.start_monitoring()

    def build_ui(self):
        ctk.CTkLabel(self, text="DeepSwapX - Face Swapping Lab", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        file_frame = ctk.CTkFrame(self)
        file_frame.pack(pady=10, fill="x", padx=20)

        self.source_label = ctk.CTkLabel(file_frame, text="No source image uploaded")
        self.source_label.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(file_frame, text="Upload Source Image", command=self.load_source).grid(row=1, column=0, padx=10, pady=10)

        self.target_label = ctk.CTkLabel(file_frame, text="No target image uploaded")
        self.target_label.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(file_frame, text="Upload Target Image", command=self.load_target).grid(row=1, column=1, padx=10, pady=10)

        self.model_label = ctk.CTkLabel(file_frame, text="No ONNX model uploaded")
        self.model_label.grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkButton(file_frame, text="Upload ONNX Model", command=self.load_model).grid(row=1, column=2, padx=10, pady=10)

        config_frame = ctk.CTkFrame(self)
        config_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(config_frame, text="Processing Device:").grid(row=0, column=0, padx=10)
        ctk.CTkOptionMenu(config_frame, values=["CPU", "GPU"], variable=self.device).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(config_frame, text="Output Filename:").grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkEntry(config_frame, textvariable=self.output_name).grid(row=1, column=1, padx=10, pady=10)

        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, orientation="horizontal", width=300)
        self.progress_bar.grid(row=0, column=0, padx=5)
        self.progress_bar.set(0)

        #
        #self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        #self.progress_bar.pack(pady=5)
        #self.progress_bar.set(0)  # Start at 0%
#
        self.sys_label = ctk.CTkLabel(self, text="CPU: 0% used | GPU: 0% used", font=ctk.CTkFont(size=14))
        self.sys_label.pack(pady=5)

        ctk.CTkButton(self, text="🔄 Start Face Swap", command=self.run_swap_thread, fg_color="#1f6aa5").pack(pady=15)

    def load_source(self):
        self.source_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if self.source_path:
            self.source_label.configure(text=f"Source Image: {os.path.basename(self.source_path)}")

    def load_target(self):
        self.target_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if self.target_path:
            self.target_label.configure(text=f"Target Image: {os.path.basename(self.target_path)}")

    def load_model(self):
        self.model_path = filedialog.askopenfilename(filetypes=[("ONNX Model", "*.onnx")])
        if self.model_path:
            self.model_label.configure(text=f"ONNX Model: {os.path.basename(self.model_path)}")

    def run_swap_thread(self):
        threading.Thread(target=self.show_legal_notice, daemon=True).start()

    def show_legal_notice(self):
        legal_popup = ctk.CTkToplevel(self)
        legal_popup.title("Legal Notice Agreement")
        legal_popup.geometry("600x500")
        legal_popup.grab_set()

        frame = ctk.CTkFrame(legal_popup)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.textbox = ctk.CTkTextbox(frame, wrap="word", height=350)
        self.textbox.pack(fill="both", expand=True)

        long_notice = """LEGAL NOTICE:
        
Welcome to DeepSwapX. Please carefully read the following legal disclaimer before using this software.

1. Purpose:
This software is intended solely for educational, research, and personal entertainment purposes. You must not use this software to create misleading content, harm the reputation of others, commit fraud, or violate any applicable law or regulation.

2. Consent:
You must have the consent of individuals appearing in any media used with this software. Unauthorized use of someone's likeness without permission may violate their rights.

3. Responsibility:
You are solely responsible for any content you create using DeepSwapX. The creators, developers, and distributors of DeepSwapX disclaim all liability for any misuse.

4. Data Usage:
No data (images, models, results) is stored or transmitted externally by DeepSwapX. All processing occurs locally on your machine.

5. No Warranty:
DeepSwapX is provided "as-is" without any warranties, expressed or implied. The developers are not liable for any damages arising from its use.

6. Restrictions:
- No use for deepfake pornography.
- No use for harassment, bullying, defamation.
- No impersonation of individuals for malicious purposes.

7. Legal Compliance:
You must ensure that your use of DeepSwapX complies with all relevant local, national, and international laws.

By scrolling down and agreeing, you acknowledge that you understand and accept all terms and conditions stated above. Unauthorized or illegal use may expose you to civil and criminal liability.
"""  # Tripled to make it longer for scroll

        self.textbox.insert(tk.END, long_notice)
        self.textbox.configure(state="disabled")

        self.textbox.bind("<Motion>", self.check_scroll)
        self.textbox.bind("<ButtonRelease-1>", self.check_scroll)

        self.agree_var = tk.BooleanVar(value=False)  # Default to unchecked

        self.agree_checkbox = ctk.CTkCheckBox(frame, text="I Agree to the Terms", variable=self.agree_var, text_color="#000000")
        self.proceed_button = ctk.CTkButton(frame, text="Proceed", command=lambda: self.proceed_after_agreement(legal_popup))

        # Pack the checkbox and button immediately when the popup appears
        self.agree_checkbox.pack(pady=10)
        self.proceed_button.pack(pady=10)

    def check_scroll(self, event=None):
        if self.textbox.yview()[1] == 1.0:  # Scrolled to bottom
            pass  # No longer waiting for scrolling, just showing checkbox/button

    def proceed_after_agreement(self, popup_window):
        if self.agree_var.get():
            popup_window.destroy()
            threading.Thread(target=self.run_swap, daemon=True).start()
        else:
            messagebox.showwarning("Agreement Required", "Please agree to the terms before proceeding.")

    def run_swap(self):
        if not all([self.source_path, self.target_path, self.model_path]):
            messagebox.showerror("Missing Input", "Please upload all required files.")
            return

        try:
            # Simulate face swapping process
            self.update_percentage(10)

            # Loading images
            img1 = cv2.imread(self.source_path)
            img2 = cv2.imread(self.target_path)
            self.update_percentage(20)

            ctx_id = 0 if self.device.get() == "GPU" else -1
            providers = ['CUDAExecutionProvider'] if ctx_id == 0 else ['CPUExecutionProvider']
            app = FaceAnalysis(name="buffalo_l")
            app.prepare(ctx_id=ctx_id, det_size=(640, 640))
            model = get_model(self.model_path, providers=providers)
            self.update_percentage(40)

            faces1 = app.get(img1)
            faces2 = app.get(img2)
            self.update_percentage(60)

            if not faces1 or not faces2:
                messagebox.showerror("Detection Error", "No faces detected in one or both images.")
                return

            result_img = model.get(img1, faces1[0], faces2[0])
            self.update_percentage(80)

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = "For Educational Use Only"
            height, width = result_img.shape[:2]
            scale = max(0.5, min(2.0, height / 800))
            thickness = max(1, int(scale * 2))
            (text_w, text_h), _ = cv2.getTextSize(text, font, scale, thickness)
            x = width - text_w - 10
            y = height - 10

            overlay = result_img.copy()
            cv2.putText(overlay, text, (x, y), font, scale, (0, 0, 255), thickness, cv2.LINE_AA)
            alpha = 0.35
            cv2.addWeighted(overlay, alpha, result_img, 1 - alpha, 0, result_img)

            #output_path = os.path.join(os.getcwd(), self.output_name.get())
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop_path, self.output_name.get())
            cv2.imwrite(output_path, result_img)
            self.update_percentage(100)

            messagebox.showinfo("Success", f"Face Swap completed! Image saved to {output_path}")
            self.clear_inputs()
            self.update_percentage(0)  # Reset progress bar
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    #def update_percentage(self, percentage):
    #    self.after(0, self.progress_bar.set, percentage / 100)
    #    self.after(0, self.percentage_label.configure, {"text": f"{percentage}%"})
    #    self.update()
    def update_percentage(self, percentage):
        if hasattr(self, "progress_bar"):
            self.after(0, self.progress_bar.set, percentage / 100)
        self.update()


    def update_system_stats(self):
        try:
            if self.device.get() == "GPU":
                gpus = GPUtil.getGPUs()
                if gpus:
                    usage = f"GPU {gpus[0].id}: {gpus[0].load * 100:.2f}% used, Mem {gpus[0].memoryUtil * 100:.2f}%"
                else:
                    usage = "GPU not detected"
            else:
                cpu_usage = psutil.cpu_percent()
                memory_usage = psutil.virtual_memory().percent
                usage = f"CPU: {cpu_usage:.2f}% used, RAM: {memory_usage:.2f}% used"

            self.sys_label.configure(text=usage)
        except Exception as e:
            self.sys_label.configure(text=f"Error: {e}")

        self.after(2000, self.update_system_stats)  # Update every 2 seconds

    def start_monitoring(self):
        # Start the background thread for system stats monitoring
        threading.Thread(target=self.update_system_stats, daemon=True).start()

    def clear_inputs(self):
        self.source_path = None
        self.target_path = None
        self.model_path = None
        self.output_name.set("swapped.jpg")
        self.source_label.configure(text="No source image uploaded")
        self.target_label.configure(text="No target image uploaded")
        self.model_label.configure(text="No ONNX model uploaded")
        self.agree_var.set(False)
        self.agree_checkbox.pack_forget()
        self.proceed_button.pack_forget()

# === START ===
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = AuthApp()
    app.mainloop()
