from flask import Blueprint, render_template, request, redirect, url_for, jsonify,session
from datetime import datetime
from app.models.usuario import Usuario
usuario_bp = Blueprint('usuario', __name__)
usuario_model = Usuario()
def calcular_edad(fecha_nacimiento):
    hoy = datetime.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
@usuario_bp.route('/usuarios')
def usuarios():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('adm_usuarios.html')
@usuario_bp.route('/datos_personales')
def datos_personales():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('editor_datos_personales.html', nombre=session.get('nombre_us'))
@usuario_bp.route('/usuario/buscar', methods=['POST'])
def buscar_usuario():
    usuario = Usuario()
    id_usuario = request.form['dato']
    datos = usuario.obtener_datos(id_usuario)
    if datos:
        row = datos[0]
        avatar_filename = row['avatar'] if row['avatar'] else 'avatar.png'
        # Convertir la fecha de nacimiento si es necesario
        fecha_nacimiento = row['edad']
        if not isinstance(fecha_nacimiento, datetime):
            try:
                fecha_nacimiento = datetime.strptime(str(fecha_nacimiento), '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                fecha_nacimiento = datetime.strptime(str(fecha_nacimiento), '%Y-%m-%d')
        edad = calcular_edad(fecha_nacimiento)
        result = {
            'id_usuario': row['id_usuario'],
            'nombre': row['nombre_us'],
            'apellidos': row['apellidos_us'],
            'edad': edad,  # ← ya no mostramos la fecha, sino la edad calculada
            'dni': row['dni_us'],
            'contrasena': row['contrasena_us'],
            'tipo': row['nombre_tipo'],
            'telefono': row['telefono_us'],
            'residencia': row['residencia_us'],
            'correo': row['correo_us'],
            'sexo': row['sexo_us'],
            'adicional': row['adicional_us'],
            'avatar': url_for('static', filename=f'img/{row["avatar"]}'),
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'No se encontró el usuario'})
@usuario_bp.route('/usuario/listar', methods=['POST'])
def listar_usuarios():
    consulta = request.form.get('consulta', '')
    usuarios = usuario_model.buscar(consulta)
    resultado = []
    for u in usuarios:
        # Convertir la fecha de nacimiento a objeto datetime si es string
        try:
            fecha_nac = u['edad']
            if not isinstance(fecha_nac, datetime):
                fecha_nac = datetime.strptime(str(fecha_nac), '%Y-%m-%d')
            edad = calcular_edad(fecha_nac)
        except Exception:
            edad = "N/A"

        avatar = u['avatar'] if u['avatar'] else 'avatar.png'
        avatar_url = url_for('static', filename=f'img/{avatar}')

        usuario = {
            'id': u['id_usuario'],
            'nombre': u['nombre_us'],
            'apellidos': u['apellidos_us'],
            'edad': edad,
            'dni': u['dni_us'],
            'tipo': u['nombre_tipo'],
            'tipo_usuario': u['us_tipo'],
            'telefono': u['telefono_us'],
            'residencia': u['residencia_us'],
            'correo': u['correo_us'],
            'sexo': u['sexo_us'],
            'adicional': u['adicional_us'],
            'avatar': avatar_url
        }
        resultado.append(usuario)
    return jsonify(resultado)
@usuario_bp.route('/usuario/capturar', methods=['POST'])
def capturar_datos():
    id_usuario = request.form.get('id_usuario')
    datos = usuario_model.obtener_datos(id_usuario)
    if datos:
        u = datos[0]
        return jsonify({
            'telefono': u['telefono_us'],
            'residencia': u['residencia_us'],
            'correo': u['correo_us'],
            'sexo': u['sexo_us'],
            'adicional': u['adicional_us']
        })
    return jsonify({})
@usuario_bp.route('/usuario/editar', methods=['POST'])
def editar_usuario():
    id_usuario = request.form.get('id_usuario')
    telefono = request.form.get('telefono')
    residencia = request.form.get('residencia')
    correo = request.form.get('correo')
    sexo = request.form.get('sexo')
    adicional = request.form.get('adicional')
    usuario_model.editar(id_usuario, telefono, residencia, correo, sexo, adicional)
    return 'editado'
@usuario_bp.route('/usuario/cambiar_contra', methods=['POST'])
def cambiar_contra():
    id_usuario = request.form.get('id_usuario')
    oldpass = request.form.get('oldpass')
    newpass = request.form.get('newpass')
    resultado = usuario_model.cambiar_contra(id_usuario, oldpass, newpass)
    return resultado
@usuario_bp.route('/usuario/cambiar_foto', methods=['POST'])
def cambiar_foto():
    from werkzeug.utils import secure_filename
    import os, time
    from flask import current_app
    if 'photo' not in request.files:
        return jsonify({'alert': 'noedit'})
    photo = request.files['photo']
    id_usuario = request.form.get('id_usuario')
    if photo.filename == '':
        return jsonify({'alert': 'noedit'})
    ext = os.path.splitext(photo.filename)[1]
    if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
        return jsonify({'alert': 'noedit'})
    # Guardar solo el nombre del archivo, no la ruta completa
    filename = f"{id_usuario}_{str(time.time()).replace('.', '')}{ext}"
    ruta_absoluta = os.path.join(current_app.root_path, 'static', 'img', filename)
    photo.save(ruta_absoluta)
    usuario_model = Usuario()
    anteriores = usuario_model.cambiar_photo(id_usuario, filename)  # <-- solo nombre
    # Eliminar avatar anterior si no es el predeterminado
    if anteriores:
        anterior = anteriores[0][0]
        anterior_path = os.path.join(current_app.root_path, 'static', 'img', anterior)
        try:
            if os.path.exists(anterior_path) and anterior != "avatar.png":
                os.remove(anterior_path)
        except PermissionError:
            print(f"No se pudo eliminar {anterior_path} porque está en uso.")

    return jsonify({'alert': 'edit', 'ruta': url_for('static', filename=f"img/{filename}")})
@usuario_bp.route('/usuario/crear', methods=['POST'])
def crear_usuario():
    data = request.form
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    edad = data.get('edad')
    dni = data.get('dni')
    password = data.get('pass')
    tipo = 4
    avatar = 'default.png'
    usuario_model.crear(nombre, apellido, edad, dni, password, tipo, avatar)
    return jsonify({'msg': 'usuario_creado'})
@usuario_bp.route('/usuario/ascender', methods=['POST'])
def ascender_usuario():
    id_usuario = session.get('usuario')
    pass_admin = request.form.get('pass')
    id_ascendido = request.form.get('id_usuario')
    resultado = usuario_model.ascender(pass_admin, id_ascendido, id_usuario)
    return jsonify({'msg': resultado})
@usuario_bp.route('/usuario/descender', methods=['POST'])
def descender_usuario():
    id_usuario = session.get('usuario')
    pass_admin = request.form.get('pass')
    id_descendido = request.form.get('id_usuario')
    resultado = usuario_model.descender(pass_admin, id_descendido, id_usuario)
    return jsonify({'msg': resultado})
@usuario_bp.route('/usuario/borrar', methods=['POST'])
def borrar_usuario():
    id_usuario = session.get('usuario')
    pass_admin = request.form.get('pass')
    id_borrado = request.form.get('id_usuario')
    resultado = resultado = usuario_model.borrar_usuario(pass_admin, id_borrado, id_usuario)
    return jsonify({'msg': resultado})