from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/download")
def download():
    return render_template("download.html")

if __name__ == "__main__":
    app.run(debug=True)
