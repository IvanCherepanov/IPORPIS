from flask import Flask, render_template
import os

from tasks.task_4.api.main import email_api

app = Flask(__name__)
app.register_blueprint(email_api, url_prefix='/api')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            port=os.environ.get('FLASK_PORT', 5000),
            debug=os.environ.get('FLASK_DEBUG', True))
