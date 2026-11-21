import psycopg
from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import flash_db_error, get_db_connection

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


def validar_formulario():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    errores = []
    if not nombre:
        errores.append("El nombre es obligatorio.")
    if len(nombre) > 80:
        errores.append("El nombre no puede superar 80 caracteres.")
    return nombre, descripcion, errores


@categorias_bp.get("/")
def listar():
    try:
        with get_db_connection() as conn:
            categorias = conn.execute(
                "SELECT id_categoria, nombre, descripcion FROM categorias ORDER BY nombre"
            ).fetchall()
    except psycopg.Error as error:
        flash_db_error(error)
        categorias = []
    return render_template("categorias/listar.html", categorias=categorias)


@categorias_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre, descripcion, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)",
                        (nombre, descripcion or None),
                    )
                flash("Categoría creada correctamente.", "success")
                return redirect(url_for("categorias.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        return render_template(
            "categorias/form.html",
            categoria={"nombre": nombre, "descripcion": descripcion},
            titulo="Nueva categoría",
        )
    return render_template("categorias/form.html", categoria={}, titulo="Nueva categoría")


@categorias_bp.route("/<int:id_categoria>/editar", methods=["GET", "POST"])
def editar(id_categoria):
    try:
        with get_db_connection() as conn:
            categoria = conn.execute(
                "SELECT id_categoria, nombre, descripcion FROM categorias WHERE id_categoria = %s",
                (id_categoria,),
            ).fetchone()
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("categorias.listar"))
    if categoria is None:
        flash("No se encontró la categoría solicitada.", "warning")
        return redirect(url_for("categorias.listar"))
    if request.method == "POST":
        nombre, descripcion, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
            categoria = {
                "id_categoria": id_categoria,
                "nombre": nombre,
                "descripcion": descripcion,
            }
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        "UPDATE categorias SET nombre = %s, descripcion = %s WHERE id_categoria = %s",
                        (nombre, descripcion or None, id_categoria),
                    )
                flash("Categoría actualizada correctamente.", "success")
                return redirect(url_for("categorias.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
                categoria = {
                    "id_categoria": id_categoria,
                    "nombre": nombre,
                    "descripcion": descripcion,
                }
    return render_template(
        "categorias/form.html", categoria=categoria, titulo="Editar categoría"
    )


@categorias_bp.post("/<int:id_categoria>/eliminar")
def eliminar(id_categoria):
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
        flash("Categoría eliminada correctamente.", "success")
    except psycopg.Error as error:
        flash_db_error(error)
    return redirect(url_for("categorias.listar"))
