# PROMPTS Taller

**Creación de herramientas (Métodos básicos)**

```
Crea una herramienta para consumir la API de OpenAlex (https://api.openalex.org), utilizando la variable de entorno api_key_open_alex para la autenticación.

Implementa los siguientes métodos:

conexion_open_alex: sin parámetros de entrada. Devuelve el estado de la conexión y el código HTTP.

search_open_alex_works: recibe un término de búsqueda, año inicial, año final y número máximo de resultados (5 por defecto). Devuelve el total de resultados y una lista con ID de OpenAlex, título, autores, año, DOI, revista y número de citas.

get_open_alex_work: recibe un ID de OpenAlex o DOI. Devuelve los metadatos de la publicación, incluyendo resumen, autores, afiliaciones y número de citas.

Define cada método como una función independiente, con parámetros tipados y documentación.

Utiliza JSON como formato de salida, gestiona los errores sin exponer la API key y evita utilizar locals(), globals(), eval() o exec().

Genera código sencillo, sin bloques redundantes ni referencias a funciones o variables no definidas, salvo las proporcionadas por la plataforma.
```

**Creación de herramientas (Métodos por institución y autor)**

```
Amplía la herramienta de OpenAlex existente añadiendo únicamente dos métodos:

- `search_open_alex_works_by_institution`: recibe el nombre o ID de una institución, término de búsqueda opcional, año inicial, año final y número máximo de resultados (5 por defecto). Devuelve el nombre e ID de la institución, total de resultados y lista de publicaciones.
- `search_open_alex_works_by_author`: recibe el nombre, ID u ORCID de un autor, término de búsqueda opcional, año inicial, año final y número máximo de resultados (5 por defecto). Devuelve el nombre e ID del autor, total de resultados y lista de publicaciones.

Consulta primero `/institutions` o `/authors` para identificar la entidad y después `/works` para recuperar sus publicaciones mediante los filtros `institutions.id` o `author.id`, respectivamente.

Si existen múltiples coincidencias, devuelve las opciones disponibles. Recuerda que `results` es una lista de diccionarios.

Mantén las siguientes condiciones:
- No modifiques los tres métodos existentes.
- Implementa únicamente las dos nuevas funciones, sin funciones auxiliares adicionales.
- Utiliza `requests` y `get_env("api_key_open_alex")`.
- Utiliza tipos básicos de Python: `str`, `int`, `dict` y `list`, sin importar `typing`.
- No utilices `locals()`, `globals()`, `eval()` ni `exec()`.
- Mantén el formato JSON de los métodos existentes y gestiona los errores sin exponer la API key.

Comprueba que el código no contenga referencias a variables o funciones no definidas.
```

**Listado de prompts**
- Crea un dashboard interactivo que incluya un diagrama de dispersión utilizando datos de prueba para las variables X e Y. Incorpora 30 puntos de datos, etiquetas en los ejes, una línea de tendencia y el coeficiente de correlación. Utiliza un diseño limpio y permite visualizar los valores de cada punto al pasar el cursor sobre él.
- Comprueba la conexión con OpenAlex.
- Busca 5 artículos sobre inteligencia artificial aplicada a la desnutrición infantil entre 2022 y 2026.
- Recupera los metadatos completos y el resumen del primer artículo encontrado.
- Presenta las publicaciones recuperadas en una tabla y genera un gráfico de barras con su número de citas.
- Recupera 5 publicaciones de la Universidad de Vigo entre 2022 y 2026.
- Busca 5 publicaciones sobre inteligencia artificial de la Escuela Politécnica Nacional entre 2022 y 2026.
- Recupera 5 publicaciones de Yoshua Bengio entre 2022 y 2026.
- Busca al investigador Jorge Galán Mena identifica sus posibles afiliaciones.
- Genera un dashboard de las publicaciones recuperadas que incluya una tabla de artículos, distribución por año y número de citas.