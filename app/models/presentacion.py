from app.db import get_db

class Presentacion:
    def crear(self, nombre):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_presentacion FROM presentacion WHERE nombre = %s", (nombre,))
        if cur.fetchone():
            return 'noadd'
        cur.execute("INSERT INTO presentacion(nombre) VALUES (%s)", (nombre,))
        db.commit()
        return 'add'

    def buscar(self, consulta=""):
        db = get_db()
        cur = db.cursor()
        if consulta:
            cur.execute("SELECT * FROM presentacion WHERE nombre LIKE %s", (f"%{consulta}%",))
        else:
            cur.execute("SELECT * FROM presentacion WHERE nombre NOT LIKE '' ORDER BY id_presentacion LIMIT 25")
        return cur.fetchall()

    def borrar(self, id):
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM presentacion WHERE id_presentacion = %s", (id,))
        db.commit()
        if cur.rowcount > 0:
            return 'borrado'
        else:
            return 'noborrado'

    def editar(self, nombre, id_editado):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE presentacion SET nombre = %s WHERE id_presentacion = %s", (nombre, id_editado))
        db.commit()
        return 'edit'

    def rellenar_presentaciones(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM presentacion ORDER BY nombre ASC")
        return cur.fetchall()
