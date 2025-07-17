from flask import Blueprint, request, jsonify, url_for, current_app
from flask import Blueprint, render_template, session, redirect, url_for
from datetime import datetime
from app.models.laboratorio import Laboratorio
import os, time
laboratorio_bp = Blueprint('laboratorio', __name__)
laboratorio_model = Laboratorio()
@laboratorio_bp.route('/laboratorio/crear', methods=['POST'])
def crear_laboratorio():
    nombre = request.form.get('nombre_laboratorio')
    avatar = 'lab_default.png'
    resultado = laboratorio_model.crear(nombre, avatar)
    return jsonify({'msg': resultado})
@laboratorio_bp.route('/laboratorio/editar', methods=['POST'])
def editar_laboratorio():
    nombre = request.form.get('nombre_laboratorio')
    id_editado = request.form.get('id_editado')
    resultado = laboratorio_model.editar(nombre, id_editado)
    return jsonify({'msg': resultado})
@laboratorio_bp.route('/laboratorio/buscar', methods=['POST'])
def buscar_laboratorios():
    consulta = request.form.get('consulta', '')
    laboratorios = laboratorio_model.buscar(consulta)
    resultado = []
    for lab in laboratorios:
        resultado.append({
            'id': lab['id_laboratorio'],
            'nombre': lab['nombre'],
            'avatar': url_for('static', filename=f'img/lab/{lab["avatar"]}')
        })
    return jsonify(resultado)
laboratorio_bp.route('/laboratorio/cambiar_logo', methods=['POST'])
def cambiar_logo():
    if 'photo' not in request.files:
        return jsonify({'alert': 'noedit'})

    photo = request.files['photo']
    id_laboratorio = request.form.get('id_logo_lab')
    avatar_anterior = request.form.get('avatar')

    if photo.filename == '':
        return jsonify({'alert': 'noedit'})

    ext = os.path.splitext(photo.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        return jsonify({'alert': 'noedit'})

    filename = f"{id_laboratorio}_{str(time.time()).replace('.', '')}{ext}"
    ruta_absoluta = os.path.join(current_app.root_path, 'static', 'img', filename)
    photo.save(ruta_absoluta)

    anteriores = laboratorio_model.cambiar_logo(id_laboratorio, filename)
    if anteriores and anteriores[0]['avatar'] != 'lab_default.png':
        anterior_path = os.path.join(current_app.root_path, 'static', 'img', anteriores[0]['avatar'])
        if os.path.exists(anterior_path):
            os.remove(anterior_path)

    return jsonify({'alert': 'edit', 'ruta': url_for('static', filename=f'img/{filename}')})
@laboratorio_bp.route('/laboratorio/borrar', methods=['POST'])
def borrar_laboratorio():
    id_laboratorio = request.form.get('id')
    resultado = laboratorio_model.borrar(id_laboratorio)
    return jsonify({'msg': resultado})
@laboratorio_bp.route('/laboratorio/rellenar', methods=['POST'])
def rellenar_laboratorios():
    laboratorios = laboratorio_model.rellenar_laboratorios()
    resultado = [{'id': lab['id_laboratorio'], 'nombre': lab['nombre']} for lab in laboratorios]
    return jsonify(resultado)