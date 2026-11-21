INSERT INTO autores (nombre, nacionalidad) VALUES
('Gabriel García Márquez', 'Colombiana'),
('Isabel Allende', 'Chilena'),
('Jorge Luis Borges', 'Argentina'),
('Mario Vargas Llosa', 'Peruana'),
('Laura Esquivel', 'Mexicana'),
('Julio Cortázar', 'Argentina'),
('Piedad Bonnett', 'Colombiana'),
('Carlos Fuentes', 'Mexicana'),
('Clarice Lispector', 'Brasileña'),
('Eduardo Galeano', 'Uruguaya');

INSERT INTO categorias (nombre, descripcion) VALUES
('Novela', 'Narrativa de ficción extensa.'),
('Cuento', 'Relatos breves de ficción.'),
('Ensayo', 'Textos de análisis y reflexión.'),
('Poesía', 'Obras escritas en verso o prosa poética.'),
('Historia', 'Obras sobre hechos históricos.'),
('Ciencia', 'Divulgación e investigación científica.'),
('Infantil', 'Lecturas dirigidas a público infantil.'),
('Fantasía', 'Narraciones con elementos fantásticos.'),
('Biografía', 'Relatos de vida de personas reales.'),
('Teatro', 'Obras escritas para representación escénica.');

INSERT INTO libros
    (titulo, isbn, anio_publicacion, stock_total, id_autor, id_categoria)
VALUES
('Cien años de soledad', '978-0307474728', 1967, 4, 1, 1),
('La casa de los espíritus', '978-8401352836', 1982, 3, 2, 1),
('Ficciones', '978-0802130303', 1944, 5, 3, 2),
('La ciudad y los perros', '978-8432216475', 1963, 2, 4, 1),
('Como agua para chocolate', '978-0385420174', 1989, 3, 5, 1),
('Rayuela', '978-8437604572', 1963, 2, 6, 1),
('Lo que no tiene nombre', '978-9588806123', 2013, 4, 7, 3),
('La muerte de Artemio Cruz', '978-8437604947', 1962, 2, 8, 1),
('La hora de la estrella', '978-0811218015', 1977, 3, 9, 1),
('Las venas abiertas de América Latina', '978-9505116944', 1971, 2, 10, 3);

INSERT INTO lectores (nombre_completo, correo, telefono, activo) VALUES
('Ana Martínez', 'ana.martinez@example.com', '3001112233', TRUE),
('Luis Rodríguez', 'luis.rodriguez@example.com', '3002223344', TRUE),
('María Gómez', 'maria.gomez@example.com', '3003334455', TRUE),
('Carlos Pérez', 'carlos.perez@example.com', '3004445566', TRUE),
('Sofía Torres', 'sofia.torres@example.com', '3005556677', TRUE),
('Diego Ramírez', 'diego.ramirez@example.com', '3006667788', TRUE),
('Valentina Castro', 'valentina.castro@example.com', '3007778899', TRUE),
('Andrés Herrera', 'andres.herrera@example.com', '3008889900', TRUE),
('Camila Rojas', 'camila.rojas@example.com', '3009990011', TRUE),
('Mateo Díaz', 'mateo.diaz@example.com', '3010001122', FALSE);

INSERT INTO prestamos
    (id_libro, id_lector, fecha_prestamo, fecha_devolucion_prevista, devuelto)
VALUES
(1, 1, '2026-01-05', '2026-01-19', TRUE),
(2, 2, '2026-01-10', '2026-01-24', TRUE),
(3, 3, '2026-02-01', '2026-02-15', TRUE),
(4, 4, '2026-02-12', '2026-02-26', FALSE),
(5, 5, '2026-03-03', '2026-03-17', TRUE),
(6, 6, '2026-03-18', '2026-04-01', FALSE),
(7, 7, '2026-04-02', '2026-04-16', FALSE),
(8, 8, '2026-04-10', '2026-04-24', TRUE),
(9, 9, '2026-05-01', '2026-05-15', FALSE),
(10, 10, '2026-05-11', '2026-05-25', FALSE);
