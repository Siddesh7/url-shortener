from logging import warning
from flask import flash
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random


app = Flask(__name__)
app.secret_key = 'sssssrfgvv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Shortener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lin = db.Column(db.String(100))
    surl = db.Column(db.String(100))


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        short = ""
        lurl = request.form.get("longurl")
        desired_link = request.form.get("did")
        found = Shortener.query.filter_by(surl=desired_link).first()
        print(found)
        if desired_link != "" and found == None:
            short = desired_link
        else:
            short = ''.join(random.choices(
                string.ascii_letters, k=6))
        final = request.host_url+short
        new_link = Shortener(lin=lurl, surl=short)
        db.session.add(new_link)
        db.session.commit()
        return render_template("base.html", li=final)
    return render_template("base.html")


@app.route("/<short>")
def red(short):
    redirect_link = Shortener.query.filter_by(surl=short).first()
    return redirect(redirect_link.lin)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
