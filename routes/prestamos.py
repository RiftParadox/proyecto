from datetime import date

import psycopg
from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import flash_db_error, get_db_connection

prestamos_bp = Blueprint("prestamos", __name__, url_prefix="/prestamos")


def cargar_opciones(conn):
    libros = conn.execute(
        "SELECT id_libro, titulo FROM libros ORDER BY titulo"
    ).fetchall()
    lectores = conn.execute(
        "SELECT id_lector, nombre_completo FROM lectores ORDER BY nombre_completo"
    ).fetchall()
    return libros, lectores


def validar_fecha(valor, etiqueta, errores):
    try:
        return date.fromisoformat(valor)
    except ValueError:
        errores.append(f"Ingresa una fecha válida para {etiqueta}.")
        return None


def validar_formulario():
    libro_texto = request.form.get("id_libro", "").strip()
    lector_texto = request.form.get("id_lector", "").strip()
    fecha_prestamo_texto = request.form.get("fecha_prestamo", "").strip()
    fecha_prevista_texto = request.form.get("fecha_devolucion_prevista", "").strip()
    devuelto_texto = request.form.get("devuelto", "")
    errores = []
    try:
        id_libro = int(libro_texto)
    except ValueError:
        id_libro = None
        errores.append("Selecciona un libro válido.")
    try:
        id_lector = int(lector_texto)
    except ValueError:
        id_lector = None
        errores.append("Selecciona un lector válido.")
    fecha_prestamo = validar_fecha(fecha_prestamo_texto, "el préstamo", errores)
    fecha_prevista = validar_fecha(fecha_prevista_texto, "la devolución prevista", errores)
    if fecha_prestamo and fecha_prevista and fecha_prevista < fecha_prestamo:
        errores.append("La devolución prevista no puede ser anterior al préstamo.")
    if devuelto_texto not in ("true", "false"):
        errores.append("Selecciona el estado de devolución.")
    return {
        "id_libro": id_libro,
        "id_lector": id_lector,
        "fecha_prestamo": fecha_prestamo_texto,
        "fecha_devolucion_prevista": fecha_prevista_texto,
        "devuelto": devuelto_texto == "true",
    }, errores


@prestamos_bp.get("/")
def listar():
    try:
        with get_db_connection() as conn:
            prestamos = conn.execute(
                """
                SELECT p.id_prestamo, l.titulo AS libro, r.nombre_completo AS lector,
                       p.fecha_prestamo, p.fecha_devolucion_prevista, p.devuelto
                FROM prestamos p
                JOIN libros l ON l.id_libro = p.id_libro
                JOIN lectores r ON r.id_lector = p.id_lector
                ORDER BY p.fecha_prestamo DESC, p.id_prestamo DESC
                """
            ).fetchall()
    except psycopg.Error as error:
        flash_db_error(error)
        prestamos = []
    return render_template("prestamos/listar.html", prestamos=prestamos)


@prestamos_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    try:
        with get_db_connection() as conn:
            libros, lectores = cargar_opciones(conn)
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("prestamos.listar"))
    if request.method == "POST":
        prestamo, errores = validar_formulario()
        if not libros or not lectores:
            errores.append("Se necesita al menos un libro y un lector activo.")
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO prestamos
                            (id_libro, id_lector, fecha_prestamo,
                             fecha_devolucion_prevista, devuelto)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            prestamo["id_libro"], prestamo["id_lector"],
                            prestamo["fecha_prestamo"],
                            prestamo["fecha_devolucion_prevista"], prestamo["devuelto"],
                        ),
                    )
                flash("Préstamo registrado correctamente.", "success")
                return redirect(url_for("prestamos.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        return render_template(
            "prestamos/form.html", prestamo=prestamo, libros=libros,
            lectores=lectores, titulo="Nuevo préstamo",
        )
    return render_template(
        "prestamos/form.html", prestamo={}, libros=libros,
        lectores=lectores, titulo="Nuevo préstamo",
    )


@prestamos_bp.route("/<int:id_prestamo>/editar", methods=["GET", "POST"])
def editar(id_prestamo):
    try:
        with get_db_connection() as conn:
            prestamo_actual = conn.execute(
                """
                SELECT id_prestamo, id_libro, id_lector, fecha_prestamo,
                       fecha_devolucion_prevista, devuelto
                FROM prestamos WHERE id_prestamo = %s
                """,
                (id_prestamo,),
            ).fetchone()
            libros, lectores = cargar_opciones(conn)
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("prestamos.listar"))
    if prestamo_actual is None:
        flash("No se encontró el préstamo solicitado.", "warning")
        return redirect(url_for("prestamos.listar"))
    if request.method == "POST":
        prestamo, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        UPDATE prestamos SET id_libro = %s, id_lector = %s,
                            fecha_prestamo = %s, fecha_devolucion_prevista = %s,
                            devuelto = %s
                        WHERE id_prestamo = %s
                        """,
                        (
                            prestamo["id_libro"], prestamo["id_lector"],
                            prestamo["fecha_prestamo"],
                            prestamo["fecha_devolucion_prevista"], prestamo["devuelto"],
                            id_prestamo,
                        ),
                    )
                flash("Préstamo actualizado correctamente.", "success")
                return redirect(url_for("prestamos.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        prestamo["id_prestamo"] = id_prestamo
    else:
        prestamo = prestamo_actual
    return render_template(
        "prestamos/form.html", prestamo=prestamo, libros=libros,
        lectores=lectores, titulo="Editar préstamo",
    )


@prestamos_bp.post("/<int:id_prestamo>/eliminar")
def eliminar(id_prestamo):
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM prestamos WHERE id_prestamo = %s", (id_prestamo,))
        flash("Préstamo eliminado correctamente.", "success")
    except psycopg.Error as error:
        flash_db_error(error)
    return redirect(url_for("prestamos.listar"))
