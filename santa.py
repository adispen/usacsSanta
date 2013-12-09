from pymongo import MongoClient
from flask import Flask, render_template, flash, request, redirect
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
		message = "Your request was successfully submitted."
		flash(message)
		dictionary = {"name":form.name.data, "gift":form.gift.data, "email":form.email.data }
	return render_template("index.html", form = form)

@app.route("/posted", methods=["GET", "POST"])
def posted():
	nameIn = request.form.get("name", None)
	gift = request.form.get("gift", None)
	email = request.form.get("email", None)
	returnUser = db.santa.find( { "name" : nameIn.lower() } )
	count = 0
	for item in returnUser:
		count = count + 1
	if count > 0:
		failedmessage = nameIn.capitalize() +  ", you have already submitted a request." 
		flash(failedmessage)
		return render_template("posted.html")
	if nameIn is None or gift is None or email is None:	
		return redirect("/")
	successmessage = 'Your request has been successfully submitted.'
	flash(successmessage)
	db.santa.insert({"name": nameIn.lower(), "gift":gift, "email":email})
	return render_template("posted.html")


if __name__ == '__main__':
	app.run(debug=True)
