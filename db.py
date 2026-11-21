import psycopg
from flask import current_app, flash
from psycopg.rows import dict_row

from config import DB_CONFIG


def get_db_connection():
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


def flash_db_error(error):
    constraint_errors = (
        psycopg.errors.UniqueViolation,
        psycopg.errors.ForeignKeyViolation,
        psycopg.errors.CheckViolation,
        psycopg.errors.NotNullViolation,
    )
    if isinstance(error, psycopg.errors.UniqueViolation):
        message = "Ya existe un registro con ese dato único (por ejemplo, correo o ISBN)."
    elif isinstance(error, psycopg.errors.ForeignKeyViolation):
        message = "El registro relacionado no existe o no se puede eliminar porque está en uso."
    elif isinstance(error, psycopg.errors.CheckViolation):
        message = "Los datos no cumplen las reglas establecidas."
    elif isinstance(error, psycopg.errors.NotNullViolation):
        message = "Falta completar un campo obligatorio."
    else:
        message = "Ocurrió un error al guardar o consultar la base de datos."
    if isinstance(error, constraint_errors):
        current_app.logger.warning("Restricción de base de datos (%s)", error.sqlstate)
    else:
        current_app.logger.exception("Error de base de datos")
    flash(message, "danger")
