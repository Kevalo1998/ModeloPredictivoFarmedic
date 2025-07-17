from app.db import get_db
from pymysql.err import IntegrityError

class Proveedor:
    def crear(self, nombre, telefono, correo, direccion, avatar):
        db = get_db()
        cur = db.cursor()
        # Verificar si ya existe
        cur.execute("""
            SELECT id_proveedor FROM proveedor WHERE nombre = %s
        """, (nombre,))
        existe = cur.fetchall()
        if existe:
            return 'noadd'
        else:
            try:
                cur.execute("""
                    INSERT INTO proveedor(nombre, telefono, correo, direccion, avatar)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, telefono, correo, direccion, avatar))
                db.commit()
                return 'add'
            except IntegrityError:
                return 'noadd'
    def buscar(self, consulta=None):
        db = get_db()
        cur = db.cursor()

        if consulta:
            cur.execute("""SELECT * FROM proveedor WHERE nombre LIKE %s""", (f"%{consulta}%",))
        else:
            cur.execute("""SELECT * FROM proveedor WHERE nombre NOT LIKE '' ORDER BY id_proveedor DESC LIMIT 25""")

        return cur.fetchall()
    def cambiar_logo(self, id, nombre):
        db = get_db()
        cur = db.cursor()
        cur.execute("UPDATE proveedor SET avatar = %s WHERE id_proveedor = %s", (nombre, id))
        db.commit()
    def borrar(self, id):
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("DELETE FROM proveedor WHERE id_proveedor = %s", (id,))
            db.commit()
            return 'borrado'
        except:
            return 'noborrado'
    def editar(self, id, nombre, telefono, correo, direccion):
        db = get_db()
        cur = db.cursor()

        # Verificar duplicado
        cur.execute("""
            SELECT id_proveedor FROM proveedor WHERE id_proveedor != %s AND nombre = %s
        """, (id, nombre))
        existe = cur.fetchall()

        if existe:
            return 'noedit'
        else:
            cur.execute("""
                UPDATE proveedor SET nombre = %s, telefono = %s, correo = %s, direccion = %s
                WHERE id_proveedor = %s
            """, (nombre, telefono, correo, direccion, id))
            db.commit()
            return 'edit'
    def rellenar_proveedores(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM proveedor ORDER BY nombre ASC")
        return cur.fetchall()