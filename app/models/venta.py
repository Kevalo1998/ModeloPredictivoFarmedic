from app.db import get_db
from pymysql.err import IntegrityError

class Venta:
    def crear(self, nombre, dni, total, fecha, vendedor):
        """
        Inserta una nueva venta en la tabla `venta`.
        """
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute("""
                INSERT INTO venta (fecha, cliente, dni, total, vendedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (fecha, nombre, dni, total, vendedor))
            db.commit()
            return cur.lastrowid
        except IntegrityError as e:
            db.rollback()
            raise e

    def ultima_venta(self):
        """
        Devuelve el id de la última venta registrada.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT MAX(id_venta) AS ultima_venta FROM venta")
        row = cur.fetchone()
        return row['ultima_venta'] if row and row.get('ultima_venta') is not None else None

    def borrar(self, id_venta):
        """
        Borra una venta dado su id.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("DELETE FROM venta WHERE id_venta = %s", (id_venta,))
        db.commit()

    def buscar(self):
        """
        Devuelve todas las ventas con datos de vendedor concatenados.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT 
              v.id_venta,
              v.fecha,
              v.cliente,
              v.dni,
              v.total,
              CONCAT(u.nombre_us, ' ', u.apellidos_us) AS vendedor
            FROM venta AS v
            JOIN usuario AS u ON v.vendedor = u.id_usuario
            ORDER BY v.fecha DESC
        """)
        columns = [c[0] for c in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]

    def venta_dia_vendedor(self, id_usuario):
        """
        Suma del total vendido hoy por un vendedor.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(total), 0) AS venta_dia_vendedor
            FROM venta
            WHERE vendedor = %s
              AND DATE(fecha) = CURDATE()
        """, (id_usuario,))
        row = cur.fetchone()
        return row['venta_dia_vendedor'] if row else 0

    def venta_diaria(self):
        """
        Suma del total vendido hoy (todos los vendedores).
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(total), 0) AS venta_diaria
            FROM venta
            WHERE DATE(fecha) = CURDATE()
        """)
        row = cur.fetchone()
        return row['venta_diaria'] if row else 0

    def venta_mensual(self):
        """
        Suma del total vendido en el mes actual.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(total), 0) AS venta_mensual
            FROM venta
            WHERE YEAR(fecha) = YEAR(CURDATE())
              AND MONTH(fecha) = MONTH(CURDATE())
        """)
        row = cur.fetchone()
        return row['venta_mensual'] if row else 0

    def venta_anual(self):
        """
        Suma del total vendido en el año actual.
        """
        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(total), 0) AS venta_anual
            FROM venta
            WHERE YEAR(fecha) = YEAR(CURDATE())
        """)
        row = cur.fetchone()
        return row['venta_anual'] if row else 0