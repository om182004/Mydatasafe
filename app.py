import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------- SECRET KEY --------------------
app.secret_key = "supersecretkey123"  # ⚠️ Change this before deployment

# -------------------- DATABASE CONNECTION --------------------
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    return render_template('index.html')

# -------------------- REGISTER --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return "Username or Email already taken. Please try again."

        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, hashed_password))
            conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.close()
            return "An error occurred during registration. Please try again later."

        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

# -------------------- LOGIN --------------------
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_password = user['password']
            if check_password_hash(stored_password, password):
                session['user'] = user['username']  # Save user session
                return redirect(url_for('dashboard'))
            else:
                return "Invalid password!"
        else:
            return "User not found!"

    return render_template("login.html")

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# -------------------- DASHBOARD --------------------
@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", username=session['user'])

# -------------------- OTHER STATIC PAGES --------------------
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/download")
def download():
    return render_template("download.html")

@app.route("/privacy-tips")
def privacy_tips():
    return render_template("privacy_tips.html")

@app.route("/data-rights")
def data_rights():
    return render_template("data_rights.html")

@app.route("/privacy-tools")
def privacy_tools():
    return render_template("privacy_tools.html")

@app.route("/news-alerts")
def news_alerts():
    return render_template("news_alerts.html")

@app.route('/digital_footprint')
def digital_footprint():
    return render_template('digital_footprint.html')

# -------------------- DIGITAL FOOTPRINT API --------------------
@app.route('/get_user_data')
def get_user_data():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/").json()
        data = {
            "ip": ip,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name"),
            "org": response.get("org"),
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude")
        }
    except Exception as e:
        print("Error fetching IP info:", e)
        data = {"ip": ip, "city": "Unknown", "region": "Unknown", "country": "Unknown"}

    return jsonify(data)

# -------------------- PRIVACY TOOLS DETAIL PAGES --------------------
@app.route('/privacy-tools/password-managers')
def password_managers():
    return render_template('tools/password_managers.html')

@app.route('/privacy-tools/vpns')
def vpns():
    return render_template('tools/vpns.html')

@app.route('/privacy-tools/two-factor-auth')
def two_factor_auth():
    return render_template('tools/two_factor_auth.html')

@app.route('/privacy-tools/private-browsers')
def private_browsers():
    return render_template('tools/private_browsers.html')

@app.route('/privacy-tools/encrypted-storage')
def encrypted_storage():
    return render_template('tools/encrypted_storage.html')

@app.route('/privacy-tools/data-cleaners')
def data_cleaners():
    print("Accessing Data Cleaners page")
    return render_template('tools/data_cleaners.html')

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
