--
-- PostgreSQL database dump
--

\restrict nbQF7mO2JgINprZJ2oaDeVFGrJBM54vTN3nFosRUckegbXn4GpJXc3Msmobjvgo

-- Dumped from database version 16.16 (Debian 16.16-1.pgdg13+1)
-- Dumped by pg_dump version 16.16 (Debian 16.16-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: autores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.autores (
    id_autor integer NOT NULL,
    nombre character varying(120) NOT NULL,
    nacionalidad character varying(80) NOT NULL
);


--
-- Name: autores_id_autor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.autores_id_autor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: autores_id_autor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.autores_id_autor_seq OWNED BY public.autores.id_autor;


--
-- Name: categorias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nombre character varying(80) NOT NULL,
    descripcion text
);


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.categorias_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.categorias_id_categoria_seq OWNED BY public.categorias.id_categoria;


--
-- Name: lectores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lectores (
    id_lector integer NOT NULL,
    nombre_completo character varying(140) NOT NULL,
    correo character varying(140) NOT NULL,
    telefono character varying(30),
    activo boolean DEFAULT true NOT NULL
);


--
-- Name: lectores_id_lector_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lectores_id_lector_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lectores_id_lector_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lectores_id_lector_seq OWNED BY public.lectores.id_lector;


--
-- Name: libros; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.libros (
    id_libro integer NOT NULL,
    titulo character varying(180) NOT NULL,
    isbn character varying(30) NOT NULL,
    anio_publicacion integer NOT NULL,
    stock_total integer DEFAULT 1 NOT NULL,
    id_autor integer NOT NULL,
    id_categoria integer NOT NULL,
    CONSTRAINT libros_anio_publicacion_check CHECK ((anio_publicacion > 0)),
    CONSTRAINT libros_stock_total_check CHECK ((stock_total >= 0))
);


--
-- Name: libros_id_libro_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.libros_id_libro_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: libros_id_libro_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.libros_id_libro_seq OWNED BY public.libros.id_libro;


--
-- Name: prestamos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prestamos (
    id_prestamo integer NOT NULL,
    id_libro integer NOT NULL,
    id_lector integer NOT NULL,
    fecha_prestamo date NOT NULL,
    fecha_devolucion_prevista date NOT NULL,
    devuelto boolean DEFAULT false NOT NULL,
    CONSTRAINT prestamos_check CHECK ((fecha_devolucion_prevista >= fecha_prestamo))
);


--
-- Name: prestamos_id_prestamo_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prestamos_id_prestamo_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prestamos_id_prestamo_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prestamos_id_prestamo_seq OWNED BY public.prestamos.id_prestamo;


--
-- Name: autores id_autor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autores ALTER COLUMN id_autor SET DEFAULT nextval('public.autores_id_autor_seq'::regclass);


--
-- Name: categorias id_categoria; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias ALTER COLUMN id_categoria SET DEFAULT nextval('public.categorias_id_categoria_seq'::regclass);


--
-- Name: lectores id_lector; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lectores ALTER COLUMN id_lector SET DEFAULT nextval('public.lectores_id_lector_seq'::regclass);


--
-- Name: libros id_libro; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros ALTER COLUMN id_libro SET DEFAULT nextval('public.libros_id_libro_seq'::regclass);


--
-- Name: prestamos id_prestamo; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prestamos ALTER COLUMN id_prestamo SET DEFAULT nextval('public.prestamos_id_prestamo_seq'::regclass);


--
-- Data for Name: autores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.autores (id_autor, nombre, nacionalidad) FROM stdin;
1	Gabriel García Márquez	Colombiana
2	Isabel Allende	Chilena
3	Jorge Luis Borges	Argentina
4	Mario Vargas Llosa	Peruana
5	Laura Esquivel	Mexicana
6	Julio Cortázar	Argentina
7	Piedad Bonnett	Colombiana
8	Carlos Fuentes	Mexicana
9	Clarice Lispector	Brasileña
10	Eduardo Galeano	Uruguaya
\.


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.categorias (id_categoria, nombre, descripcion) FROM stdin;
1	Novela	Narrativa de ficción extensa.
2	Cuento	Relatos breves de ficción.
3	Ensayo	Textos de análisis y reflexión.
4	Poesía	Obras escritas en verso o prosa poética.
5	Historia	Obras sobre hechos históricos.
6	Ciencia	Divulgación e investigación científica.
7	Infantil	Lecturas dirigidas a público infantil.
8	Fantasía	Narraciones con elementos fantásticos.
9	Biografía	Relatos de vida de personas reales.
10	Teatro	Obras escritas para representación escénica.
\.


--
-- Data for Name: lectores; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lectores (id_lector, nombre_completo, correo, telefono, activo) FROM stdin;
1	Ana Martínez	ana.martinez@example.com	3001112233	t
2	Luis Rodríguez	luis.rodriguez@example.com	3002223344	t
3	María Gómez	maria.gomez@example.com	3003334455	t
4	Carlos Pérez	carlos.perez@example.com	3004445566	t
5	Sofía Torres	sofia.torres@example.com	3005556677	t
6	Diego Ramírez	diego.ramirez@example.com	3006667788	t
7	Valentina Castro	valentina.castro@example.com	3007778899	t
8	Andrés Herrera	andres.herrera@example.com	3008889900	t
9	Camila Rojas	camila.rojas@example.com	3009990011	t
10	Mateo Díaz	mateo.diaz@example.com	3010001122	f
\.


--
-- Data for Name: libros; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.libros (id_libro, titulo, isbn, anio_publicacion, stock_total, id_autor, id_categoria) FROM stdin;
1	Cien años de soledad	978-0307474728	1967	4	1	1
2	La casa de los espíritus	978-8401352836	1982	3	2	1
3	Ficciones	978-0802130303	1944	5	3	2
4	La ciudad y los perros	978-8432216475	1963	2	4	1
5	Como agua para chocolate	978-0385420174	1989	3	5	1
6	Rayuela	978-8437604572	1963	2	6	1
7	Lo que no tiene nombre	978-9588806123	2013	4	7	3
8	La muerte de Artemio Cruz	978-8437604947	1962	2	8	1
9	La hora de la estrella	978-0811218015	1977	3	9	1
10	Las venas abiertas de América Latina	978-9505116944	1971	2	10	3
\.


--
-- Data for Name: prestamos; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.prestamos (id_prestamo, id_libro, id_lector, fecha_prestamo, fecha_devolucion_prevista, devuelto) FROM stdin;
1	1	1	2026-01-05	2026-01-19	t
2	2	2	2026-01-10	2026-01-24	t
3	3	3	2026-02-01	2026-02-15	t
4	4	4	2026-02-12	2026-02-26	f
5	5	5	2026-03-03	2026-03-17	t
6	6	6	2026-03-18	2026-04-01	f
7	7	7	2026-04-02	2026-04-16	f
8	8	8	2026-04-10	2026-04-24	t
9	9	9	2026-05-01	2026-05-15	f
10	10	10	2026-05-11	2026-05-25	f
\.


--
-- Name: autores_id_autor_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.autores_id_autor_seq', 13, true);


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.categorias_id_categoria_seq', 16, true);


--
-- Name: lectores_id_lector_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lectores_id_lector_seq', 13, true);


--
-- Name: libros_id_libro_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.libros_id_libro_seq', 13, true);


--
-- Name: prestamos_id_prestamo_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.prestamos_id_prestamo_seq', 18, true);


--
-- Name: autores autores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.autores
    ADD CONSTRAINT autores_pkey PRIMARY KEY (id_autor);


--
-- Name: categorias categorias_nombre_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_nombre_key UNIQUE (nombre);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- Name: lectores lectores_correo_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lectores
    ADD CONSTRAINT lectores_correo_key UNIQUE (correo);


--
-- Name: lectores lectores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lectores
    ADD CONSTRAINT lectores_pkey PRIMARY KEY (id_lector);


--
-- Name: libros libros_isbn_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_isbn_key UNIQUE (isbn);


--
-- Name: libros libros_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_pkey PRIMARY KEY (id_libro);


--
-- Name: prestamos prestamos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_pkey PRIMARY KEY (id_prestamo);


--
-- Name: libros libros_id_autor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_id_autor_fkey FOREIGN KEY (id_autor) REFERENCES public.autores(id_autor);


--
-- Name: libros libros_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.libros
    ADD CONSTRAINT libros_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);


--
-- Name: prestamos prestamos_id_lector_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_id_lector_fkey FOREIGN KEY (id_lector) REFERENCES public.lectores(id_lector);


--
-- Name: prestamos prestamos_id_libro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prestamos
    ADD CONSTRAINT prestamos_id_libro_fkey FOREIGN KEY (id_libro) REFERENCES public.libros(id_libro);


--
-- PostgreSQL database dump complete
--

\unrestrict nbQF7mO2JgINprZJ2oaDeVFGrJBM54vTN3nFosRUckegbXn4GpJXc3Msmobjvgo

