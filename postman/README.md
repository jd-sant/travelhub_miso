# Postman

Archivos listos para probar el MVP de `payments` desde Postman y validar criterios de aceptacion aplicables al backend.

## Archivos

- `travelhub-payments.postman_collection.json`
- `travelhub-local.postman_environment.json`

## Preparacion

1. Importa la coleccion y el environment.
2. Selecciona el environment `TravelHub Local`.
3. Levanta el backend en `http://localhost:8002`.

## Orden sugerido de ejecucion

1. `00 - Health / Health - Payments`
2. `01 - Pago Exitoso / Create Charge - Success`
3. `01 - Pago Exitoso / Get Payment By Id`
4. `01 - Pago Exitoso / List Payment Events - Success`
5. `02 - Pago Fallido / Create Charge - Failure`
6. `02 - Pago Fallido / List Payment Events - Failure`
7. `03 - Duplicados / Create Charge - Duplicate Seed`
8. `03 - Duplicados / Create Charge - Duplicate Replay`
9. `04 - Seguridad Transporte / Create Charge - Missing TLS Header`

## Criterios de aceptacion que valida la coleccion

- El backend recibe solo `payment_method_token` y no expone datos sensibles en respuesta.
- Un cargo exitoso retorna `status=confirmed` y genera recibo.
- Un cargo fallido retorna `status=failed` y un `failure_reason` claro.
- Un intento duplicado en ventana corta es rechazado con `409`.
- Un request sin el header de transporte seguro es rechazado.
- Los eventos de pago dejan trazabilidad para confirmacion y recibo.

## Fuera de alcance de Postman en este repo

- Stripe Elements en navegador.
- Tokenizacion real contra Stripe.
- Confirmacion real de reserva en otro microservicio.
- Enforcement real de TLS 1.2+ por infraestructura.

## Notas

- La coleccion genera `idempotency_key` dinamicos para evitar choques entre corridas.
- El token `pm_fail_insufficient_funds` simula rechazo por fondos insuficientes en el gateway MVP.
