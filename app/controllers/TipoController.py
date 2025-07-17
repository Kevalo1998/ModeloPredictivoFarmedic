from flask import Blueprint, request, jsonify 
from app.models.tipo import Tipo
tipo_bp = Blueprint('tipo', __name__)
tipo_model = Tipo()
@tipo_bp.route('/tipo/crear', methods=['POST'])
def crear_tipo():
    nombre = request.form.get('nombre_tipo')
    resultado = tipo_model.crear(nombre)
    return jsonify({'msg': resultado})
@tipo_bp.route('/tipo/editar', methods=['POST'])
def editar_tipo():
    nombre = request.form.get('nombre_tipo')
    id_editado = request.form.get('id_editado')
    resultado = tipo_model.editar(nombre, id_editado)
    return jsonify({'msg': resultado})
@tipo_bp.route('/tipo/buscar', methods=['POST'])
def buscar_tipos():
    consulta = request.form.get('consulta', '')
    tipos = tipo_model.buscar(consulta)
    resultado = []
    for t in tipos:
        resultado.append({
            'id': t['id_tip_prod'],
            'nombre': t['nombre']
        })
    return jsonify(resultado)
@tipo_bp.route('/tipo/borrar', methods=['POST'])
def borrar_tipo():
    id_tipo = request.form.get('id')
    resultado = tipo_model.borrar(id_tipo)
    return jsonify({'msg': resultado})
@tipo_bp.route('/tipo/rellenar', methods=['POST'])
def rellenar_tipos():
    tipos = tipo_model.rellenar_tipos()
    resultado = []
    for t in tipos:
        resultado.append({
            'id': t['id_tip_prod'],
            'nombre': t['nombre']
        })
    return jsonify(resultado)
