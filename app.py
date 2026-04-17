from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devinfotech-secret-key-2026')

# ==================== GMAIL CONFIGURATION ====================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')      # Your Gmail
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')      # App Password (not normal password)
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)
# ============================================================

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

        if not name or not email or not message:
            flash('Please fill all required fields.', 'danger')
            return redirect(url_for('contact'))

        try:
            msg = Message(
                subject=f"New Website Enquiry - {name}",
                recipients=[os.environ.get('MAIL_USERNAME')],   # Your Gmail
                reply_to=email
            )
            
            msg.body = f"""
New Contact Form Submission from DevInfotech Website

Name      : {name}
Email     : {email}
Phone     : {phone}
Company   : {company}

Message:
{message}

---
Sent from: DevInfotech Pvt. Ltd. Website (Bangalore)
Time     : {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            mail.send(msg)
            flash(f'Thank you {name}! Your enquiry has been received. We will contact you shortly.', 'success')
            
        except Exception as e:
            flash('Sorry, there was a problem sending your message. Please try again or email us directly.', 'danger')
            print("Email Error:", str(e))

        return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)