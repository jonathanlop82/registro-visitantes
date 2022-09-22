from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime as dt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registro-visitas.db"
db = SQLAlchemy(app)

class Visitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    company = db.Column(db.String(250), nullable=False)
    cid = db.Column(db.String(20), nullable=False)
    date_in = db.Column(db.DateTime, nullable=False)
    date_out = db.Column(db.DateTime)
    status = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Visitas %r>' % self.title

db.create_all()

# visita = Visitas(name='Jonathan Lopez', company='Altaplaza Mall', cid='8-761-825', date_in=dt.datetime.now(), status=True)
# db.session.add(visita)
# db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')




if __name__ == '__main__':
    app.run(debug=True)