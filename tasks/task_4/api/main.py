import os
import tempfile

from flask import Blueprint, request, jsonify

from tasks.logger import logger
from tasks.task_4.app.email_func import smtp_servers, send_email
from tasks.task_4.app.file_func import read_csv
from tasks.utils import validate_email

email_api = Blueprint('email_api', __name__)

@email_api.route('/send_emails', methods=['POST'])
def send_emails():
    if 'csv_file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name

            try:
                theme = request.form.get('theme')
                message = request.form.get('message')
                sender_email = request.form.get('sender_email')
                sender_password = request.form.get('sender_password')
                smtp_index = int(request.form.get('smtp_server', '0'))

                smtp_server, smtp_port = smtp_servers[smtp_index]

                if not validate_email(sender_email):
                    return jsonify({"message": f"Email {sender_email} is invalid!"}), 400

                for row in read_csv(temp_file_path):
                    addr_to = row[0].strip()
                    files = [f.strip() for f in row[1:] if f.strip()]

                    if validate_email(addr_to):
                        send_email(addr_to, theme, message, smtp_server, smtp_port, sender_email, sender_password,
                                   files)
                    else:
                        logger.info(f"Invalid email: {addr_to}")

                return jsonify({"message": "Emails sent successfully!"}), 200
            except Exception as e:
                logger.exception(e)
            finally:
                temp_file.close()
                os.unlink(temp_file_path)

    return jsonify({"error": "Failed to process file"}), 500