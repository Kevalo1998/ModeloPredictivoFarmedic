from flask import Blueprint, render_template, session, redirect, url_for

prediccion_bp = Blueprint('prediccion', __name__)

@prediccion_bp.route('/predicciones')
def predicciones():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('adm_prediccion.html', tipo_usuario=session['us_tipo'], nombre=session.get('nombre_us'))