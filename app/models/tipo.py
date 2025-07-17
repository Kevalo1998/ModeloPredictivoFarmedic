from app.db import get_db

class Tipo:
    def crear(self, nombre):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_tip_prod FROM tipo_producto WHERE nombre=%s", (nombre,))
        if cur.fetchone():
            return 'noadd'
        cur.execute("INSERT INTO tipo_producto(nombre) VALUES (%s)", (nombre,))
        db.commit()
        return 'add'
    def buscar(self, consulta=''):
        db = get_db()
        cur = db.cursor()
        if consulta:
            cur.execute("SELECT * FROM tipo_producto WHERE nombre LIKE %s", (f"%{consulta}%",))
        else:
            cur.execute("SELECT * FROM tipo_producto WHERE nombre NOT LIKE '' ORDER BY id_tip_prod LIMIT 25")
        return cur.fetchall()
    def borrar(self, id):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM tipo_producto WHERE id_tip_prod=%s", (id,))
            db.commit()
            return 'borrado'
        except:
            return 'noborrado'
    def editar(self, nombre, id_editado):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE tipo_producto SET nombre=%s WHERE id_tip_prod=%s", (nombre, id_editado))
        db.commit()
        return 'edit'
    def rellenar_tipos(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM tipo_producto ORDER BY nombre ASC")
        return cur.fetchall()
