from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
import json
from datetime import datetime
from app.db import get_db

compra_bp = Blueprint('compra', __name__, url_prefix='/compra')

@compra_bp.route('/realizar', methods=['GET'])
def realizar():
    if 'us_tipo' not in session:
        return redirect(url_for('login.login'))
    return render_template('adm_compra.html', tipo_usuario=session['us_tipo'], nombre=session.get('nombre_us'))


@compra_bp.route('/registrar', methods=['POST'])
def registrar_compra():
    """
    Registra una compra (venta) y reparte los productos en lotes FIFO según vencimiento.
    """
    db = get_db()
    cur = db.cursor()

    try:
        # 1. Obtener datos del formulario
        total = request.form.get('total')
        nombre = request.form.get('nombre')
        dni = request.form.get('dni')
        productos = json.loads(request.form.get('json', '[]'))
        vendedor = session.get('usuario')
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 2. Insertar cabecera de venta
        cur.execute("""
            INSERT INTO venta (fecha, cliente, dni, total, vendedor)
            VALUES (%s, %s, %s, %s, %s)
        """, (fecha, nombre, dni, total, vendedor))
        id_venta = cur.lastrowid

        db.begin()

        # 3. Procesar cada producto
        for prod in productos:
            cantidad = prod['cantidad']
            id_prod = prod['id']
            precio = prod['precio']

            while cantidad > 0:
                cur.execute("""
                    SELECT id_lote, stock, vencimiento, lote_id_prov
                    FROM lote
                    WHERE lote_id_prod = %s
                      AND vencimiento = (
                        SELECT MIN(vencimiento)
                        FROM lote
                        WHERE lote_id_prod = %s
                    )
                    FOR UPDATE
                """, (id_prod, id_prod))
                lote = cur.fetchone()

                if not lote:
                    raise Exception(f"Sin stock para el producto ID: {id_prod}")

                id_lote, stock, vencimiento, id_proveedor = lote

                if cantidad <= stock:
                    cur.execute("""
                        INSERT INTO detalle_venta (det_cantidad, det_vencimiento, id_det_lote, id_det_prod, lote_id_prov, id_det_venta)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (cantidad, vencimiento, id_lote, id_prod, id_proveedor, id_venta))

                    if cantidad == stock:
                        cur.execute("DELETE FROM lote WHERE id_lote = %s", (id_lote,))
                    else:
                        cur.execute("UPDATE lote SET stock = stock - %s WHERE id_lote = %s", (cantidad, id_lote))
                    
                    cantidad = 0
                else:
                    cur.execute("""
                        INSERT INTO detalle_venta (det_cantidad, det_vencimiento, id_det_lote, id_det_prod, lote_id_prov, id_det_venta)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (stock, vencimiento, id_lote, id_prod, id_proveedor, id_venta))
                    cur.execute("DELETE FROM lote WHERE id_lote = %s", (id_lote,))
                    cantidad -= stock

            # 4. Insertar venta_producto
            subtotal = prod['cantidad'] * precio
            cur.execute("""
                INSERT INTO venta_producto (cantidad, subtotal, producto_id_producto, venta_id_venta)
                VALUES (%s, %s, %s, %s)
            """, (prod['cantidad'], subtotal, id_prod, id_venta))

        db.commit()
        return jsonify({'estado': 'ok', 'id_venta': id_venta})

    except Exception as e:
        db.rollback()
        try:
            cur.execute("DELETE FROM venta WHERE id_venta = %s", (id_venta,))
            db.commit()
        except:
            pass
        return jsonify({'estado': 'error', 'error': str(e)}), 400