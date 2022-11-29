from crypt import methods
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime as dt
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registro-visitas.db"
db = SQLAlchemy(app)

app.config["IMAGE_UPLOADS"] = "/Users/tecnologia/WORKDIR/REGISTRO-VISITANTES/static/img/images_id/"

class Visitantes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_visitante = db.Column(db.String(250), nullable=False)
    empresa_visitante = db.Column(db.String(250), nullable=False)
    cedula_visitante = db.Column(db.String(20), unique=True, nullable=False)
    imagen_cedula = db.Column(db.String(100), nullable=True)
    

    def __repr__(self):
        return '<Visitantes %r>' % self.name

class Visitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local_id = db.Column(db.Integer, nullable=False)
    visitante_id = db.Column(db.Integer, nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    fecha_salida = db.Column(db.DateTime)
    numero_tiquete = db.Column(db.String(250), nullable=False)
    color_tiquete = db.Column(db.String(250), nullable=False)
    estado_visita = db.Column(db.Boolean, nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return '<Visitas %r>' % self.id

class Locales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_local = db.Column(db.String(250), nullable=False)
    codigo_local = db.Column(db.String(250), nullable=False)
    nivel_local = db.Column(db.String(50), nullable=False)
    telefono_local = db.Column(db.String(50), nullable=True)
    encargado_local = db.Column(db.String(250), nullable=True)
    
    def __repr__(self):
        return '<Locales %r>' % self.nombre_local

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(250), nullable=False)
    correo = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Usuarios %r>' % self.id

with app.app_context():
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
         Visitas.visitante_id == Visitantes.id,
    ).filter(
         Visitas.estado_visita == True,
    ).all()
    return render_template('index.html', visits=visits)

@app.route('/buscar', methods=['POST','GET'])
def search():
    if request.method == "POST":
        cedula_visitante = request.form.get("cid")
        visitor_to_find = Visitantes.query.filter_by(cedula_visitante=cedula_visitante).first()
        if visitor_to_find:
            return render_template('register.html', visitor=visitor_to_find)
        else:
            flash('Visitante no encontrado')
            return render_template('register.html', cedula_visitante=cedula_visitante)

    return render_template('register_search.html')

@app.route('/locales', methods=['POST','GET'])
def agregar_local():
    if request.method == "POST":
        nombre_local = request.form.get("nombre_local")
        numero_local = request.form.get("numero_local")
        nivel = request.form.get("nivel")
        telefono = request.form.get("telefono")
        encargado = request.form.get("encargado")
        nuevo_local = Locales(nombre_local=nombre_local, codigo_local=numero_local, nivel_local=nivel, telefono_local=telefono, encargado_local=encargado)
        db.session.add(nuevo_local)
        db.session.commit()
        flash('Registro realizado exitosamente!')
        return redirect(url_for('agregar_local'))
    return render_template('locales.html')

@app.route('/actualizar_locales')
def actualizar_locales():
    locales = db.session.query(Locales).order_by(Locales.codigo_local).all()

    return render_template('actualizar_locales.html', locales=locales)

@app.route('/editar_local/<int:id>', methods=['POST','GET'])
def editar_local(id=id):
    if request.method == 'POST':
        local_por_actualizar = Locales.query.get(id)
        local_por_actualizar.nombre_local = request.form.get("nombre_local")
        local_por_actualizar.codigo_local = request.form.get("numero_local")
        local_por_actualizar.nivel_local = request.form.get("nivel")
        local_por_actualizar.telefono_local = request.form.get("telefono")
        local_por_actualizar.encargado_local = request.form.get("encargado")
        db.session.commit()
        flash('Registro realizado exitosamente!')
        return redirect(url_for('actualizar_locales'))
    else:
        local = Locales.query.filter_by(id=id).first()
        return render_template('editar_local.html', local=local)

@app.route('/eliminar_locales')
def eliminar_locales():
    locales = db.session.query(Locales).order_by(Locales.codigo_local).all()
    return render_template('eliminar_locales.html', locales=locales)

@app.route('/eliminar_local/<int:id>', methods=['POST','GET'])
def eliminar_local(id=id):
    if request.method == 'POST':
        local_por_eliminar = Locales.query.get(id)
        db.session.delete(local_por_eliminar)
        db.session.commit()
        flash('Registro eliminado exitosamente!')
        return redirect(url_for('eliminar_locales'))
    else:
        return redirect(url_for('eliminar_locales'))






# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == "POST":
#         cid = request.form.get("cid")
#         name = request.form.get("name")
#         company = request.form.get("company")
#         # if request.files['image'].filename == '':
#         #     print('No hay archivo')
#         # else:
#         #     print(request.files['image'].filename)
#         if request.files:
#             # print('UPLOAD')
#             image = request.files["image"]
#             # print(image + "Uploaded to Faces")
#             # flash('Image successfully Uploaded to Faces.')
#             image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
#             filename = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
#             id_image = str(image.filename)
#         else:
#             # print('NOTHING')
#             id_image = None
        

#         visitor = Visitantes.query.filter_by(cid=cid).first()

#         # visits = Visitas.query.filter_by(cid=cid).all()
#         visits = db.session.query(Visitas).filter(Visitas.cid == cid).filter(Visitas.status == True).all()

#         if not(visitor):
#             visitante = Visitantes(name=name, company=company, cid=cid, id_image=id_image)
#             db.session.add(visitante)
#             db.session.commit()

#         if not(visits):
#             visita = Visitas(cid=cid, date_in=dt.datetime.now(), status=True)
#             db.session.add(visita)
#             db.session.commit()
#             flash('Registro realizado exitosamente!')
#             return redirect(url_for('home'))

#         else:
#             flash('Existe un registro sin salida registrada!')
#             return render_template('register.html')
        

#         flash('Registro realizado exitosamente!')
#         return render_template('register.html')
    
#     return render_template('register.html')

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
    app.run(debug=True, host='0.0.0.0')