from flask import Flask, render_template

from routes.autores import autores_bp
from routes.categorias import categorias_bp
from routes.libros import libros_bp
from routes.lectores import lectores_bp
from routes.prestamos import prestamos_bp


app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(autores_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(libros_bp)
app.register_blueprint(lectores_bp)
app.register_blueprint(prestamos_bp)


@app.get("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
