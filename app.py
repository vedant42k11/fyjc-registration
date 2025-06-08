from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import random

app = Flask(__name__)
app.secret_key = '6LeJnlkrAAAAAKpbk0rhn2YIpCcatOU7eEfZqW5Q'  # Change this for security

RECAPTCHA_SECRET_KEY = '6LeJnlkrAAAAAKpbk0rhn2YIpCcatOU7eEfZqW5Q'  # Replace with your real key later

registrations = {}

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()
    school = request.form.get('school').strip()
    recaptcha_response = request.form.get('g-recaptcha-response')

    data = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    if not result.get('success'):
        flash('reCAPTCHA verification failed. Please try again.')
        return redirect(url_for('index'))

    verification_code = str(random.randint(100000, 999999))

    registrations[email] = {
        'name': name,
        'school': school,
        'code': verification_code,
        'verified': False
    }

    return render_template('verify.html', email=email, code=verification_code)

@app.route('/verify', methods=['POST'])
def verify():
    email = request.form.get('email')
    input_code = request.form.get('code')

    record = registrations.get(email)
    if record and record['code'] == input_code:
        record['verified'] = True
        return f"Congrats {record['name']}, your registration is verified and complete!"
    else:
        flash("Verification code is incorrect. Try again.")
        return render_template('verify.html', email=email, code="")

if __name__ == '__main__':
    app.run(debug=True)
