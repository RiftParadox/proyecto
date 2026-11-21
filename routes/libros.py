import re

import psycopg
from flask import Blueprint, flash, redirect, render_template, request, url_for

from db import flash_db_error, get_db_connection

libros_bp = Blueprint("libros", __name__, url_prefix="/libros")


def cargar_opciones(conn):
    autores = conn.execute(
        "SELECT id_autor, nombre FROM autores ORDER BY nombre"
    ).fetchall()
    categorias = conn.execute(
        "SELECT id_categoria, nombre FROM categorias ORDER BY nombre"
    ).fetchall()
    return autores, categorias


def validar_formulario():
    titulo = request.form.get("titulo", "").strip()
    isbn = request.form.get("isbn", "").strip()
    anio_texto = request.form.get("anio_publicacion", "").strip()
    stock_texto = request.form.get("stock_total", "").strip()
    autor_texto = request.form.get("id_autor", "").strip()
    categoria_texto = request.form.get("id_categoria", "").strip()
    errores = []
    try:
        anio = int(anio_texto)
        if anio <= 0:
            errores.append("El año de publicación debe ser mayor que cero.")
        elif anio > 2147483647:
            errores.append("El año de publicación excede el rango permitido.")
    except ValueError:
        anio = None
        errores.append("Ingresa un año de publicación válido.")
    try:
        stock = int(stock_texto)
        if stock < 0:
            errores.append("El stock no puede ser negativo.")
        elif stock > 2147483647:
            errores.append("El stock excede el rango permitido.")
    except ValueError:
        stock = None
        errores.append("Ingresa una cantidad de stock válida.")
    try:
        id_autor = int(autor_texto)
    except ValueError:
        id_autor = None
        errores.append("Selecciona un autor válido.")
    try:
        id_categoria = int(categoria_texto)
    except ValueError:
        id_categoria = None
        errores.append("Selecciona una categoría válida.")
    if not titulo:
        errores.append("El título es obligatorio.")
    elif len(titulo) > 180:
        errores.append("El título no puede superar 180 caracteres.")
    if not isbn:
        errores.append("El ISBN es obligatorio.")
    elif len(isbn) > 30:
        errores.append("El ISBN no puede superar 30 caracteres.")
    elif not re.fullmatch(r"(?:[0-9]{9}[0-9Xx]|[0-9]{13})", isbn.replace("-", "")):
        errores.append("Ingresa un ISBN-10 o ISBN-13 válido, con o sin guiones.")
    return {
        "titulo": titulo,
        "isbn": isbn,
        "anio_publicacion": anio,
        "stock_total": stock,
        "id_autor": id_autor,
        "id_categoria": id_categoria,
    }, errores


@libros_bp.get("/")
def listar():
    try:
        with get_db_connection() as conn:
            libros = conn.execute(
                """
                SELECT l.id_libro, l.titulo, l.isbn, l.anio_publicacion, l.stock_total,
                       a.nombre AS autor, c.nombre AS categoria
                FROM libros l
                JOIN autores a ON a.id_autor = l.id_autor
                JOIN categorias c ON c.id_categoria = l.id_categoria
                ORDER BY l.titulo
                """
            ).fetchall()
    except psycopg.Error as error:
        flash_db_error(error)
        libros = []
    return render_template("libros/listar.html", libros=libros)


@libros_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    try:
        with get_db_connection() as conn:
            autores, categorias = cargar_opciones(conn)
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("libros.listar"))
    if request.method == "POST":
        libro, errores = validar_formulario()
        if not autores or not categorias:
            errores.append("Primero registra al menos un autor y una categoría.")
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        INSERT INTO libros
                            (titulo, isbn, anio_publicacion, stock_total, id_autor, id_categoria)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            libro["titulo"], libro["isbn"], libro["anio_publicacion"],
                            libro["stock_total"], libro["id_autor"], libro["id_categoria"],
                        ),
                    )
                flash("Libro creado correctamente.", "success")
                return redirect(url_for("libros.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        return render_template(
            "libros/form.html", libro=libro, autores=autores,
            categorias=categorias, titulo="Nuevo libro",
        )
    return render_template(
        "libros/form.html", libro={}, autores=autores,
        categorias=categorias, titulo="Nuevo libro",
    )


@libros_bp.route("/<int:id_libro>/editar", methods=["GET", "POST"])
def editar(id_libro):
    try:
        with get_db_connection() as conn:
            libro_actual = conn.execute(
                """
                SELECT id_libro, titulo, isbn, anio_publicacion, stock_total,
                       id_autor, id_categoria
                FROM libros WHERE id_libro = %s
                """,
                (id_libro,),
            ).fetchone()
            autores, categorias = cargar_opciones(conn)
    except psycopg.Error as error:
        flash_db_error(error)
        return redirect(url_for("libros.listar"))
    if libro_actual is None:
        flash("No se encontró el libro solicitado.", "warning")
        return redirect(url_for("libros.listar"))
    if request.method == "POST":
        libro, errores = validar_formulario()
        if errores:
            for error in errores:
                flash(error, "warning")
        else:
            try:
                with get_db_connection() as conn:
                    conn.execute(
                        """
                        UPDATE libros SET titulo = %s, isbn = %s, anio_publicacion = %s,
                            stock_total = %s, id_autor = %s, id_categoria = %s
                        WHERE id_libro = %s
                        """,
                        (
                            libro["titulo"], libro["isbn"], libro["anio_publicacion"],
                            libro["stock_total"], libro["id_autor"], libro["id_categoria"],
                            id_libro,
                        ),
                    )
                flash("Libro actualizado correctamente.", "success")
                return redirect(url_for("libros.listar"))
            except psycopg.Error as error:
                flash_db_error(error)
        libro["id_libro"] = id_libro
    else:
        libro = libro_actual
    return render_template(
        "libros/form.html", libro=libro, autores=autores,
        categorias=categorias, titulo="Editar libro",
    )


@libros_bp.post("/<int:id_libro>/eliminar")
def eliminar(id_libro):
    try:
        with get_db_connection() as conn:
            conn.execute("DELETE FROM libros WHERE id_libro = %s", (id_libro,))
        flash("Libro eliminado correctamente.", "success")
    except psycopg.Error as error:
        flash_db_error(error)
    return redirect(url_for("libros.listar"))
