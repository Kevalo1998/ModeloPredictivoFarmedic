from app.db import get_db

class VentaProducto:
    def ver(self, id_venta):
        """
        Devuelve todos los detalles de producto de una venta determinada.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT 
                vp.cantidad,
                vp.subtotal,
                p.nombre            AS producto,
                p.concentracion     AS concentracion,
                l.vencimiento       AS vencimiento,
                lab.nombre          AS laboratorio,
                pres.nombre         AS presentacion,
                tprod.nombre        AS tipo
            FROM venta_producto vp
            JOIN producto p       ON vp.producto_id_producto = p.id_producto
            LEFT JOIN lote l      ON vp.id_det_lote = l.id_lote
            LEFT JOIN laboratorio lab ON p.prod_lab = lab.id_laboratorio
            LEFT JOIN presentacion pres ON p.prod_present = pres.id_presentacion
            LEFT JOIN tipo_producto tprod ON p.prod_tip_prod = tprod.id_tip_prod
            WHERE vp.venta_id_venta = %s
        """, (id_venta,))
        columnas = [c[0] for c in cur.description]
        filas = cur.fetchall()
        return [dict(zip(columnas, fila)) for fila in filas]