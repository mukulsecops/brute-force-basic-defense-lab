from flask import Flask, request, session, redirect, url_for, render_template
from datetime import datetime
import defense

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Toggle Security
ACTIVATE_SECURITY=True

# Hardcoded credentails
USERNAME="admin"
PASSWORD="password"


# Helpers
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For")
    return request.remote_addr


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login/", methods=['GET', 'POST'])
def login():
    error = None
    ip = get_client_ip()

    if ACTIVATE_SECURITY:

        if defense.is_ip_blocked(ip):
            defense.ip_block_attempt_log(ip)
            return "IP Temporarily Blocked", 403
        
        if not defense.check_rate_limit(ip):
            defense.rate_limit_log(ip)
            return "Too many requests", 429

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["user"] = username

            defense.auth_log_success(ip, username)
            return redirect(url_for("dashboard"))
        else:
            defense.auth_log_failure(ip, username)

            if ACTIVATE_SECURITY:
                defense.track_failed_attempt(ip)

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
    app.run(host="0.0.0.0", port=5000, debug=True)