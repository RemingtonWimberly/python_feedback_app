from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost/whitlockis'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://exsandmsnlsvbi:06b4212e1133cd4cd77b0b91bd8c98d4d27ab7a674bbb2b56f3060de4ecb7a48@ec2-54-225-234-165.compute-1.amazonaws.com:5432/d8682qsgd1gl2u'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), unique=True)
    customer_email = db.Column(db.String(200), unique=True)
    consultant = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer_name, customer_email, consultant, rating, comments):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.consultant = consultant
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer_name = request.form['customer']
        customer_email = request.form['customer_email']
        consultant = request.form['consultant']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer_name, customer_email, consultant, rating, comments)
        if customer_name == '' or customer_email == '' or consultant == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer_name == customer_name).count() == 0:
            data = Feedback(customer_name, customer_email, consultant, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer_name, customer_email, consultant, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()
