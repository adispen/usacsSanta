from pymongo import MongoClient
from flask import Flask, render_template
from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms import TextField

class santaForm(Form):
	name = TextField('name', validators=[Required()])
	gift = TextField('gift', validators=[Required()])
	email = TextField('email', validators=[Required()])

client = MongoClient('localhost', 27017)
db = client.santa
app = Flask(__name__)
app.config.from_pyfile("santa.cfg")

@app.route("/", methods=["GET", "POST"])
def set():
	form = santaForm()
	if form.validate_on_submit():
		dictionary = {"name":form.name.data, "gift":form.gift.data, "email":form.email.data }
		db.santa.insert(dictionary)
	return render_template("index.html", form = form)

if __name__ == '__main__':
	app.run(debug=True)
