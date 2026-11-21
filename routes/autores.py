import psycopg
from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import flash_db_error, get_db_connection

autores_bp = Blueprint("autores", __name__, url_prefix="/autores")


def validar_formulario():
    nombre = request.form.get("nombre", "").strip()
    nacionalidad = request.form.get("nacionalidad", "").strip()
    errores = []
    if not nombre:
        errores.append("El nombre es obligatorio.")
    if len(nombre) > 120:
        errores.append("El nombre no puede superar 120 caracteres.")
    if not nacionalidad:
        errores.append("La nacionalidad es obligatoria.")
    if len(nacionalidad) > 80:
        errores.append("La nacionalidad no puede superar 80 caracteres.")
    return nombre, nacionalidad, errores


@autores_bp.get("/")
def listar():
    try:
        with get_db_connection() as conn:
            autores = conn.execute(
                "SELECT id_autor, nombre, nacionalidad FROM autores ORDER BY nombre"
            ).fetchall()
    except psycopg.Error as error:
        flash_db_error(error)
        autores = []
    return render_template("autores/listar.html", autores=autores)


@autores_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre, nacionalidad, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        "INSERT INTO autores (nombre, nacionalidad) VALUES (%s, %s)",
                        (nombre, nacionalidad),
                    )
                flash("Autor creado correctamente.", "success")
                return redirect(url_for("autores.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        return render_template(
            "autores/form.html",
            autor={"nombre": nombre, "nacionalidad": nacionalidad},
            titulo="Nuevo autor",
        )
    return render_template("autores/form.html", autor={}, titulo="Nuevo autor")


@autores_bp.route("/<int:id_autor>/editar", methods=["GET", "POST"])
def editar(id_autor):
    try:
        with get_db_connection() as conn:
            autor = conn.execute(
                "SELECT id_autor, nombre, nacionalidad FROM autores WHERE id_autor = %s",
                (id_autor,),
            ).fetchone()
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("autores.listar"))
    if autor is None:
        flash("No se encontró el autor solicitado.", "warning")
        return redirect(url_for("autores.listar"))
    if request.method == "POST":
        nombre, nacionalidad, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
            autor = {"id_autor": id_autor, "nombre": nombre, "nacionalidad": nacionalidad}
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        "UPDATE autores SET nombre = %s, nacionalidad = %s WHERE id_autor = %s",
                        (nombre, nacionalidad, id_autor),
                    )
                flash("Autor actualizado correctamente.", "success")
                return redirect(url_for("autores.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
                autor = {"id_autor": id_autor, "nombre": nombre, "nacionalidad": nacionalidad}
    return render_template("autores/form.html", autor=autor, titulo="Editar autor")


@autores_bp.post("/<int:id_autor>/eliminar")
def eliminar(id_autor):
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM autores WHERE id_autor = %s", (id_autor,))
        flash("Autor eliminado correctamente.", "success")
    except psycopg.Error as error:
        flash_db_error(error)
    return redirect(url_for("autores.listar"))
