from flask import Blueprint, render_template, session, redirect, url_for,jsonify,request
from datetime import datetime
from app.models.venta import Venta

venta_bp = Blueprint('venta', __name__, url_prefix='/venta')
venta_model = Venta()

@venta_bp.route('/ventas')
def ventas():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))  # Asegúrate que esto coincida con tu blueprint de login
    return render_template('adm_ventas.html', nombre=session.get('nombre_us'))

@venta_bp.route('/listar', methods=['POST'])
def listar_ventas():
    """
    Devuelve el listado completo de ventas (para DataTables, por ejemplo).
    """
    datos = venta_model.buscar()
    # Adaptar a formato DataTables
    return jsonify({'data': datos})

@venta_bp.route('/mostrar_consulta', methods=['POST'])
def mostrar_consulta():
    """
    Devuelve los totales de ventas: por día por vendedor, diaria, mensual y anual.
    """
    usuario_id = session.get('usuario')
    resp = {
        'venta_dia_vendedor': venta_model.venta_dia_vendedor(usuario_id),
        'venta_diaria':       venta_model.venta_diaria(),
        'venta_mensual':      venta_model.venta_mensual(),
        'venta_anual':        venta_model.venta_anual(),
    }
    return jsonify(resp)

@venta_bp.route('/registrar', methods=['POST'])
def crear_venta():
    """
    (Opcional) Ruta sencilla para crear una venta sin distribuir lotes.
    Recibe: fecha, cliente, dni, total, vendedor en form-data.
    """
    fecha    = request.form.get('fecha')    or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cliente  = request.form.get('cliente')
    dni      = request.form.get('dni')
    total    = request.form.get('total')
    vendedor = request.form.get('vendedor') or session.get('usuario')
    nueva_id = venta_model.crear(cliente, dni, total, fecha, vendedor)
    return jsonify({'id_venta': nueva_id})