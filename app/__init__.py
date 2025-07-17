from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.controllers.LoginController import login_bp

from config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from app.db import close_db
    app.teardown_appcontext(close_db)

    # Importar y registrar blueprints
    from app.controllers.LoginController import login_bp
    from app.controllers.ProductoController import producto_bp
    from app.controllers.UsuarioController import usuario_bp
    from app.controllers.ProveedorController import proveedor_bp
    from app.controllers.PrediccionController import prediccion_bp
    from app.controllers.LaboratorioController import laboratorio_bp
    from app.controllers.LoteController import lote_bp
    from app.controllers.PresentacionController import presentacion_bp
    from app.controllers.TipoController import tipo_bp
    from app.controllers.CompraController import compra_bp
    from app.controllers.VentaController import venta_bp
    from app.controllers.VentaProductoController import venta_producto_bp
    app.register_blueprint(venta_producto_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(prediccion_bp)
    app.register_blueprint(laboratorio_bp)
    app.register_blueprint(lote_bp)
    app.register_blueprint(presentacion_bp)
    app.register_blueprint(tipo_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(compra_bp)
    

    return app