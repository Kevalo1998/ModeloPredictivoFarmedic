from flask import Blueprint, request, jsonify, url_for, current_app
from flask import Blueprint, render_template, session, redirect, url_for
from flask import jsonify
from app.db import get_db
import os, time
from app.models.producto import Producto
producto_bp = Blueprint('producto', __name__)
producto_model = Producto()
@producto_bp.route('/productos')
def productos():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('adm_productos.html', tipo_usuario=session['us_tipo'], nombre=session.get('nombre_us'))
@producto_bp.route('/producto/crear', methods=['POST'])
def crear_producto():
    data = request.form
    producto_model.crear(
        data.get('nombre'),
        data.get('concentracion'),
        data.get('adicional'),
        data.get('precio'),
        data.get('laboratorio'),
        data.get('tipo'),
        data.get('presentacion'),
        'prod_default.png'
    )
    return 'add'
@producto_bp.route('/producto/editar', methods=['POST'])
def editar_producto():
    data = request.form
    producto_model.editar(
        data.get('id'),
        data.get('nombre'),
        data.get('concentracion'),
        data.get('adicional'),
        data.get('precio'),
        data.get('laboratorio'),
        data.get('tipo'),
        data.get('presentacion')
    )
    return 'edit'
@producto_bp.route('/producto/buscar', methods=['POST'])
def buscar_producto():
    productos = producto_model.buscar()
    resultado = []
    for p in productos:
        stock = producto_model.obtener_stock(p['id_producto'])
        resultado.append({
            'id': p['id_producto'],
            'nombre': p['nombre'],
            'concentracion': p['concentracion'],
            'adicional': p['adicional'],
            'precio': p['precio'],
            'stock': stock,
            'laboratorio': p['laboratorio'],
            'tipo': p['tipo'],
            'presentacion': p['presentacion'],
            'laboratorio_id': p['prod_lab'],
            'tipo_id': p['prod_tip_prod'],
            'presentacion_id': p['prod_present'],
            'avatar': url_for('static', filename=f'img/prod/{p["avatar"]}')
        })
    return jsonify(resultado)
@producto_bp.route('/producto/cambiar_avatar', methods=['POST'])
def cambiar_avatar():
    id_producto = request.form.get('id_logo_prod')
    avatar_anterior = request.form.get('avatar')
    archivo = request.files['photo']

    if archivo and archivo.filename != '':
        extension = os.path.splitext(archivo.filename)[1]
        if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            filename = f"{str(time.time()).replace('.', '')}-{archivo.filename}"
            path = os.path.join(current_app.root_path, 'static', 'img', 'prod', filename)
            archivo.save(path)
            producto_model.cambiar_logo(id_producto, filename)
            if 'prod_default.png' not in avatar_anterior:
                try:
                    os.remove(os.path.join(current_app.root_path, avatar_anterior.strip('/')))
                except:
                    pass
            return jsonify({'ruta': url_for('static', filename=f'img/prod/{filename}'), 'alert': 'edit'})
    return jsonify({'alert': 'noedit'})
@producto_bp.route('/producto/borrar', methods=['POST'])
def borrar_producto():
    id_producto = request.form.get('id')
    resultado = producto_model.borrarip(id_producto)
    return jsonify({'msg': resultado})
@producto_bp.route('/producto/buscar_id', methods=['POST'])
def buscar_id():
    id_producto = request.form.get('id_producto')
    datos = producto_model.buscar_id(id_producto)
    if datos:
        stock = producto_model.obtener_stock(datos['id_producto'])
        datos['stock'] = stock
        datos['avatar'] = url_for('static', filename=f'img/prod/{datos["avatar"]}')
        return jsonify(datos)
    return jsonify({})
@producto_bp.route('/producto/verificar_stock', methods=['POST'])
def verificar_stock():
    productos = request.form.get('productos')
    productos = eval(productos)  #ambiar por json.loads si recibes JSON
    error = 0
    for p in productos:
        stock = producto_model.obtener_stock(p['id'])
        if stock < p['cantidad'] or p['cantidad'] <= 0:
            error += 1
    return str(error)
@producto_bp.route('/producto/info/<int:id>', methods=['GET'])
def info_producto(id):
    db = get_db()
    cursor = db.cursor()

    # Obtener stock actual desde el modelo si ya tienes método
    stock_actual = producto_model.obtener_stock(id)

    # Consultar ventas del mes actual
    cursor.execute("""
        SELECT SUM(dv.cantidad) AS ventas_mes
        FROM detalle_venta dv
        JOIN venta v ON dv.id_venta = v.id_venta
        WHERE dv.id_producto = ? 
        AND strftime('%m', v.fecha) = strftime('%m', 'now')
        AND strftime('%Y', v.fecha) = strftime('%Y', 'now')
    """, (id,))
    row = cursor.fetchone()
    ventas_mes = row['ventas_mes'] if row and row['ventas_mes'] else 0

    return jsonify({
        "stock_actual": stock_actual,
        "ventas_mes": ventas_mes
    })
