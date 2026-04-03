# Payments Service

Microservicio de pagos de TravelHub para el MVP de procesamiento seguro.

## Responsabilidades

- Recibir solo tokens de pago generados fuera del backend
- Ejecutar el cargo a traves de un gateway desacoplado
- Evitar cobros duplicados accidentales
- Registrar eventos del pago y generar recibo en exitos
- Rechazar requests de pago sin transporte seguro cuando TLS es exigido

## Alcance MVP de HU016

- El backend no recibe numero de tarjeta, CVV ni fecha de expiracion
- El contrato HTTP acepta unicamente `payment_method_token`
- Se persiste solo el hash del token, nunca el token en claro
- Se genera recibo cuando el pago queda `confirmed`
- Se devuelve `failure_reason` cuando el cargo falla
- Se rechazan duplicados por `idempotency_key` y por ventana corta de 2 segundos

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/payments/charges` | Crear cargo con token de pago |
| GET | `/api/v1/payments/{payment_id}` | Consultar un pago |
| GET | `/api/v1/payments/{payment_id}/events` | Listar eventos del pago |

## Ejecucion

### Con Docker

```bash
make docker-up
# El servicio queda en http://localhost:8002
```

### Local

```bash
cd services/payments
pip install -r requirements.txt
PYTHONPATH=src uvicorn entrypoints.api.main:app --reload --port 8002
```

### Tests

```bash
make payments-test
# o
PYTHONPATH=services/payments/src pytest services/payments/tests/ -v
```

## Configuracion

| Variable | Default | Descripcion |
|----------|---------|-------------|
| `RDS_HOSTNAME` | `localhost` | Host de PostgreSQL |
| `RDS_PORT` | `5432` | Puerto de PostgreSQL |
| `RDS_USERNAME` | `travelhub_user` | Usuario de BD |
| `RDS_PASSWORD` | `travelhub_pass` | Contrasena de BD |
| `RDS_DB_NAME` | `travelhub` | Nombre de la BD |
| `DB_SCHEMA` | `payments_schema` | Schema de PostgreSQL |
| `PAYMENT_PROVIDER` | `fake_stripe` | Gateway del MVP |
| `PAYMENT_DUPLICATE_WINDOW_SECONDS` | `2` | Ventana anti-duplicados |
| `PAYMENT_INTEGRITY_SECRET` | - | Secreto HMAC para checksum |
| `ENFORCE_TLS_HEADER` | `True` | Exige `X-Forwarded-Proto: https` |

## Notas de arquitectura

- Este repo backend deja listo el contrato token-only para integrarse luego con Stripe Elements desde el frontend.
- En el MVP actual el gateway por defecto es simulado para permitir pruebas automatizadas sin depender de servicios externos.
- Los eventos `reservation.confirmation.requested` e `inventory.update.requested` dejan trazabilidad para la futura integracion asincrona.
