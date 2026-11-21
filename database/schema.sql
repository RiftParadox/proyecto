CREATE TABLE autores (
    id_autor SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    nacionalidad VARCHAR(80) NOT NULL
);

CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    descripcion TEXT
);

CREATE TABLE libros (
    id_libro SERIAL PRIMARY KEY,
    titulo VARCHAR(180) NOT NULL,
    isbn VARCHAR(30) NOT NULL UNIQUE,
    anio_publicacion INT NOT NULL CHECK (anio_publicacion > 0),
    stock_total INT NOT NULL DEFAULT 1 CHECK (stock_total >= 0),
    id_autor INT NOT NULL REFERENCES autores(id_autor),
    id_categoria INT NOT NULL REFERENCES categorias(id_categoria)
);

CREATE TABLE lectores (
    id_lector SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(140) NOT NULL,
    correo VARCHAR(140) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE prestamos (
    id_prestamo SERIAL PRIMARY KEY,
    id_libro INT NOT NULL REFERENCES libros(id_libro),
    id_lector INT NOT NULL REFERENCES lectores(id_lector),
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_prevista DATE NOT NULL,
    devuelto BOOLEAN NOT NULL DEFAULT FALSE,
    CHECK (fecha_devolucion_prevista >= fecha_prestamo)
);
