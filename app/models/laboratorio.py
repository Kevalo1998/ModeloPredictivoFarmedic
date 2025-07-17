from app.db import get_db
from pymysql import IntegrityError
class Laboratorio:
    def crear(self, nombre, avatar):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_laboratorio FROM laboratorio WHERE nombre = %s", (nombre,))
        if cur.fetchone():
            return 'noadd'
        cur.execute("INSERT INTO laboratorio (nombre, avatar) VALUES (%s, %s)", (nombre, avatar))
        db.commit()
        return 'add'

    def editar(self, nombre, id_editado):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE laboratorio SET nombre = %s WHERE id_laboratorio = %s", (nombre, id_editado))
        db.commit()
        return 'edit'

    def buscar(self, consulta=''):
        db = get_db()
        cur = db.cursor()
        if consulta:
            cur.execute("SELECT * FROM laboratorio WHERE nombre LIKE %s", (f"%{consulta}%",))
        else:
            cur.execute("SELECT * FROM laboratorio WHERE nombre != '' ORDER BY id_laboratorio LIMIT 25")
        return cur.fetchall()

    def cambiar_logo(self, id_laboratorio, nombre):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT avatar FROM laboratorio WHERE id_laboratorio = %s", (id_laboratorio,))
        avatar_anterior = cur.fetchall()
        cur.execute("UPDATE laboratorio SET avatar = %s WHERE id_laboratorio = %s", (nombre, id_laboratorio))
        db.commit()
        return avatar_anterior

    def borrar(self, id):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM laboratorio WHERE id_laboratorio = %s", (id,))
            db.commit()
            return 'borrado'
        except Exception:
            return 'noborrado'
    def rellenar_laboratorios(self):
        db = get_db()
        cur = db.cursor()
        sql = "SELECT id_laboratorio, nombre FROM laboratorio ORDER BY nombre ASC"
        cur.execute(sql)
        return cur.fetchall()