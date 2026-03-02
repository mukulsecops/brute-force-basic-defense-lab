import logging
from flask import Flask, request, session, redirect, url_for, render_template
from datetime import datetime

auth_logger = logging.getLogger("auth_logger")
auth_logger.setLevel(logging.INFO)

handler = logging.FileHandler("logs/auth.log")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

handler.setFormatter(formatter)
auth_logger.addHandler(handler)


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Helpers
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For")
    return request.remote_addr


# Hardcoded credentails
USERNAME="admin"
PASSWORD="password"

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login/", methods=['GET', 'POST'])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        ip = get_client_ip()

        if username == USERNAME and password == PASSWORD:
            session["user"] = username

            auth_logger.info(f"SUCCESS LOGIN | IP={ip} | USER={username}")
            return redirect(url_for("dashboard"))
        else:
            auth_logger.warning(f"FAILED LOGIN | IP={ip} | USER={username}")
            error = "Invalid Credentails"
    
    return render_template("login.html", error=error)
    

@app.route("/dashboard/")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)