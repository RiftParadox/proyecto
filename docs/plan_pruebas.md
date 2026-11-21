# Plan de pruebas funcionales

## Alcance y ejecución

Los 15 casos se ejecutan contra PostgreSQL con los datos iniciales de `database/seed.sql`. Las pruebas crean datos temporales identificados con un token aleatorio, verifican las respuestas y eliminan sus propios registros. Los casos que comprueban restricciones usan registros sembrados y no los modifican.

Desde la raíz del proyecto y con PostgreSQL iniciado:

```powershell
python -m unittest discover -s tests -v
```

La suite automatizada está en [test_functional.py](../tests/test_functional.py). La salida de la ejecución verificada está en [resultado_pruebas.txt](capturas/resultado_pruebas.txt); las capturas visuales correspondientes se enlazan en cada caso.

## Casos

| ID | Tabla | Operación / entrada | Resultado esperado | Resultado obtenido y evidencia |
|---|---|---|---|---|
| CP-01 | autores | Crear, listar, editar y eliminar autor temporal | Se crea y aparece en listado, se actualiza y se elimina. | **PASS.** `test_01_autores_crear_listar_editar_eliminar`. [Captura](capturas/CP-01-autores.png). |
| CP-02 | autores | Crear sin nombre | Mensaje de campo obligatorio; no se crea el autor. | **PASS.** `test_02_autores_rechaza_nombre_vacio`. [Captura](capturas/CP-02-autores-invalido.png). |
| CP-03 | autores | Eliminar autor con libros | PostgreSQL rechaza el borrado y la app muestra un mensaje. | **PASS.** `test_03_autores_no_se_elimina_si_tiene_libros`. [Captura](capturas/CP-03-autores-relacionado.png). |
| CP-04 | categorias | Crear, listar, editar y eliminar categoría temporal | Se crea, lista, actualiza y elimina. | **PASS.** `test_04_categorias_crear_listar_editar_eliminar`. [Captura](capturas/CP-04-categorias.png). |
| CP-05 | categorias | Crear categoría con nombre ya existente | Mensaje de dato único duplicado; la app no falla. | **PASS.** `test_05_categorias_rechaza_nombre_duplicado`. [Captura](capturas/CP-05-categorias-invalida.png). |
| CP-06 | categorias | Eliminar categoría asignada a libros | PostgreSQL rechaza el borrado y la app muestra un mensaje. | **PASS.** `test_06_categorias_no_se_elimina_si_tiene_libros`. [Captura](capturas/CP-06-categorias-relacionada.png). |
| CP-07 | libros | Crear, listar, editar y eliminar libro temporal | Se guardan los datos y se muestran autor/categoría relacionados. | **PASS.** `test_07_libros_crear_listar_editar_eliminar`. [Captura](capturas/CP-07-libros.png). |
| CP-08 | libros | Crear con ISBN mal formado | Mensaje de validación; no se crea el libro. | **PASS.** `test_08_libros_rechaza_isbn_invalido`. [Captura](capturas/CP-08-libros-invalido.png). |
| CP-09 | libros | Eliminar libro con préstamos | PostgreSQL rechaza el borrado y la app muestra un mensaje. | **PASS.** `test_09_libros_no_se_elimina_si_tiene_prestamos`. [Captura](capturas/CP-09-libros-relacionado.png). |
| CP-10 | lectores | Crear, listar, editar y eliminar lector temporal | Se crea, lista, actualiza y elimina. | **PASS.** `test_10_lectores_crear_listar_editar_eliminar`. [Captura](capturas/CP-10-lectores.png). |
| CP-11 | lectores | Crear con correo no válido | Mensaje de formato inválido; no se crea el lector. | **PASS.** `test_11_lectores_rechaza_correo_invalido`. [Captura](capturas/CP-11-lectores-invalido.png). |
| CP-12 | lectores | Eliminar lector con préstamos | PostgreSQL rechaza el borrado y la app muestra un mensaje. | **PASS.** `test_12_lectores_no_se_elimina_si_tiene_prestamos`. [Captura](capturas/CP-12-lectores-relacionado.png). |
| CP-13 | prestamos | Crear, listar, editar y eliminar préstamo temporal | Se crea, lista con libro/lector, actualiza y elimina. | **PASS.** `test_13_prestamos_crear_listar_editar_eliminar`. [Captura](capturas/CP-13-prestamos.png). |
| CP-14 | prestamos | Registrar devolución anterior al préstamo | Mensaje de validación; no se crea el préstamo. | **PASS.** `test_14_prestamos_rechaza_fecha_invertida`. [Captura](capturas/CP-14-prestamos-invalido.png). |
| CP-15 | prestamos | Enviar una FK inexistente al endpoint | PostgreSQL rechaza la referencia y la app muestra un mensaje entendible. | **PASS.** `test_15_prestamos_rechaza_claves_foraneas_inexistentes`. [Captura](capturas/CP-15-prestamos-fk-invalida.png). |

Los préstamos no son referenciados por otra tabla, por lo que su eliminación no puede probar una restricción de borrado por dependencia; CP-15 prueba el rechazo de claves foráneas inexistentes al registrar un préstamo. La ejecución completa se verifica con la suite automatizada de 15 casos.
