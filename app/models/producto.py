from app.db import get_db
from pymysql import IntegrityError

class Producto:
    def crear(self, nombre, concentracion, adicional, precio, laboratorio, tipo, presentacion, avatar):
        db = get_db()
        cur = db.cursor()
        cur.execute("""SELECT id_producto FROM producto 
                       WHERE nombre=%s AND concentracion=%s AND adicional=%s 
                       AND prod_lab=%s AND prod_tip_prod=%s AND prod_present=%s""",
                    (nombre, concentracion, adicional, laboratorio, tipo, presentacion))
        if cur.fetchone():
            return 'noadd'
        cur.execute("""INSERT INTO producto(nombre, concentracion, adicional, precio, prod_lab, 
                       prod_tip_prod, prod_present, avatar) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (nombre, concentracion, adicional, precio, laboratorio, tipo, presentacion, avatar))
        db.commit()
        return 'add'
    def editar(self, id, nombre, concentracion, adicional, precio, laboratorio, tipo, presentacion):
        db = get_db()
        cur = db.cursor()
        cur.execute("""SELECT id_producto FROM producto WHERE id_producto!=%s AND nombre=%s 
                       AND concentracion=%s AND adicional=%s 
                       AND prod_lab=%s AND prod_tip_prod=%s AND prod_present=%s""",
                    (id, nombre, concentracion, adicional, laboratorio, tipo, presentacion))
        if cur.fetchone():
            return 'noedit'
        cur.execute("""UPDATE producto SET nombre=%s, concentracion=%s, adicional=%s, 
                       precio=%s, prod_lab=%s, prod_tip_prod=%s, prod_present=%s 
                       WHERE id_producto=%s""",
                    (nombre, concentracion, adicional, precio, laboratorio, tipo, presentacion, id))
        db.commit()
        return 'edit'
    def buscar(self, consulta=None):
        db = get_db()
        cur = db.cursor()
        if consulta:
            cur.execute("""SELECT p.id_producto, p.nombre, p.concentracion, p.adicional, p.precio, 
                                  l.nombre AS laboratorio, t.nombre AS tipo, pr.nombre AS presentacion, 
                                  p.avatar, p.prod_lab, p.prod_tip_prod, p.prod_present
                           FROM producto p
                           JOIN laboratorio l ON p.prod_lab = l.id_laboratorio
                           JOIN tipo_producto t ON p.prod_tip_prod = t.id_tip_prod
                           JOIN presentacion pr ON p.prod_present = pr.id_presentacion
                           WHERE p.nombre LIKE %s LIMIT 25""", (f"%{consulta}%",))
        else:
            cur.execute("""SELECT p.id_producto, p.nombre, p.concentracion, p.adicional, p.precio, 
                                  l.nombre AS laboratorio, t.nombre AS tipo, pr.nombre AS presentacion, 
                                  p.avatar, p.prod_lab, p.prod_tip_prod, p.prod_present
                           FROM producto p
                           JOIN laboratorio l ON p.prod_lab = l.id_laboratorio
                           JOIN tipo_producto t ON p.prod_tip_prod = t.id_tip_prod
                           JOIN presentacion pr ON p.prod_present = pr.id_presentacion
                           ORDER BY p.nombre LIMIT 25""")
        return cur.fetchall()
    def obtener_stock(self, id_producto):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT SUM(stock) AS total FROM lote WHERE lote_id_prod=%s", (id_producto,))
        result = cur.fetchone()
        return result['total'] if result and result['total'] else 0
    def cambiar_logo(self, id_producto, avatar):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE producto SET avatar=%s WHERE id_producto=%s", (avatar, id_producto))
        db.commit()
    def borrar(self, id_producto):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM producto WHERE id_producto=%s", (id_producto,))
            db.commit()
            return 'borrado'
        except IntegrityError:
            return 'noborrado'
    def buscar_por_id(self, id_producto):
        db = get_db()
        cur = db.cursor()
        cur.execute("""SELECT p.id_producto, p.nombre, p.concentracion, p.adicional, p.precio, 
                              l.nombre AS laboratorio, t.nombre AS tipo, pr.nombre AS presentacion, 
                              p.avatar, p.prod_lab, p.prod_tip_prod, p.prod_present
                       FROM producto p
                       JOIN laboratorio l ON p.prod_lab = l.id_laboratorio
                       JOIN tipo_producto t ON p.prod_tip_prod = t.id_tip_prod
                       JOIN presentacion pr ON p.prod_present = pr.id_presentacion
                       WHERE p.id_producto=%s""", (id_producto,))
        return cur.fetchone()