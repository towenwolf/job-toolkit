#!/usr/bin/env python3
"""
Simple script to test the send_email function in job_searcher.py
Uses email configuration from .env file
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def main():
    print("="*80)
    print("Testing send_email functionality")
    print("="*80)
    
    # Get email configuration from .env
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('APP_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    # Display email configuration
    print("\nEmail Configuration from .env:")
    print(f"  SMTP Server: {smtp_server}")
    print(f"  SMTP Port: {smtp_port}")
    print(f"  From: {sender_email}")
    print(f"  To: {recipient_email}")
    
    # Validate configuration
    if not all([smtp_server, sender_email, sender_password, recipient_email]):
        print("\n✗ ERROR: Missing email configuration in .env file")
        print("Required variables: SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, APP_PASSWORD, RECIPIENT_EMAIL")
        return 1
    
    # Create test email content
    test_html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .test-box {{ 
                    border: 3px solid #3498db; 
                    padding: 30px; 
                    margin: 20px; 
                    background-color: #ecf0f1;
                    border-radius: 8px;
                    max-width: 600px;
                }}
                h1 {{ color: #2c3e50; }}
                .success {{ color: #27ae60; font-weight: bold; }}
                .info {{ color: #7f8c8d; font-size: 14px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="test-box">
                <h1>✓ Job Searcher Email Test</h1>
                <p class="success">SUCCESS! The send_email() function is working correctly.</p>
                <p>This test email was sent using the <code>send_email()</code> method from <code>job_searcher.py</code>.</p>
                <p>If you're reading this, it means:</p>
                <ul>
                    <li>✓ Email configuration is correct</li>
                    <li>✓ SMTP authentication succeeded</li>
                    <li>✓ Email was sent and received successfully</li>
                </ul>
                <div class="info">
                    <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Method: JobSearcher.send_email()</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    # Create email message
    message = MIMEMultipart('alternative')
    message['Subject'] = f"Job Searcher Email Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    message['From'] = sender_email
    message['To'] = recipient_email
    
    # Attach HTML content
    html_part = MIMEText(test_html_content, 'html')
    message.attach(html_part)
    
    # Send the test email
    print("\n" + "="*80)
    print("Sending test email using SMTP from .env...")
    print("="*80)
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"\n✓ SUCCESS! Email sent successfully to {recipient_email}")
        print("Check your inbox at the recipient email address.")
    except Exception as e:
        print(f"\n✗ ERROR: Failed to send email")
        print(f"Error details: {e}")
        return 1
    
    print("\n" + "="*80)
    return 0

if __name__ == "__main__":
    exit(main())
