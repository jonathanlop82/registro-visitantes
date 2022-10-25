from crypt import methods
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registro-visitas.db"
db = SQLAlchemy(app)

app.config["IMAGE_UPLOADS"] = "/Users/tecnologia/WORKDIR/REGISTRO_DE_VISITAS/static/img/images_id/"

class Visitantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    company = db.Column(db.String(250), nullable=False)
    cid = db.Column(db.String(20), unique=True, nullable=False)
    id_image = db.Column(db.String(100), nullable=True)
    

    def __repr__(self):
        return '<Visitantes %r>' % self.name

class Visitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String(20), nullable=False)
    date_in = db.Column(db.DateTime, nullable=False)
    date_out = db.Column(db.DateTime)
    status = db.Column(db.Boolean, nullable=False)
    

    def __repr__(self):
        return '<Visitas %r>' % self.id



db.create_all()

# visitante = Visitantes(name='Jonathan Lopez', company='Altaplaza Mall', cid='8-761-825')
# db.session.add(visitante)
# db.session.commit()

# visita = Visitas(cid='8-761-825', date_in=dt.datetime.now(), status=True)
# db.session.add(visita)
# db.session.commit()


@app.route('/')
def home():
    visits = db.session.query(
         Visitas, Visitantes,
    ).filter(
         Visitas.cid == Visitantes.cid,
    ).filter(
         Visitas.status == True,
    ).all()
    return render_template('index.html', visits=visits)

@app.route('/buscar', methods=['POST','GET'])
def search():
    if request.method == "POST":
        cid = request.form.get("cid")
        visitor_to_find = Visitantes.query.filter_by(cid=cid).first()
        if visitor_to_find:
            return render_template('register.html', visitor=visitor_to_find)
        else:
            flash('Visitante no encontrado')
            return render_template('register.html', cid=cid)

    return render_template('register_search.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        cid = request.form.get("cid")
        name = request.form.get("name")
        company = request.form.get("company")
        # if request.files['image'].filename == '':
        #     print('No hay archivo')
        # else:
        #     print(request.files['image'].filename)
        if request.files:
            # print('UPLOAD')
            image = request.files["image"]
            # print(image + "Uploaded to Faces")
            # flash('Image successfully Uploaded to Faces.')
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            filename = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            id_image = str(image.filename)
        else:
            # print('NOTHING')
            id_image = None
        

        visitor = Visitantes.query.filter_by(cid=cid).first()

        # visits = Visitas.query.filter_by(cid=cid).all()
        visits = db.session.query(Visitas).filter(Visitas.cid == cid).filter(Visitas.status == True).all()

        if not(visitor):
            visitante = Visitantes(name=name, company=company, cid=cid, id_image=id_image)
            db.session.add(visitante)
            db.session.commit()

        if not(visits):
            visita = Visitas(cid=cid, date_in=dt.datetime.now(), status=True)
            db.session.add(visita)
            db.session.commit()
            flash('Registro realizado exitosamente!')
            return redirect(url_for('home'))

        else:
            flash('Existe un registro sin salida registrada!')
            return render_template('register.html')
        

        flash('Registro realizado exitosamente!')
        return render_template('register.html')
    
    return render_template('register.html')

# @app.route('/salida/<int:id>', methods=['POST','GET'])
# def register_out(id):
#     if request.method == "POST":
#         print(id)
#         visit_to_update = Visitas.query.get(id)
#         visit_to_update.date_out = dt.datetime.now()
#         visit_to_update.status = False
#         db.session.commit()

#         return redirect(url_for('home'))

#     return redirect(url_for('home'))

@app.route("/salida/<int:id>",methods=['POST'])
def register_out(id=id):
    visit_to_update = Visitas.query.get(id)
    visit_to_update.date_out = dt.datetime.now()
    visit_to_update.status = False
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)