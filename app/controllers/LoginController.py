from flask import Blueprint, render_template, request, redirect, session, url_for
import pymysql
login_bp = Blueprint('login', __name__)
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='farmedic',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
@login_bp.route('/', methods=['GET'])
def index():
    if 'us_tipo' in session:
        return redirect(url_for('login.catalogo'))
    return redirect(url_for('login.login'))
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM usuario 
                INNER JOIN tipo_us ON us_tipo = id_tipo_us 
                WHERE dni_us = %s AND contrasena_us = %s
            """, (dni, password))
            user = cursor.fetchone()
        conn.close()
        if user:
            session['usuario'] = user['id_usuario']
            session['us_tipo'] = user['us_tipo']
            session['nombre_us'] = user['nombre_us']
            return redirect(url_for('login.catalogo'))
        else:
            error = "Credenciales inválidas"
    
    return render_template('login.html', error=error)
@login_bp.route('/catalogo')
def catalogo():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('adm_catalogo.html', nombre=session.get('nombre_us'))
@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))