# Recursos del taller — Conexión IA UCE 2026

Materiales para la actividad práctica del taller: la creación de **dos agentes de inteligencia artificial** orientados a la exploración de literatura científica y al análisis bibliométrico con enfoque en integridad científica.

## Contenido del repositorio

```
Recursos/
├── agente-1/                      Explorador Científico
│   ├── instruccion_general.md     Nombre, descripción e instrucción general del agente
│   └── prompts.md                 Prompts para crear sus herramientas y probarlo
└── agente-2/                      Radar Científico IA
    ├── instruccion_general.md     Nombre, descripción e instrucción general del agente
    ├── Skills/
    │   └── SKILL.md               Skill de análisis universitario (SCImago IRIS + OpenAlex)
    └── Conocimiento/              Base de conocimiento SCImago IRIS — Ecuador
        ├── scimago_iris_ecuador.md
        ├── scimago_iris_fichas_ecuador.md
        ├── scimago_iris_indice_ecuador.md
        └── scimago_iris_metodologia.md
```

## Agente 1 — Explorador Científico

Agente para la **búsqueda, consulta y visualización de publicaciones científicas** mediante la API de [OpenAlex](https://openalex.org). Permite explorar literatura académica, autores e instituciones.

**Cómo armarlo:**

1. Crea un agente nuevo y copia el nombre, la descripción y la instrucción general desde [agente-1/instruccion_general.md](agente-1/instruccion_general.md).
2. Crea sus herramientas con los dos prompts de construcción incluidos en [agente-1/prompts.md](agente-1/prompts.md):
   - **Métodos básicos:** comprobación de conexión, búsqueda de publicaciones por término y recuperación de metadatos por ID o DOI.
   - **Métodos por institución y autor:** búsqueda de publicaciones filtrada por institución o por autor (nombre, ID u ORCID).
3. Configura la variable de entorno `api_key_open_alex` para la autenticación.

**Cómo probarlo:** el mismo archivo [prompts.md](agente-1/prompts.md) incluye un listado de prompts de ejemplo: comprobar la conexión, buscar artículos por tema y período, recuperar metadatos, consultar publicaciones de una institución o de un autor, y generar tablas y dashboards con los resultados.

## Agente 2 — Radar Científico IA

Agente especializado en **análisis bibliométrico, integridad científica y gestión estratégica de la investigación**. Combina dos fuentes:

- **OpenAlex (vía MCP):** producción científica, subcampos, impacto de citación y colaboración.
- **Base de conocimiento SCImago IRIS:** indicadores de riesgo de integridad científica de las 30 universidades del Ecuador (instantánea del 23-11-2026), con fichas institucionales, índice nacional y metodología.

**Cómo armarlo:**

1. Crea un agente nuevo y copia el nombre, la descripción y la instrucción general desde [agente-2/instruccion_general.md](agente-2/instruccion_general.md).
2. Agrega la skill [agente-2/Skills/SKILL.md](agente-2/Skills/SKILL.md), que define el flujo de trabajo del agente: decidir, consultar, comprobar y responder, con rutas separadas para OpenAlex, la base IRIS y el análisis integrado.
3. Carga los cuatro archivos de [agente-2/Conocimiento/](agente-2/Conocimiento/) como base de conocimiento del agente.
4. Conecta el servidor MCP de OpenAlex.

**Qué permite hacer:** comparar la producción y el impacto de universidades ecuatorianas, consultar su posición en el índice IRIS, interpretar los nueve indicadores de integridad (retractaciones, autocitación, hiperautoría, revistas descontinuadas, entre otros) y generar informes o dashboards verificables, distinguiendo siempre entre datos directos, contexto indirecto e información no disponible.

## Notas importantes

- Los indicadores SCImago IRIS son **señales estructurales normalizadas de riesgo, no pruebas de mala conducta**. La skill del agente 2 obliga a citar la fuente de cada dato y a declarar lo que no se pudo verificar.
- La base de conocimiento corresponde a una instantánea fija (23 de noviembre de 2026); los valores no se actualizan automáticamente.
- Las instrucciones detalladas de la actividad práctica se encuentran en la carpeta `Documentos` del taller.
