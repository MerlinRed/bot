#!/usr/bin/python3
from flask import Flask

from users_db import update_mail_activated

app = Flask(__name__)


@app.route("/check/mail/<email>")
def mail(email):
    update_mail_activated(email=email)
    return f'Email {email} activated'


if __name__ == "__main__":
    app.run(host='195.2.76.72')
