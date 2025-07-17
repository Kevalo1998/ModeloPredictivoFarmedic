from flask import Blueprint, request, jsonify
from app.models.venta_producto import VentaProducto

venta_producto_bp = Blueprint('venta_producto', __name__, url_prefix='/venta_producto')
vp_model = VentaProducto()

@venta_producto_bp.route('/ver', methods=['POST'])
def ver_detalle_venta():
    """
    Recibe en form-data: `id` (id_venta)
    Devuelve un JSON con el listado de productos de esa venta.
    """
    id_venta = request.form.get('id')
    if not id_venta:
        return jsonify({'error': 'Falta id'}), 400

    detalles = vp_model.ver(id_venta)
    return jsonify(detalles)