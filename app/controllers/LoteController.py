from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models.lote import Lote
lote_bp = Blueprint('lote', __name__)
lote_model = Lote()
@lote_bp.route('/lote/crear', methods=['POST'])
def crear_lote():
    id_producto = request.form.get('id_producto')
    proveedor = request.form.get('proveedor')
    stock = request.form.get('stock')
    vencimiento = request.form.get('vencimiento')
    resultado = lote_model.crearlote(id_producto, proveedor, stock, vencimiento)
    return resultado
@lote_bp.route('/lote/editar', methods=['POST'])
def editar_lote():
    id_lote = request.form.get('id')
    stock = request.form.get('stock')
    resultado = lote_model.editarlote(id_lote, stock)
    return resultado
@lote_bp.route('/lote/buscar', methods=['POST'])
def buscar_lotes():
    consulta = request.form.get('consulta', '')
    lotes = lote_model.buscar(consulta)
    resultado = []
    fecha_actual = datetime.now().date()  # Convertido a date
    for lote in lotes:
        vencimiento = lote['vencimiento']  # Es date
        diferencia = vencimiento - fecha_actual
        dias = diferencia.days
        invertido = 1 if dias >= 0 else 0
        dias = abs(dias)
        estado = 'light' if dias > 90 else 'warning'
        if invertido == 0:
            estado = 'danger'
        resultado.append({
            'id': lote['id_lote'],
            'nombre': lote['prod_nom'],
            'concentracion': lote['concentracion'],
            'adicional': lote['adicional'],
            'vencimiento': vencimiento.strftime('%Y-%m-%d'),
            'proveedor': lote['proveedor'],
            'stock': lote['stock'],
            'laboratorio': lote['lab_nom'],
            'tipo': lote['tip_nom'],
            'presentacion': lote['pre_nom'],
            'avatar': f'/static/img/prod/{lote["logo"]}',
            'mes': dias // 30,
            'dia': dias % 30,
            'estado': estado,
            'invert': invertido,
        })

    return jsonify(resultado)
@lote_bp.route('/lote/borrar', methods=['POST'])
def borrar_lote():
    id_lote = request.form.get('id')
    resultado = lote_model.borrarlote(id_lote)
    return resultado