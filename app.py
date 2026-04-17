from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Secret key from .env file (important for security and flash messages)
app.secret_key = os.environ.get('SECRET_KEY')

# ==================== GMAIL CONFIGURATION (from .env) ====================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)
# =====================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        company = request.form.get('company', '')
        message = request.form.get('message')

        # Basic validation
        if not name or not email or not message:
            flash('Please fill all required fields (Name, Email, and Message).', 'danger')
            return redirect(url_for('contact'))

        try:
            msg = Message(
                subject=f"New Enquiry from DevInfotech Website - {name}",
                recipients=[os.environ.get('MAIL_USERNAME')],
                reply_to=email
            )
            
            msg.body = f"""
New Contact Form Submission

Name      : {name}
Email     : {email}
Phone     : {phone}
Company   : {company}

Message:
{message}

---
Sent from: DevInfotech Pvt. Ltd. Website
Location : Bengaluru, Karnataka, India
Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            mail.send(msg)
            flash(f'Thank you {name}! Your enquiry has been sent successfully. We will contact you within 24 hours.', 'success')
            
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again or email us directly.', 'danger')
            print(f"Email Error: {str(e)}")

        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
