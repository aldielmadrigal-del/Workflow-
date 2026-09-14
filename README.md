# CryptoFiscal Lead Automation

Practical automation demo for receiving, classifying and prioritizing client inquiries in a fiscal and crypto services environment.

## What it does

The system receives a client inquiry through an HTTP webhook and automatically:

1. Validates the submitted data.
2. Classifies the inquiry by topic.
3. Assigns a priority level.
4. Determines whether human attention is required.
5. Generates an automatic response.
6. Creates a unique request ID.
7. Stores the request for later consultation.

### Workflow

**Client → Webhook → Validation → Classification → Priority → Human attention decision → Automatic response → Record**

## Example

Input:

> "Quiero saber cómo declarar mis ganancias de Bitcoin."

Automated result:

- **Type:** Fiscalidad cripto
- **Priority:** Media
- **Human attention:** No
- **Automatic response:** Generated
- **Request ID:** CF-000004

Urgent requests related to Hacienda or legal matters are automatically classified as high priority and marked for human review.

## API

### POST /consulta

Receives a client inquiry.

Expected fields:

- `nombre`
- `email`
- `consulta`

### GET /consultas

Returns the stored inquiries.

## Technologies

- Python
- HTTP
- JSON
- Webhooks
- API endpoints
- Data validation
- Conditional logic
- Process automation

## Why this demo

The project demonstrates the core logic behind an operational automation workflow: receiving information, processing it, making decisions based on rules, generating an action, and recording the result.

The current implementation uses deterministic rules. The architecture can later be extended with AI models and external integrations such as WhatsApp, Gmail, CRMs or other automation platforms.

## Run locally

Requires Python 3.

Run:

    python main.py

The server starts locally at:

`http://127.0.0.1:8000`

### Workflow

**Client → Webhook → Validation → Classification → Priority → Human attention decision → Automatic response → Record**

## Example

Input:

> "Quiero saber cómo declarar mis ganancias de Bitcoin."

Automated result:

- **Type:** Fiscalidad cripto
- **Priority:** Media
- **Human attention:** No
- **Automatic response:** Generated
- **Request ID:** CF-000004

Urgent requests related to Hacienda or legal matters are automatically classified as high priority and marked for human review.
