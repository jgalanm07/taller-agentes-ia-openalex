import requests

def conexion_open_alex() -> dict:
    """Verifica la conexión con la API de OpenAlex y el estado de autenticación.

    Args:
        Sin argumentos.

    Returns:
        dict: Diccionario con el estado de la conexión, código HTTP y un mensaje descriptivo.
    """
    url = "https://api.openalex.org/works"
    api_key = get_env("api_key_open_alex")
    params = {}
    if api_key:
        params["api_key"] = api_key
    
    try:
        response = requests.get(url, params=params, timeout=10)
        return {
            "status": "success" if response.status_code == 200 else "error",
            "http_code": response.status_code,
            "message": "Conexión exitosa con OpenAlex." if response.status_code == 200 else f"Error HTTP {response.status_code}"
        }
    except requests.RequestException as e:
        return {
            "status": "error",
            "http_code": 500,
            "message": "Error de red al conectar con OpenAlex."
        }

def search_open_alex_works(query: str, from_year: int = 2020, to_year: int = 2024, max_results: int = 5) -> dict:
    """Busca publicaciones científicas en OpenAlex según término, rango de años y límite.

    Args:
        query: Término de búsqueda para los trabajos académicos
        from_year: Año inicial del filtro temporal
        to_year: Año final del filtro temporal
        max_results: Número máximo de resultados a retornar (por defecto 5)

    Returns:
        dict: Diccionario con el total de resultados y la lista de publicaciones procesadas.
    """
    url = "https://api.openalex.org/works"
    api_key = get_env("api_key_open_alex")
    
    params = {
        "search": query,
        "filter": f"publication_year:{from_year}-{to_year}",
        "per_page": max_results
    }
    if api_key:
        params["api_key"] = api_key
        
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            return {
                "status": "error",
                "http_code": response.status_code,
                "message": f"Error en la consulta HTTP: {response.status_code}"
            }
            
        data = response.json()
        meta = data.get("meta", {})
        results = data.get("results", [])
        
        works_list = []
        for item in results:
            authorships = item.get("authorships", [])
            authors = [auth.get("author", {}).get("display_name", "Desconocido") for auth in authorships]
            
            loc = item.get("primary_location", {}) or {}
            source = loc.get("source", {}) or {}
            journal = source.get("display_name", "N/A") if source else "N/A"
            
            work_info = {
                "openalex_id": item.get("id"),
                "title": item.get("title"),
                "authors": authors,
                "year": item.get("publication_year"),
                "doi": item.get("doi"),
                "journal": journal,
                "cited_by_count": item.get("cited_by_count", 0)
            }
            works_list.append(work_info)
            
        return {
            "status": "success",
            "count": meta.get("count", len(works_list)),
            "results": works_list
        }
    except requests.RequestException:
        return {
            "status": "error",
            "http_code": 500,
            "message": "Error de red al consultar OpenAlex."
        }

def get_open_alex_work(work_id: str) -> dict:
    """Obtiene metadatos detallados de una publicación de OpenAlex por su ID o DOI.

    Args:
        work_id: ID de OpenAlex (ej. W2741809807) o DOI de la publicación

    Returns:
        dict: Diccionario con los metadatos completos, incluyendo resumen, autores, afiliaciones y citas.
    """
    # Si work_id parece un DOI (contiene 10.), lo anteponemos con doi:
    identifier = work_id
    if "10." in work_id and not work_id.startswith("https://"):
        identifier = f"https://doi.org/{work_id}"
        
    url = f"https://api.openalex.org/works/{identifier}"
    api_key = get_env("api_key_open_alex")
    params = {}
    if api_key:
        params["api_key"] = api_key
        
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            return {
                "status": "error",
                "http_code": response.status_code,
                "message": f"Publicación no encontrada o error HTTP: {response.status_code}"
            }
            
        item = response.json()
        
        # Reconstruir el abstract a partir de inverted_index si existe
        abstract = None
        inv_index = item.get("abstract_inverted_index")
        if inv_index:
            try:
                word_positions = []
                for word, positions in inv_index.items():
                    for pos in positions:
                        word_positions.append((pos, word))
                word_positions.sort(key=lambda x: x[0])
                abstract = " ".join([w[1] for w in word_positions])
            except Exception:
                abstract = "No se pudo reconstruir el resumen."
                
        authorships = item.get("authorships", [])
        formatted_authors = []
        for auth in authorships:
            author_name = auth.get("author", {}).get("display_name", "Desconocido")
            institutions = [inst.get("display_name", "Desconocida") for inst in auth.get("institutions", [])]
            formatted_authors.append({
                "author": author_name,
                "institutions": institutions
            })
            
        loc = item.get("primary_location", {}) or {}
        source = loc.get("source", {}) or {}
        journal = source.get("display_name", "N/A") if source else "N/A"
        
        work_details = {
            "openalex_id": item.get("id"),
            "title": item.get("title"),
            "doi": item.get("doi"),
            "year": item.get("publication_year"),
            "journal": journal,
            "cited_by_count": item.get("cited_by_count", 0),
            "abstract": abstract,
            "authorships": formatted_authors
        }
        
        return {
            "status": "success",
            "data": work_details
        }
    except requests.RequestException:
        return {
            "status": "error",
            "http_code": 500,
            "message": "Error de red al consultar la publicación en OpenAlex."
        }

def search_open_alex_works_by_institution(institution_query: str, query: str = "", from_year: int = 2020, to_year: int = 2024, max_results: int = 5) -> dict:
    """Busca publicaciones científicas en OpenAlex filtrando por una institución específica.

    Args:
        institution_query: Nombre o ID de la institución (ej. I12345678 o Harvard University)
        query: Término de búsqueda opcional para los trabajos académicos
        from_year: Año inicial del filtro temporal
        to_year: Año final del filtro temporal
        max_results: Número máximo de resultados a retornar (por defecto 5)

    Returns:
        dict: Diccionario con la información de la institución, total de resultados y lista de publicaciones.
    """
    api_key = get_env("api_key_open_alex")
    inst_id = institution_query
    inst_name = institution_query

    if not institution_query.startswith("I"):
        inst_url = "https://api.openalex.org/institutions"
        inst_params = {"search": institution_query}
        if api_key:
            inst_params["api_key"] = api_key
        try:
            inst_resp = requests.get(inst_url, params=inst_params, timeout=15)
            if inst_resp.status_code != 200:
                return {
                    "status": "error",
                    "http_code": inst_resp.status_code,
                    "message": f"Error al buscar la institución: {inst_resp.status_code}"
                }
            inst_data = inst_resp.json()
            inst_results = inst_data.get("results", [])
            if not inst_results:
                return {
                    "status": "error",
                    "http_code": 404,
                    "message": f"No se encontró ninguna institución con el término: {institution_query}"
                }
            if len(inst_results) > 1:
                options = [{"id": item.get("id"), "display_name": item.get("display_name")} for item in inst_results]
                return {
                    "status": "multiple_choices",
                    "message": "Se encontraron múltiples instituciones coincidentes.",
                    "options": options
                }
            inst_id = inst_results[0].get("id")
            inst_name = inst_results[0].get("display_name")
        except requests.RequestException:
            return {
                "status": "error",
                "http_code": 500,
                "message": "Error de red al buscar la institución en OpenAlex."
            }

    works_url = "https://api.openalex.org/works"
    filter_str = f"institutions.id:{inst_id},publication_year:{from_year}-{to_year}"
    works_params = {
        "filter": filter_str,
        "per_page": max_results
    }
    if query:
        works_params["search"] = query
    if api_key:
        works_params["api_key"] = api_key

    try:
        response = requests.get(works_url, params=works_params, timeout=15)
        if response.status_code != 200:
            return {
                "status": "error",
                "http_code": response.status_code,
                "message": f"Error en la consulta HTTP de trabajos: {response.status_code}"
            }
            
        data = response.json()
        meta = data.get("meta", {})
        results = data.get("results", [])
        
        works_list = []
        for item in results:
            authorships = item.get("authorships", [])
            authors = [auth.get("author", {}).get("display_name", "Desconocido") for auth in authorships]
            
            loc = item.get("primary_location", {}) or {}
            source = loc.get("source", {}) or {}
            journal = source.get("display_name", "N/A") if source else "N/A"
            
            work_info = {
                "openalex_id": item.get("id"),
                "title": item.get("title"),
                "authors": authors,
                "year": item.get("publication_year"),
                "doi": item.get("doi"),
                "journal": journal,
                "cited_by_count": item.get("cited_by_count", 0)
            }
            works_list.append(work_info)
            
        return {
            "status": "success",
            "institution": {
                "id": inst_id,
                "display_name": inst_name
            },
            "count": meta.get("count", len(works_list)),
            "results": works_list
        }
    except requests.RequestException:
        return {
            "status": "error",
            "http_code": 500,
            "message": "Error de red al consultar los trabajos de la institución en OpenAlex."
        }

def search_open_alex_works_by_author(author_query: str, query: str = "", from_year: int = 2020, to_year: int = 2024, max_results: int = 5) -> dict:
    """Busca publicaciones científicas en OpenAlex filtrando por un autor específico.

    Args:
        author_query: Nombre, ID (ej. A12345678) u ORCID de un autor
        query: Término de búsqueda opcional para los trabajos académicos
        from_year: Año inicial del filtro temporal
        to_year: Año final del filtro temporal
        max_results: Número máximo de resultados a retornar (por defecto 5)

    Returns:
        dict: Diccionario con la información del autor, total de resultados y lista de publicaciones.
    """
    api_key = get_env("api_key_open_alex")
    author_id = author_query
    author_name = author_query

    is_id_or_orcid = author_query.startswith("A") or "orcid.org" in author_query or "-" in author_query

    if not is_id_or_orcid:
        author_url = "https://api.openalex.org/authors"
        author_params = {"search": author_query}
        if api_key:
            author_params["api_key"] = api_key
        try:
            author_resp = requests.get(author_url, params=author_params, timeout=15)
            if author_resp.status_code != 200:
                return {
                    "status": "error",
                    "http_code": author_resp.status_code,
                    "message": f"Error al buscar el autor: {author_resp.status_code}"
                }
            author_data = author_resp.json()
            author_results = author_data.get("results", [])
            if not author_results:
                return {
                    "status": "error",
                    "http_code": 404,
                    "message": f"No se encontró ningún autor con el término: {author_query}"
                }
            if len(author_results) > 1:
                options = [{"id": item.get("id"), "display_name": item.get("display_name"), "orcid": item.get("orcid")} for item in author_results]
                return {
                    "status": "multiple_choices",
                    "message": "Se encontraron múltiples autores coincidentes.",
                    "options": options
                }
            author_id = author_results[0].get("id")
            author_name = author_results[0].get("display_name")
        except requests.RequestException:
            return {
                "status": "error",
                "http_code": 500,
                "message": "Error de red al buscar el autor en OpenAlex."
            }

    works_url = "https://api.openalex.org/works"
    filter_str = f"author.id:{author_id},publication_year:{from_year}-{to_year}"
    works_params = {
        "filter": filter_str,
        "per_page": max_results
    }
    if query:
        works_params["search"] = query
    if api_key:
        works_params["api_key"] = api_key

    try:
        response = requests.get(works_url, params=works_params, timeout=15)
        if response.status_code != 200:
            return {
                "status": "error",
                "http_code": response.status_code,
                "message": f"Error en la consulta HTTP de trabajos: {response.status_code}"
            }
            
        data = response.json()
        meta = data.get("meta", {})
        results = data.get("results", [])
        
        works_list = []
        for item in results:
            authorships = item.get("authorships", [])
            authors = [auth.get("author", {}).get("display_name", "Desconocido") for auth in authorships]
            
            loc = item.get("primary_location", {}) or {}
            source = loc.get("source", {}) or {}
            journal = source.get("display_name", "N/A") if source else "N/A"
            
            work_info = {
                "openalex_id": item.get("id"),
                "title": item.get("title"),
                "authors": authors,
                "year": item.get("publication_year"),
                "doi": item.get("doi"),
                "journal": journal,
                "cited_by_count": item.get("cited_by_count", 0)
            }
            works_list.append(work_info)
            
        return {
            "status": "success",
            "author": {
                "id": author_id,
                "display_name": author_name
            },
            "count": meta.get("count", len(works_list)),
            "results": works_list
        }
    except requests.RequestException:
        return {
            "status": "error",
            "http_code": 500,
            "message": "Error de red al consultar los trabajos del autor en OpenAlex."
        }
