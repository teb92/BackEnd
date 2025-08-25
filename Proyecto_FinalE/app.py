
from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt, jwt, cache, cache_key_prefix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    import models  


    from products.routes import bp as products_bp
    app.register_blueprint(products_bp, url_prefix="/")

    from auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    
    from users.routes import bp as users_bp
    app.register_blueprint(users_bp, url_prefix="/")
    
    from carts.routes import bp as carts_bp
    app.register_blueprint(carts_bp, url_prefix="/carts")
    


    @app.get("/debug/cache-info")
    def cache_info():
        from extensions import cache
        backend = type(cache.cache).__name__
        key = f"{cache_key_prefix(app)}debug:ping"
        try:
            cache.set(key, "pong", timeout=10)
            val = cache.get(key)
            return {"backend": backend, "connected": val == "pong", "sample_key": key, "value": val}, (200 if val == "pong" else 500)
        except Exception as e:
            return {"backend": backend, "connected": False, "error": str(e)}, 500

    @app.get("/health")
    def health():
        return {"ok": True}

    return app

app = create_app()

