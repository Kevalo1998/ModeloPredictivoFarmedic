from app.db import get_db
class Usuario:
    def __init__(self):
        self.objetos = []
    def obtener_datos(self, id_usuario):
        db = get_db()
        sql = """SELECT * FROM usuario 
                 JOIN tipo_us ON us_tipo = id_tipo_us 
                 WHERE id_usuario = %s"""
        cur = db.cursor()
        cur.execute(sql, (id_usuario,))
        self.objetos = cur.fetchall()
        return self.objetos
    def editar(self, id_usuario, telefono, residencia, correo, sexo, adicional):
        db = get_db()
        sql = """UPDATE usuario SET telefono_us = %s, residencia_us = %s, 
                 correo_us = %s, sexo_us = %s, adicional_us = %s 
                 WHERE id_usuario = %s"""
        cur = db.cursor()
        cur.execute(sql, (telefono, residencia, correo, sexo, adicional, id_usuario))
        db.commit()
    def cambiar_contra(self, id_usuario, oldpass, newpass):
        db = get_db()
        check_sql = """SELECT * FROM usuario 
                       WHERE id_usuario = %s AND contrasena_us = %s"""
        cur = db.cursor()
        cur.execute(check_sql, (id_usuario, oldpass))
        if cur.fetchone():
            update_sql = """UPDATE usuario SET contrasena_us = %s 
                            WHERE id_usuario = %s"""
            cur.execute(update_sql, (newpass, id_usuario))
            db.commit()
            return 'update'
        return 'noupdate'
    def cambiar_photo(self, id_usuario, filename):
        db = get_db()
        cur = db.cursor()
        select_sql = "SELECT avatar FROM usuario WHERE id_usuario = %s"
        cur.execute(select_sql, (id_usuario,))
        self.objetos = cur.fetchall()

        update_sql = "UPDATE usuario SET avatar = %s WHERE id_usuario = %s"
        cur.execute(update_sql, (filename, id_usuario))
        db.commit()
        return self.objetos
    def buscar(self, consulta=""):
        db = get_db()
        cur = db.cursor()
        if consulta:
            sql = """SELECT * FROM usuario 
                    JOIN tipo_us ON us_tipo = id_tipo_us 
                    WHERE nombre_us LIKE %s"""
            cur.execute(sql, (f'%{consulta}%',))
        else:
            sql = """SELECT * FROM usuario 
                    JOIN tipo_us ON us_tipo = id_tipo_us 
                    WHERE nombre_us != '' 
                    ORDER BY id_usuario LIMIT 25"""
            cur.execute(sql)
        
        rows = cur.fetchall()
        return rows
    def crear(self, nombre, apellido, edad, dni, password, tipo, avatar):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE dni_us = %s", (dni,))
        if cur.fetchone():
            return 'noadd'
        insert_sql = """INSERT INTO usuario 
                        (nombre_us, apellidos_us, edad, dni_us, contrasena_us, us_tipo, avatar) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cur.execute(insert_sql, (nombre, apellido, edad, dni, password, tipo, avatar))
        db.commit()
        return 'add'
    def ascender(self, pass_input, id_ascendido, id_admin):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s AND contrasena_us = %s", (id_admin, pass_input))
        if cur.fetchone():
            cur.execute("UPDATE usuario SET us_tipo = 2 WHERE id_usuario = %s", (id_ascendido,))
            db.commit()
            return 'ascendido'
        return 'noascendido'
    def descender(self, pass_input, id_descendido, id_admin):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s AND contrasena_us = %s", (id_admin, pass_input))
        if cur.fetchone():
            cur.execute("UPDATE usuario SET us_tipo = 3 WHERE id_usuario = %s", (id_descendido,))
            db.commit()
            return 'descendido'
        return 'nodescendido'
    def borrar_usuario(self, pass_input, id_borrado, id_admin):
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE id_usuario = %s AND contrasena_us = %s", (id_admin, pass_input))
        if cur.fetchone():
            cur.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_borrado,))
            db.commit()
            return 'borrado'
        return 'noborrado'