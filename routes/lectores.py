import re

import psycopg
from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import flash_db_error, get_db_connection

lectores_bp = Blueprint("lectores", __name__, url_prefix="/lectores")


def validar_formulario():
    nombre = request.form.get("nombre_completo", "").strip()
    correo = request.form.get("correo", "").strip()
    telefono = request.form.get("telefono", "").strip()
    activo = request.form.get("activo", "")
    errores = []
    if not nombre:
        errores.append("El nombre completo es obligatorio.")
    if len(nombre) > 140:
        errores.append("El nombre no puede superar 140 caracteres.")
    if not correo or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
        errores.append("Ingresa un correo electrónico válido.")
    if len(correo) > 140:
        errores.append("El correo no puede superar 140 caracteres.")
    if len(telefono) > 30:
        errores.append("El teléfono no puede superar 30 caracteres.")
    if activo not in ("true", "false"):
        errores.append("Selecciona si el lector está activo.")
    return {
        "nombre_completo": nombre,
        "correo": correo,
        "telefono": telefono,
        "activo": activo == "true",
    }, errores


@lectores_bp.get("/")
def listar():
    try:
        with get_db_connection() as conn:
            lectores = conn.execute(
                """
                SELECT id_lector, nombre_completo, correo, telefono, activo
                FROM lectores ORDER BY nombre_completo
                """
            ).fetchall()
    except psycopg.Error as error:
        flash_db_error(error)
        lectores = []
    return render_template("lectores/listar.html", lectores=lectores)


@lectores_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        lector, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO lectores (nombre_completo, correo, telefono, activo)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            lector["nombre_completo"], lector["correo"],
                            lector["telefono"] or None, lector["activo"],
                        ),
                    )
                flash("Lector creado correctamente.", "success")
                return redirect(url_for("lectores.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        return render_template("lectores/form.html", lector=lector, titulo="Nuevo lector")
    return render_template("lectores/form.html", lector={"activo": True}, titulo="Nuevo lector")


@lectores_bp.route("/<int:id_lector>/editar", methods=["GET", "POST"])
def editar(id_lector):
    try:
        with get_db_connection() as conn:
            lector = conn.execute(
                """
                SELECT id_lector, nombre_completo, correo, telefono, activo
                FROM lectores WHERE id_lector = %s
                """,
                (id_lector,),
            ).fetchone()
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("lectores.listar"))
    if lector is None:
        flash("No se encontró el lector solicitado.", "warning")
        return redirect(url_for("lectores.listar"))
    if request.method == "POST":
        lector, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
            lector["id_lector"] = id_lector
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        UPDATE lectores SET nombre_completo = %s, correo = %s,
                            telefono = %s, activo = %s
                        WHERE id_lector = %s
                        """,
                        (
                            lector["nombre_completo"], lector["correo"],
                            lector["telefono"] or None, lector["activo"], id_lector,
                        ),
                    )
                flash("Lector actualizado correctamente.", "success")
                return redirect(url_for("lectores.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
                lector["id_lector"] = id_lector
    return render_template("lectores/form.html", lector=lector, titulo="Editar lector")


@lectores_bp.post("/<int:id_lector>/eliminar")
def eliminar(id_lector):
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM lectores WHERE id_lector = %s", (id_lector,))
        flash("Lector eliminado correctamente.", "success")
    except psycopg.Error as error:
        flash_db_error(error)
    return redirect(url_for("lectores.listar"))
