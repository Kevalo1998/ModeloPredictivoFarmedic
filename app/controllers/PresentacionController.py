from flask import Blueprint, request, jsonify
from app.models.presentacion import Presentacion
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
presentacion_bp = Blueprint('presentacion', __name__)
presentacion_model = Presentacion()
@presentacion_bp.route('/presentacion/crear', methods=['POST'])
def crear_presentacion():
    nombre = request.form.get('nombre_presentacion')
    resultado = presentacion_model.crear(nombre)
    return resultado
@presentacion_bp.route('/presentacion/editar', methods=['POST'])
def editar_presentacion():
    nombre = request.form.get('nombre_presentacion')
    id_editado = request.form.get('id_editado')
    resultado = presentacion_model.editar(nombre, id_editado)
    return resultado
@presentacion_bp.route('/presentacion/buscar', methods=['POST'])
def buscar_presentacion():
    consulta = request.form.get('consulta', '')
    datos = presentacion_model.buscar(consulta)
    resultado = [{'id': p['id_presentacion'], 'nombre': p['nombre']} for p in datos]
    return jsonify(resultado)
@presentacion_bp.route('/presentacion/borrar', methods=['POST'])
def borrar_presentacion():
    id_presentacion = request.form.get('id')
    resultado = presentacion_model.borrar(id_presentacion)
    return resultado

@presentacion_bp.route('/presentacion/rellenar', methods=['POST'])
def rellenar_presentaciones():
    datos = presentacion_model.rellenar_presentaciones()
    resultado = [{'id': p['id_presentacion'], 'nombre': p['nombre']} for p in datos]
    return jsonify(resultado)
