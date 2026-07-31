import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_addresses, smtp_server, from_address, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = ", ".join(to_addresses)
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=attachment_path.split("\\")[-1])

    with smtplib.SMTP(smtp_server) as server:
        server.send_message(msg)

if __name__ == "__main__":
    send_email(
        subject="ETL Job Status",
        body="The pipeline completed successfully.",
        to_addresses=["verzonjayson2@gmail.com"],
        smtp_server=("smtp.office365.com", 587),
        from_address="jverzon@bsmhealth.org",
    )