# CryptoFiscal Lead Automation

Demo práctica de automatización de consultas para un entorno de servicios fiscales y crypto.

## Workflow

Cliente
↓
Webhook /consulta
↓
Validación
↓
Clasificación
↓
Prioridad
↓
¿Requiere atención humana?
↓
Respuesta automática
↓
Registro

## Qué hace

El sistema recibe una consulta mediante un endpoint HTTP POST /consulta.

A partir de los datos recibidos:

1. Valida nombre, email y consulta.
2. Clasifica la consulta.
3. Determina su prioridad.
4. Decide si requiere atención humana.
5. Genera una respuesta automática.
6. Asigna un identificador único.
7. Registra la solicitud.

También permite consultar las solicitudes mediante GET /consultas.

## Tecnologías

- Python
- HTTP
- JSON
- Webhooks
- APIs
- Validación de datos
- Automatización de procesos
- Lógica condicional

## Ejemplo

Una consulta sobre Bitcoin puede clasificarse como:

Fiscalidad cripto

Una consulta urgente relacionada con Hacienda puede clasificarse como:

Fiscalidad / legal

y marcarse para atención humana prioritaria.

## Objetivo

Esta demo muestra cómo transformar un proceso manual de recepción y clasificación de consultas en un workflow automatizado.

La implementación actual utiliza reglas deterministas. La arquitectura permite incorporar posteriormente componentes de IA e integraciones externas.

## Ejecución

Requiere Python 3.

Ejecutar:

python main.py

Servidor local:

http://127.0.0.1:8000
