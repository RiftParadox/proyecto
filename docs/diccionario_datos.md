# Diccionario de datos y normalización

El esquema contiene cinco entidades. Las claves foráneas usan el comportamiento predeterminado de PostgreSQL (`NO ACTION`): no se puede borrar una entidad mientras existan registros que la referencien.

## autores

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_autor` | SERIAL | PK | Identificador único del autor. |
| `nombre` | VARCHAR(120) | NOT NULL | Nombre del autor. |
| `nacionalidad` | VARCHAR(80) | NOT NULL | Nacionalidad del autor. |

## categorias

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_categoria` | SERIAL | PK | Identificador único de la categoría. |
| `nombre` | VARCHAR(80) | NOT NULL, UNIQUE | Nombre único de la categoría. |
| `descripcion` | TEXT | — | Descripción opcional de la categoría. |

## libros

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_libro` | SERIAL | PK | Identificador único del libro. |
| `titulo` | VARCHAR(180) | NOT NULL | Título del libro. |
| `isbn` | VARCHAR(30) | NOT NULL, UNIQUE | ISBN único del libro. |
| `anio_publicacion` | INT | NOT NULL, CHECK (`> 0`) | Año de publicación. |
| `stock_total` | INT | NOT NULL, DEFAULT 1, CHECK (`>= 0`) | Ejemplares disponibles en el inventario. |
| `id_autor` | INT | NOT NULL, FK → `autores.id_autor` | Autor del libro. |
| `id_categoria` | INT | NOT NULL, FK → `categorias.id_categoria` | Categoría del libro. |

## lectores

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_lector` | SERIAL | PK | Identificador único del lector. |
| `nombre_completo` | VARCHAR(140) | NOT NULL | Nombre completo del lector. |
| `correo` | VARCHAR(140) | NOT NULL, UNIQUE | Correo único del lector. |
| `telefono` | VARCHAR(30) | — | Teléfono opcional del lector. |
| `activo` | BOOLEAN | NOT NULL, DEFAULT TRUE | Indica si el lector está activo. |

## prestamos

| Campo | Tipo | Restricciones | Descripción |
|---|---|---|---|
| `id_prestamo` | SERIAL | PK | Identificador único del préstamo. |
| `id_libro` | INT | NOT NULL, FK → `libros.id_libro` | Libro prestado. |
| `id_lector` | INT | NOT NULL, FK → `lectores.id_lector` | Lector que recibe el libro. |
| `fecha_prestamo` | DATE | NOT NULL | Fecha en que se registra el préstamo. |
| `fecha_devolucion_prevista` | DATE | NOT NULL, CHECK (`>= fecha_prestamo`) | Fecha límite prevista para la devolución. |
| `devuelto` | BOOLEAN | NOT NULL, DEFAULT FALSE | Indica si el ejemplar fue devuelto. |

## Relaciones y cardinalidades

- `autores` 1:N `libros`: un autor puede tener varios libros; cada libro referencia un autor.
- `categorias` 1:N `libros`: una categoría puede contener varios libros; cada libro referencia una categoría.
- `libros` 1:N `prestamos`: un libro puede aparecer en varios préstamos históricos; cada préstamo referencia un libro.
- `lectores` 1:N `prestamos`: un lector puede realizar varios préstamos; cada préstamo referencia un lector.

El diagrama visual está en [mer.svg](./mer.svg).

## Justificación de 1FN, 2FN y 3FN

- **Primera forma normal (1FN):** cada columna contiene un solo valor de su tipo; no se guardan listas de autores, categorías, ejemplares o préstamos en una misma celda.
- **Segunda forma normal (2FN):** todas las tablas tienen una clave primaria de un solo campo. Los atributos no clave describen la fila identificada por esa clave completa.
- **Tercera forma normal (3FN):** los atributos descriptivos dependen directamente de la clave de su entidad. Los nombres de autor y categoría se almacenan una vez en sus tablas y se relacionan desde `libros`; los nombres del libro y del lector no se duplican en `prestamos`. No hay dependencias transitivas entre atributos no clave.
