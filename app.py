from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_email():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    msg = EmailMessage()
    msg["Subject"] = "New Website Enquiry"
    msg["From"] = "jazaacov.ms@gmail.com"
    msg["To"] = "Info@jazaaco.com"
    msg["Reply-To"] = email

    msg.set_content(f"""
New Contact Form Submission

Name: {name}
Email: {email}
Phone: {phone}

Message:
{message}
    """)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("jazaacov.ms@gmail.com", "eelz coto bknj oofc")
        smtp.send_message(msg)

    return redirect("/")

## THIS IS FOR THE CV ##
@app.route("/send_cv", methods=["POST"])
def send_cv():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("contact_number")
    email = request.form.get("email")
    location = request.form.get("location")
    prev_job = request.form.get("previous_job")
    
    cv_file = request.files.get("cv_file")

    msg = EmailMessage()
    msg["Subject"] = f"New Job Application: {first_name} {last_name}"
    msg["From"] = "jazaacov.ms@gmail.com"
    msg["To"] = "hr@jazaaco.com"
    msg["Reply-To"] = email

    msg.set_content(f"""
New Job Application Received

Name: {first_name} {last_name}
Email: {email}
Phone: {phone}
Location: {location}

Previous/Current Job:
{prev_job}
    """)

    if cv_file and cv_file.filename:
        file_data = cv_file.read()
        file_name = cv_file.filename
        
        # Add the attachment
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename=file_name
        )

    print(f"Attempting to send CV for {first_name} {last_name}")
    print(f"Attachment: {cv_file.filename if cv_file else 'None'}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("jazaacov.ms@gmail.com", "eelz coto bknj oofc")
            smtp.send_message(msg)
            print("CV Email sent successfully.")
    except Exception as e:
        print(f"Error sending CV email: {e}")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
