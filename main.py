import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

ARCHIVO = "consultas.json"


def cargar_consultas():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def siguiente_id(consultas):
    numeros = []

    for consulta in consultas:
        identificador = consulta.get("id", "")

        if identificador.startswith("CF-"):
            try:
                numeros.append(int(identificador[3:]))
            except ValueError:
                pass

    siguiente = max(numeros, default=0) + 1
    return f"CF-{siguiente:06d}"


def guardar_consulta(resultado):
    consultas = cargar_consultas()

    resultado["id"] = siguiente_id(consultas)
    resultado["fecha"] = datetime.now().isoformat(timespec="seconds")

    consultas.append(resultado)

    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(consultas, archivo, ensure_ascii=False, indent=2)

    return resultado


def contiene_alguna(texto, palabras):
    return any(palabra in texto for palabra in palabras)


def clasificar_consulta(consulta):
    texto = consulta.lower()

    if contiene_alguna(texto, [
        "llc",
        "empresa",
        "sociedad",
        "estructura empresarial",
        "crear una empresa",
        "crear empresa"
    ]):
        return "Estructura empresarial"

    if contiene_alguna(texto, [
        "criptomoneda",
        "criptomonedas",
        "bitcoin",
        "ethereum",
        "usdt",
        "crypto",
        "cripto",
        "ganancias cripto",
        "ganancias con bitcoin",
        "activos digitales"
    ]):
        return "Fiscalidad cripto"

    if contiene_alguna(texto, [
        "hacienda",
        "impuestos",
        "impuesto",
        "fiscalidad",
        "declarar",
        "declaración",
        "declaracion",
        "notificación fiscal",
        "notificacion fiscal",
        "tributario",
        "tributaria",
        "requerimiento fiscal",
        "inspección fiscal",
        "inspeccion fiscal",
        "multa fiscal",
        "sanción fiscal",
        "sancion fiscal"
    ]):
        return "Fiscalidad / legal"

    if contiene_alguna(texto, [
        "trading",
        "trader",
        "trade",
        "cuenta de fondeo",
        "cuentas de fondeo"
    ]):
        return "Trading"

    return "Otra consulta"


def determinar_prioridad(consulta):
    texto = consulta.lower()

    if contiene_alguna(texto, [
        "urgente",
        "urgencia",
        "hacienda",
        "inspección",
        "inspeccion",
        "notificación",
        "notificacion",
        "requerimiento",
        "multa",
        "sanción",
        "sancion",
        "demanda",
        "problema legal",
        "bloqueado"
    ]):
        return "Alta"

    if contiene_alguna(texto, [
        "quiero información",
        "quiero informacion",
        "quiero crear",
        "quiero abrir",
        "quiero saber",
        "cómo crear",
        "como crear",
        "cómo declarar",
        "como declarar",
        "impuestos",
        "fiscalidad",
        "asesoría",
        "asesoria",
        "información sobre",
        "informacion sobre"
    ]):
        return "Media"

    return "Baja"


def necesita_atencion_humana(consulta, prioridad):
    texto = consulta.lower()

    if prioridad == "Alta":
        return True

    if contiene_alguna(texto, [
        "hacienda",
        "inspección",
        "inspeccion",
        "notificación",
        "notificacion",
        "requerimiento",
        "multa",
        "sanción",
        "sancion",
        "demanda",
        "problema legal"
    ]):
        return True

    return False


def generar_respuesta(tipo, nombre, prioridad):
    respuestas = {
        "Estructura empresarial": (
            f"Hola {nombre}. Hemos recibido tu consulta sobre "
            "estructura empresarial. Un especialista puede revisar "
            "tu caso y orientarte sobre las opciones disponibles."
        ),

        "Fiscalidad cripto": (
            f"Hola {nombre}. Hemos recibido tu consulta relacionada "
            "con fiscalidad de criptomonedas. Un especialista puede "
            "revisar tu situación y orientarte sobre los aspectos "
            "fiscales correspondientes."
        ),

        "Fiscalidad / legal": (
            f"Hola {nombre}. Hemos recibido tu consulta relacionada "
            "con fiscalidad o asuntos legales. Un especialista puede "
            "revisar tu caso y orientarte sobre los pasos correspondientes."
        ),

        "Trading": (
            f"Hola {nombre}. Hemos recibido tu consulta sobre trading. "
            "Un especialista puede revisar tu caso y orientarte "
            "sobre las opciones disponibles."
        ),

        "Otra consulta": (
            f"Hola {nombre}. Hemos recibido tu consulta. "
            "La hemos registrado para que pueda ser revisada "
            "por el equipo correspondiente."
        )
    }

    respuesta = respuestas[tipo]

    if prioridad == "Alta":
        respuesta += (
            " Debido a la naturaleza de tu consulta, la hemos "
            "marcado para revisión prioritaria."
        )

    return respuesta


def procesar_consulta(datos):
    nombre = datos.get("nombre", "").strip()
    email = datos.get("email", "").strip()
    consulta = datos.get("consulta", "").strip()

    if not nombre or not email or not consulta:
        return {
            "ok": False,
            "error": "Faltan datos obligatorios"
        }

    tipo = clasificar_consulta(consulta)
    prioridad = determinar_prioridad(consulta)

    atencion_humana = necesita_atencion_humana(
        consulta,
        prioridad
    )

    respuesta = generar_respuesta(
        tipo,
        nombre,
        prioridad
    )

    return {
        "ok": True,
        "cliente": {
            "nombre": nombre,
            "email": email
        },
        "consulta": consulta,
        "tipo": tipo,
        "prioridad": prioridad,
        "atencion_humana": atencion_humana,
        "estado": "Pendiente de atención",
        "respuesta_automatica": respuesta
    }


class Handler(BaseHTTPRequestHandler):

    def enviar_json(self, datos, codigo=200):
        respuesta = json.dumps(
            datos,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        self.send_response(codigo)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(respuesta))
        )
        self.end_headers()

        self.wfile.write(respuesta)

    def do_POST(self):
        if self.path != "/consulta":
            self.enviar_json({
                "ok": False,
                "error": "Endpoint no encontrado"
            }, 404)
            return

        try:
            longitud = int(
                self.headers.get("Content-Length", 0)
            )

            cuerpo = self.rfile.read(longitud)
            datos = json.loads(cuerpo.decode("utf-8"))

            resultado = procesar_consulta(datos)

            if resultado["ok"]:
                resultado = guardar_consulta(resultado)

            self.enviar_json(
                resultado,
                200 if resultado["ok"] else 400
            )

        except json.JSONDecodeError:
            self.enviar_json({
                "ok": False,
                "error": "JSON inválido"
            }, 400)

        except Exception as e:
            self.enviar_json({
                "ok": False,
                "error": str(e)
            }, 500)

    def do_GET(self):
        if self.path == "/":
            self.enviar_json({
                "ok": True,
                "servicio": "CryptoFiscal Lead Automation",
                "endpoints": {
                    "POST /consulta": "Registrar y procesar una consulta",
                    "GET /consultas": "Consultar solicitudes registradas"
                }
            })
            return

        if self.path == "/consultas":
            consultas = cargar_consultas()

            self.enviar_json({
                "ok": True,
                "total": len(consultas),
                "consultas": consultas
            })
            return

        self.enviar_json({
            "ok": False,
            "error": "Endpoint no encontrado"
        }, 404)


servidor = HTTPServer(("127.0.0.1", 8000), Handler)

print("======================================")
print(" CryptoFiscal Lead Automation")
print("======================================")
print("Servidor: http://127.0.0.1:8000")
print("POST /consulta  -> procesar consulta")
print("GET  /consultas -> listar consultas")
print("======================================")
print("Pulsa Ctrl+C para detenerlo.")

servidor.serve_forever()
