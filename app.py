from flask import Flask, render_template, request
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

# 📩 Mail Configuration (Gmail SMTP)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'amemitro.official@gmail.com'
app.config['MAIL_PASSWORD'] = 'irzj bthj tidq iwkb'  # App Password
app.config['MAIL_DEFAULT_SENDER'] = 'amemitro.official@gmail.com'

mail = Mail(app)

# 🔌 Local MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",               # <-- Change if using a different MySQL user
        password="Priyal@3470",               # <-- Add your MySQL password here if set
        database="amemitro"        # <-- Make sure this DB exists locally
    )

# 🧾 Inquiry Form (Join Group)
@app.route("/inquiry", methods=["GET", "POST"])
def inquiry():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            area = request.form.get("area")
            phone = request.form.get("phone")
            sangh = request.form.get("sangh")
            info_source = request.form.get("info_source")

            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO informantion (name, area, phone, sangh, info_source)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, area, phone, sangh, info_source))
            conn.commit()
            cursor.close()
            conn.close()

            msg = Message(
                subject="📝 New Ame Mitro Inquiry Submitted",
                recipients=["amemitro.official@gmail.com", "anothermember@gmail.com"],
                body=f"""New form submitted:

Name: {name}
Area: {area}
Phone: {phone}
Sangh: {sangh}
Info Source: {info_source}
"""
            )
            mail.send(msg)

            return render_template("success.html", return_link="/join", message="✅ Thank You! Your form has been submitted successfully.")
        except Exception as e:
            return f"<h2>Error Occurred:</h2><pre>{str(e)}</pre>", 500

    return render_template("form.html")

# 🗣 Feedback Form
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            phone = request.form.get("phone")
            feedback_text = request.form.get("feedback")

            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO informantion (name, phone, feedback)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (name, phone, feedback_text))
            conn.commit()
            cursor.close()
            conn.close()

            msg = Message(
                subject="🗣️ New Feedback Received",
                recipients=["amemitro.official@gmail.com", "anothermember@gmail.com"],
                body=f"""Feedback submitted:

Name: {name}
Phone: {phone}
Feedback: {feedback_text}
"""
            )
            mail.send(msg)

            return render_template("success.html", return_link="/feedback", message="✅ Thank You! Your feedback has been submitted successfully.")
        except Exception as e:
            return f"<h2>Error Occurred:</h2><pre>{str(e)}</pre>", 500

    return render_template("feedback.html")

# 📅 Events Page
@app.route("/events")
def show_events():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events ORDER BY event_date ASC")
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("events.html", events=events)
    except Exception as e:
        return f"<h2>Error loading events:</h2><pre>{str(e)}</pre>", 500

# 🌐 Static Pages
@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/join")
def join():
    return render_template("form.html")

# ✅ Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
