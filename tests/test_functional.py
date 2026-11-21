import uuid
import unittest

import psycopg

from app import app
from db import get_db_connection


class BibliotecaFunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()
        cls.token = uuid.uuid4().hex[:10]

    @classmethod
    def fetch_one(cls, query, params=()):
        with get_db_connection() as conn:
            return conn.execute(query, params).fetchone()

    @classmethod
    def selected_ids(cls):
        author = cls.fetch_one("SELECT id_autor FROM autores ORDER BY id_autor LIMIT 1")
        category = cls.fetch_one(
            "SELECT id_categoria FROM categorias ORDER BY id_categoria LIMIT 1"
        )
        book = cls.fetch_one("SELECT id_libro FROM libros ORDER BY id_libro LIMIT 1")
        reader = cls.fetch_one(
            "SELECT id_lector FROM lectores ORDER BY id_lector LIMIT 1"
        )
        return author, category, book, reader

    def submit(self, url, data):
        response = self.client.post(url, data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        return response.get_data(as_text=True)

    def test_01_autores_crear_listar_editar_eliminar(self):
        name = "Autor prueba " + self.token
        self.submit(
            "/autores/nuevo",
            {"nombre": name, "nacionalidad": "Colombiana"},
        )
        page = self.client.get("/autores/").get_data(as_text=True)
        self.assertIn(name, page)
        self.assertIn("return confirm(", page)
        row = self.fetch_one("SELECT id_autor FROM autores WHERE nombre = %s", (name,))
        self.assertIsNotNone(row)
        author_id = row["id_autor"]
        edited_name = name + " editado"
        self.submit(
            f"/autores/{author_id}/editar",
            {"nombre": edited_name, "nacionalidad": "Mexicana"},
        )
        self.assertIn(edited_name, self.client.get("/autores/").get_data(as_text=True))
        page = self.submit(f"/autores/{author_id}/eliminar", {})
        self.assertIn("Autor eliminado correctamente", page)
        self.assertNotIn(edited_name, self.client.get("/autores/").get_data(as_text=True))

    def test_02_autores_rechaza_nombre_vacio(self):
        page = self.submit(
            "/autores/nuevo",
            {"nombre": "", "nacionalidad": "Colombiana"},
        )
        self.assertIn("El nombre es obligatorio", page)

    def test_03_autores_no_se_elimina_si_tiene_libros(self):
        row = self.fetch_one(
            """
            SELECT a.id_autor FROM autores a
            JOIN libros l ON l.id_autor = a.id_autor
            ORDER BY a.id_autor LIMIT 1
            """
        )
        page = self.submit(f"/autores/{row['id_autor']}/eliminar", {})
        self.assertIn("no se puede eliminar porque está en uso", page)

    def test_04_categorias_crear_listar_editar_eliminar(self):
        name = "Categoria prueba " + self.token
        self.submit(
            "/categorias/nuevo",
            {"nombre": name, "descripcion": "Categoría temporal para prueba."},
        )
        row = self.fetch_one(
            "SELECT id_categoria FROM categorias WHERE nombre = %s", (name,)
        )
        self.assertIsNotNone(row)
        category_id = row["id_categoria"]
        edited_name = name + " editada"
        self.submit(
            f"/categorias/{category_id}/editar",
            {"nombre": edited_name, "descripcion": "Descripción actualizada."},
        )
        self.assertIn(
            edited_name, self.client.get("/categorias/").get_data(as_text=True)
        )
        page = self.submit(f"/categorias/{category_id}/eliminar", {})
        self.assertIn("Categoría eliminada correctamente", page)
        self.assertNotIn(
            edited_name, self.client.get("/categorias/").get_data(as_text=True)
        )

    def test_05_categorias_rechaza_nombre_duplicado(self):
        existing = self.fetch_one(
            "SELECT nombre FROM categorias ORDER BY id_categoria LIMIT 1"
        )
        page = self.submit(
            "/categorias/nuevo",
            {"nombre": existing["nombre"], "descripcion": ""},
        )
        self.assertIn("dato único", page)

    def test_06_categorias_no_se_elimina_si_tiene_libros(self):
        row = self.fetch_one(
            """
            SELECT c.id_categoria FROM categorias c
            JOIN libros l ON l.id_categoria = c.id_categoria
            ORDER BY c.id_categoria LIMIT 1
            """
        )
        page = self.submit(f"/categorias/{row['id_categoria']}/eliminar", {})
        self.assertIn("no se puede eliminar porque está en uso", page)

    def test_07_libros_crear_listar_editar_eliminar(self):
        author, category, _, _ = self.selected_ids()
        title = "Libro prueba " + self.token
        isbn = "978" + str(uuid.uuid4().int)[-10:]
        self.submit(
            "/libros/nuevo",
            {
                "titulo": title,
                "isbn": isbn,
                "anio_publicacion": "2020",
                "stock_total": "2",
                "id_autor": str(author["id_autor"]),
                "id_categoria": str(category["id_categoria"]),
            },
        )
        row = self.fetch_one("SELECT id_libro FROM libros WHERE isbn = %s", (isbn,))
        self.assertIsNotNone(row)
        book_id = row["id_libro"]
        page = self.client.get("/libros/").get_data(as_text=True)
        self.assertIn(title, page)
        self.assertIn("Gabriel Garc", page)
        edited_title = title + " editado"
        self.submit(
            f"/libros/{book_id}/editar",
            {
                "titulo": edited_title,
                "isbn": isbn,
                "anio_publicacion": "2021",
                "stock_total": "3",
                "id_autor": str(author["id_autor"]),
                "id_categoria": str(category["id_categoria"]),
            },
        )
        self.assertIn(edited_title, self.client.get("/libros/").get_data(as_text=True))
        page = self.submit(f"/libros/{book_id}/eliminar", {})
        self.assertIn("Libro eliminado correctamente", page)
        self.assertNotIn(edited_title, self.client.get("/libros/").get_data(as_text=True))

    def test_08_libros_rechaza_isbn_invalido(self):
        author, category, _, _ = self.selected_ids()
        page = self.submit(
            "/libros/nuevo",
            {
                "titulo": "Libro inválido " + self.token,
                "isbn": "ISBN-incorrecto",
                "anio_publicacion": "2020",
                "stock_total": "1",
                "id_autor": str(author["id_autor"]),
                "id_categoria": str(category["id_categoria"]),
            },
        )
        self.assertIn("Ingresa un ISBN-10 o ISBN-13 válido", page)

    def test_09_libros_no_se_elimina_si_tiene_prestamos(self):
        row = self.fetch_one(
            """
            SELECT l.id_libro FROM libros l
            JOIN prestamos p ON p.id_libro = l.id_libro
            ORDER BY l.id_libro LIMIT 1
            """
        )
        page = self.submit(f"/libros/{row['id_libro']}/eliminar", {})
        self.assertIn("no se puede eliminar porque está en uso", page)

    def test_10_lectores_crear_listar_editar_eliminar(self):
        name = "Lector prueba " + self.token
        email = f"lector-{self.token}@example.com"
        self.submit(
            "/lectores/nuevo",
            {
                "nombre_completo": name,
                "correo": email,
                "telefono": "3001234567",
                "activo": "true",
            },
        )
        row = self.fetch_one("SELECT id_lector FROM lectores WHERE correo = %s", (email,))
        self.assertIsNotNone(row)
        reader_id = row["id_lector"]
        page = self.client.get("/lectores/").get_data(as_text=True)
        self.assertIn(name, page)
        edited_name = name + " editado"
        self.submit(
            f"/lectores/{reader_id}/editar",
            {
                "nombre_completo": edited_name,
                "correo": email,
                "telefono": "3007654321",
                "activo": "true",
            },
        )
        self.assertIn(edited_name, self.client.get("/lectores/").get_data(as_text=True))
        page = self.submit(f"/lectores/{reader_id}/eliminar", {})
        self.assertIn("Lector eliminado correctamente", page)
        self.assertNotIn(edited_name, self.client.get("/lectores/").get_data(as_text=True))

    def test_11_lectores_rechaza_correo_invalido(self):
        page = self.submit(
            "/lectores/nuevo",
            {
                "nombre_completo": "Lector inválido " + self.token,
                "correo": "no-es-correo",
                "telefono": "",
                "activo": "true",
            },
        )
        self.assertIn("Ingresa un correo electrónico válido", page)

    def test_12_lectores_no_se_elimina_si_tiene_prestamos(self):
        row = self.fetch_one(
            """
            SELECT r.id_lector FROM lectores r
            JOIN prestamos p ON p.id_lector = r.id_lector
            ORDER BY r.id_lector LIMIT 1
            """
        )
        page = self.submit(f"/lectores/{row['id_lector']}/eliminar", {})
        self.assertIn("no se puede eliminar porque está en uso", page)

    def test_13_prestamos_crear_listar_editar_eliminar(self):
        _, _, book, reader = self.selected_ids()
        data = {
            "id_libro": str(book["id_libro"]),
            "id_lector": str(reader["id_lector"]),
            "fecha_prestamo": "2026-06-01",
            "fecha_devolucion_prevista": "2026-06-15",
            "devuelto": "false",
        }
        self.submit("/prestamos/nuevo", data)
        row = self.fetch_one(
            """
            SELECT id_prestamo FROM prestamos
            WHERE id_libro = %s AND id_lector = %s AND fecha_prestamo = %s
            ORDER BY id_prestamo DESC LIMIT 1
            """,
            (book["id_libro"], reader["id_lector"], "2026-06-01"),
        )
        self.assertIsNotNone(row)
        loan_id = row["id_prestamo"]
        page = self.client.get("/prestamos/").get_data(as_text=True)
        self.assertIn("Cien a", page)
        self.assertIn("Ana Mart", page)
        data["fecha_devolucion_prevista"] = "2026-06-20"
        data["devuelto"] = "true"
        self.submit(f"/prestamos/{loan_id}/editar", data)
        self.assertIn(
            "2026-06-20", self.client.get("/prestamos/").get_data(as_text=True)
        )
        page = self.submit(f"/prestamos/{loan_id}/eliminar", {})
        self.assertIn("Préstamo eliminado correctamente", page)

    def test_14_prestamos_rechaza_fecha_invertida(self):
        _, _, book, reader = self.selected_ids()
        page = self.submit(
            "/prestamos/nuevo",
            {
                "id_libro": str(book["id_libro"]),
                "id_lector": str(reader["id_lector"]),
                "fecha_prestamo": "2026-06-20",
                "fecha_devolucion_prevista": "2026-06-01",
                "devuelto": "false",
            },
        )
        self.assertIn(
            "La devolución prevista no puede ser anterior al préstamo", page
        )

    def test_15_prestamos_rechaza_claves_foraneas_inexistentes(self):
        page = self.submit(
            "/prestamos/nuevo",
            {
                "id_libro": "2147483647",
                "id_lector": "2147483647",
                "fecha_prestamo": "2026-06-01",
                "fecha_devolucion_prevista": "2026-06-15",
                "devuelto": "false",
            },
        )
        self.assertIn("no existe", page)


if __name__ == "__main__":
    unittest.main(verbosity=2)
