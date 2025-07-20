import httpx
import json
from datetime import datetime

# URL base de tu API de FastAPI
BASE_URL = "http://localhost:8000"  # Asegúrate de que esta URL sea correcta

# Ruta al archivo de datos
DATA_FILE = "default_data/data.json"


async def post_data(
    client: httpx.AsyncClient, endpoint: str, data: dict, token: str | None = None
):
    """
    Realiza una petición POST a un endpoint específico de la API.

    Args:
        client (httpx.AsyncClient): Cliente HTTPX para realizar la petición.
        endpoint (str): El endpoint de la API (ej. "/usuarios/").
        data (dict): El cuerpo de la petición en formato diccionario.
        token (str, optional): Token de autorización si es necesario. Defaults to None.

    Returns:
        dict | None: La respuesta JSON de la API si la petición fue exitosa, de lo contrario None.
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = await client.post(
            f"{BASE_URL}{endpoint}", json=data, headers=headers
        )
        response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
        print(f"✅ Éxito al crear {endpoint}: {response.status_code}")
        return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"❌ Error al crear {endpoint} (Estado: {e.response.status_code}): {e.response.text}"
        )
    except httpx.RequestError as e:
        print(f"❌ Error de red al crear {endpoint}: {e}")
    return None


async def login_user(client: httpx.AsyncClient, username: str, password: str):
    """
    Realiza una petición de login para obtener un token de acceso.

    Args:
        client (httpx.AsyncClient): Cliente HTTPX para realizar la petición.
        username (str): Nombre de usuario para el login.
        password (str): Contraseña para el login.

    Returns:
        str | None: El token de acceso si el login fue exitoso, de lo contrario None.
    """
    login_data = {"username": username, "password": password}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }  # FastAPI espera form-urlencoded para login

    try:
        response = await client.post(
            f"{BASE_URL}/auth/login", data=login_data, headers=headers
        )
        response.raise_for_status()
        token_info = response.json()
        print(f"✅ Login exitoso para {username}")
        return token_info.get("access_token")
    except httpx.HTTPStatusError as e:
        print(
            f"❌ Error de login para {username} (Estado: {e.response.status_code}): {e.response.text}"
        )
    except httpx.RequestError as e:
        print(f"❌ Error de red durante el login para {username}: {e}")
    return None


async def seed_data():
    """
    Función principal para cargar y enviar los datos de prueba a la API.
    """
    print("Iniciando el proceso de siembra de datos...")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data_to_seed = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo {DATA_FILE} no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo {DATA_FILE} no es un JSON válido.")
        return

    async with httpx.AsyncClient() as client:
        # Diccionario para mapear nombres de usuario a IDs de usuario creados
        user_ids_map = {}
        # Token de autenticación (se usará el del admin para la mayoría de las operaciones)
        auth_token = None

        # 1. Sembrar Estados de Elementos de Inventario
        print("\n--- Sembrando Estados de Elementos de Inventario ---")
        for item_data in data_to_seed.get("estados_elementos_inventario", []):
            await post_data(client, "/inventario/estado_elemento_inventario", item_data)

        # 2. Sembrar Tipos de Movimientos de Inventario
        print("\n--- Sembrando Tipos de Movimientos de Inventario ---")
        for item_data in data_to_seed.get("tipos_movimientos_inventario", []):
            await post_data(client, "/inventario/tipo_movimiento_inventario", item_data)

        # 3. Sembrar Tipos de Precios de Elementos de Inventario
        print("\n--- Sembrando Tipos de Precios de Elementos de Inventario ---")
        for item_data in data_to_seed.get("tipos_precios_elementos_inventario", []):
            await post_data(
                client, "/inventario/tipo_precio_elemento_inventario", item_data
            )

        # 4. Sembrar Usuarios
        print("\n--- Sembrando Usuarios ---")
        for user_data in data_to_seed.get("usuarios", []):
            # Clonar el diccionario para no modificar el original al eliminar la contraseña
            user_create_data = user_data.copy()
            password = user_create_data.pop(
                "password"
            )  # Eliminar la contraseña del payload de creación si no es esperada por el modelo UsuarioCreate
            # Si UsuarioCreate espera la contraseña, no hacer pop.
            # En tu OpenAPI, UsuarioCreate sí espera 'password', así que no la eliminamos.
            user_create_data["password"] = (
                password  # Asegurarse de que la contraseña esté presente
            )

            response_json = await post_data(client, "/usuarios/", user_create_data)
            if response_json and "username" in response_json:
                # Asumimos que la respuesta incluye el ID del usuario creado
                # Si el ID no se devuelve, esta parte necesitará ajuste o una consulta GET
                # Para este ejemplo, asumimos que el ID se devuelve o que podemos usar el ID del JSON si se envió
                # Sin embargo, el OpenAPI para UsuarioBase no muestra 'id'.
                # Para propósitos de este script de siembra, vamos a asumir que los IDs de usuario se asignan secuencialmente
                # o que el `usuario_id` en `elementos_inventario` y `movimientos_inventario` puede ser null.
                # Si necesitas el ID real, tendrías que hacer una consulta GET después de la creación.
                # Para simplificar, si tu API devuelve el ID en la respuesta de creación, úsalo.
                # Si no, y si el `usuario_id` es `Optional`, puedes dejarlo como `null` en el JSON o mapearlo manualmente.
                # Para este script, mapearemos el username a un ID ficticio o al ID que venga en la respuesta si existe.
                # Si tu API no devuelve el ID, y el ID es auto-incrementable, deberías obtenerlo de otra forma.
                # Para este ejemplo, asignaremos IDs basados en el orden de creación para `usuario_id` en otros modelos.
                # Esto es una simplificación y puede no coincidir con los IDs reales de la DB.
                # Una mejor práctica sería obtener el ID real de la respuesta o de una consulta.
                user_ids_map[response_json["username"]] = (
                    len(user_ids_map) + 1
                )  # Asignar un ID secuencial temporal

                if user_data["username"] == "admin_user":
                    auth_token = await login_user(
                        client, user_data["username"], user_data["password"]
                    )
                    if auth_token:
                        print(
                            f"Token de admin_user obtenido: {auth_token[:20]}..."
                        )  # Mostrar solo una parte del token
                    else:
                        print(
                            "No se pudo obtener el token para admin_user. Las siguientes operaciones podrían fallar."
                        )

        # 5. Sembrar Elementos de Inventario
        print("\n--- Sembrando Elementos de Inventario ---")
        for item_data in data_to_seed.get("elementos_inventario", []):
            # Asegurarse de que el usuario_id sea válido si se usa
            if (
                item_data.get("usuario_id")
                and item_data["usuario_id"] not in user_ids_map.values()
            ):
                # Esto es una simplificación. En un escenario real, el usuario_id debería existir.
                # Aquí asumimos que los IDs en data.json coinciden con los IDs que la DB asignará.
                # Si no, esto fallará o necesitará lógica para mapear a IDs reales de usuarios creados.
                pass  # No hacemos nada si el ID no está en nuestro mapa temporal

            # Formatear la fecha si es necesario
            if "created_at" in item_data and isinstance(item_data["created_at"], str):
                try:
                    # Validar y reformatear si es necesario, aunque el JSON ya tiene el formato correcto
                    datetime.fromisoformat(item_data["created_at"])
                except ValueError:
                    print(
                        f"Advertencia: Formato de fecha incorrecto para created_at en ElementoInventario: {item_data['created_at']}"
                    )
                    item_data["created_at"] = (
                        datetime.now().isoformat()
                    )  # Usar fecha actual como fallback

            await post_data(
                client, "/inventario/elemento_inventario", item_data, token=auth_token
            )

        # 6. Sembrar Elementos Compuestos de Inventario
        print("\n--- Sembrando Elementos Compuestos de Inventario ---")
        for item_data in data_to_seed.get("elementos_compuestos_inventario", []):
            if "created_at" in item_data and isinstance(item_data["created_at"], str):
                try:
                    datetime.fromisoformat(item_data["created_at"])
                except ValueError:
                    print(
                        f"Advertencia: Formato de fecha incorrecto para created_at en ElementoCompuestoInventario: {item_data['created_at']}"
                    )
                    item_data["created_at"] = datetime.now().isoformat()

            await post_data(
                client,
                "/inventario/elemento_compuesto_inventario",
                item_data,
                token=auth_token,
            )

        # 7. Sembrar Precios de Elementos de Inventario
        print("\n--- Sembrando Precios de Elementos de Inventario ---")
        for item_data in data_to_seed.get("precios_elementos_inventario", []):
            # Asegurarse de que las fechas estén en el formato correcto
            if "fini" in item_data and isinstance(item_data["fini"], str):
                try:
                    datetime.fromisoformat(item_data["fini"])
                except ValueError:
                    print(
                        f"Advertencia: Formato de fecha incorrecto para fini en PrecioElementoInventario: {item_data['fini']}"
                    )
                    item_data["fini"] = datetime.now().isoformat()
            if "ffin" in item_data and isinstance(item_data["ffin"], str):
                try:
                    datetime.fromisoformat(item_data["ffin"])
                except ValueError:
                    print(
                        f"Advertencia: Formato de fecha incorrecto para ffin en PrecioElementoInventario: {item_data['ffin']}"
                    )
                    item_data["ffin"] = None  # O dejarlo como None si es opcional

            await post_data(
                client,
                "/inventario/precio_elemento_inventario",
                item_data,
                token=auth_token,
            )

        # 8. Sembrar Movimientos de Inventario
        print("\n--- Sembrando Movimientos de Inventario ---")
        for item_data in data_to_seed.get("movimientos_inventario", []):
            if "created_at" in item_data and isinstance(item_data["created_at"], str):
                try:
                    datetime.fromisoformat(item_data["created_at"])
                except ValueError:
                    print(
                        f"Advertencia: Formato de fecha incorrecto para created_at en MovimientoInventario: {item_data['created_at']}"
                    )
                    item_data["created_at"] = datetime.now().isoformat()

            await post_data(
                client, "/inventario/movimiento_inventario", item_data, token=auth_token
            )

    print("\nProceso de siembra de datos completado.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_data())
