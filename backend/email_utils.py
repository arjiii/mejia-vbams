
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_otp(to_email: str, otp: str):
    """
    Sends an OTP to the specified email address using Gmail SMTP.
    Requires SMTP_EMAIL and SMTP_PASSWORD environment variables to be set.
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_email or not smtp_password:
        print("[WARNING] SMTP credentials not set. Email not sent.")
        print(f"[MOCK EMAIL] To: {to_email}, OTP: {otp}")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_email
        msg['To'] = to_email
        msg['Subject'] = "VBAMS Login Verification Code"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2563eb; text-align: center;">Verify Your Login</h2>
                <p>Hello,</p>
                <p>You requested a verification code to access your VBAMS account.</p>
                <div style="background-color: #ffffff; padding: 15px; text-align: center; border-radius: 5px; border: 1px solid #e5e7eb; margin: 20px 0;">
                    <span style="font-size: 24px; font-weight: bold; letter-spacing: 5px; color: #1e40af;">{otp}</span>
                </div>
                <p>This code will expire in 10 minutes.</p>
                <p style="font-size: 12px; color: #6b7280; margin-top: 30px; text-align: center;">
                    If you did not request this code, please ignore this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to server
        print(f"[SMTP] Connecting to smtp.gmail.com...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print(f"[SMTP] Logging in as {smtp_email}...")
        server.login(smtp_email, smtp_password)
        
        # Send
        print(f"[SMTP] Sending email to {to_email}...")
        text = msg.as_string()
        server.sendmail(smtp_email, to_email, text)
        
        # Quit
        server.quit()
        print(f"[SMTP] Email sent successfully.")
        return True
        
    except Exception as e:
        print(f"[SMTP ERROR] Failed to send email: {str(e)}")
        # Fallback to local console for dev convenience if real sending fails
        print(f"[MOCK EMAIL BACKUP] To: {to_email}, OTP: {otp}")
        return False
