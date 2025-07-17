from app.db import get_db
class Lote:
    def crearlote(self, id_producto, proveedor, stock, vencimiento):
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO lote(stock, vencimiento, lote_id_prod, lote_id_prov)
            VALUES (%s, %s, %s, %s)
        """, (stock, vencimiento, id_producto, proveedor))
        db.commit()
        return 'add'

    def buscar(self, consulta=""):
        db = get_db()
        cur = db.cursor()
        if consulta:
            cur.execute("""
                SELECT id_lote, stock, vencimiento, concentracion, adicional,
                       producto.nombre as prod_nom, laboratorio.nombre as lab_nom,
                       tipo_producto.nombre as tip_nom, presentacion.nombre as pre_nom,
                       proveedor.nombre as proveedor, producto.avatar as logo
                FROM lote
                JOIN proveedor ON lote_id_prov = id_proveedor
                JOIN producto ON lote_id_prod = id_producto
                JOIN laboratorio ON prod_lab = id_laboratorio
                JOIN tipo_producto ON prod_tip_prod = id_tip_prod
                JOIN presentacion ON prod_present = id_presentacion
                WHERE producto.nombre LIKE ?
                ORDER BY producto.nombre LIMIT 25
            """, (f'%{consulta}%',))
        else:
            cur.execute("""
                SELECT id_lote, stock, vencimiento, concentracion, adicional,
                       producto.nombre as prod_nom, laboratorio.nombre as lab_nom,
                       tipo_producto.nombre as tip_nom, presentacion.nombre as pre_nom,
                       proveedor.nombre as proveedor, producto.avatar as logo
                FROM lote
                JOIN proveedor ON lote_id_prov = id_proveedor
                JOIN producto ON lote_id_prod = id_producto
                JOIN laboratorio ON prod_lab = id_laboratorio
                JOIN tipo_producto ON prod_tip_prod = id_tip_prod
                JOIN presentacion ON prod_present = id_presentacion
                WHERE producto.nombre != ''
                ORDER BY producto.nombre LIMIT 25
            """)
        
        return [dict(row) for row in cur.fetchall()]
    def editarlote(self, id_lote, stock):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE lote SET stock = ? WHERE id_lote = ?", (stock, id_lote))
        db.commit()
        return 'edit'
    def borrarlote(self, id_lote):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM lote WHERE id_lote = ?", (id_lote,))
        db.commit()
        if cur.rowcount > 0:
            return 'borrado'
        else:
            return 'noborrado'