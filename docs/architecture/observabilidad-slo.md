# Observabilidad, SLO y tableros

## Qué pide el enunciado

- Métricas, logs y trazas de la ingesta, de las aplicaciones, de la base, de los tres enlaces WAN y de la llegada de objetos de vuelo.
- Avisos de nodos y fincas sin telemetría por más de 24 horas, de alertas de cultivo no entregadas, de vuelos sin registro persistido, de fumigaciones sin cierre y de invocaciones fallidas que no mutaron el estado.
- Dos SLO con su SLI: entrega de la alerta de cultivo y disponibilidad de la consulta del saco.
- Un tablero operativo y uno de costo, partidos por las etiquetas de fincas, drones, acopio y pruebas.

Todo vive en CloudWatch, en la cuenta `AromaPacifico-Prod` y en la región `us-east-1`. Los registros de auditoría de cinco años son otra cosa y están en la [#2](gobierno-auditoria.md): aquí los logs operativos se guardan 30 días.

## 1. Qué se mide en cada capa

| Capa | Métricas | Logs | Trazas |
| --- | --- | --- | --- |
| **Ingesta** ([#12](carga-a-ingesta-telemetria.md)) | IoT Core: `PublishIn.Success`, `Connect.AuthError`, `RuleMessageThrottled` y fallos de acción de regla. SQS: edad del mensaje más antiguo y mensajes en la DLQ. Lambda: errores, duración y throttles del normalizador. Propias: lecturas persistidas por minuto y segundos entre `occurred_at` y el commit | Logs de IoT Core en nivel `ERROR`. Logs JSON del normalizador con `event_id`, `FincaID` y resultado | X-Ray en el normalizador y el despachador. IoT Core no propaga trazas, así que se correlaciona por `event_id` |
| **Aplicaciones** | API Gateway: `Count`, `4XXError`, `5XXError` y latencia p95 por ruta. Cognito: inicios de sesión fallidos y desafíos de MFA fallidos | Logs de acceso de API Gateway en JSON | X-Ray activo en API Gateway y en las Lambda que atienden |
| **Base** ([#15](carga-c-saco-y-viaje.md)) | DynamoDB: `ThrottledRequests`, `SystemErrors`, latencia de lectura y escritura, y `ReplicationLatency` de las Global Tables hacia `us-east-2` | Eventos de errores de la API de DynamoDB vía CloudTrail | Segmentos de DynamoDB dentro de las trazas de X-Ray |
| **Tres enlaces WAN** ([#8](carga-d-centro-acopio.md)) | VPN: `TunnelState`, `TunnelDataIn` y `TunnelDataOut` de cada túnel de Cauca, Huila y Tolima | Logs de túnel de Site-to-Site VPN (cambios de estado de IKE y BGP) | No aplica |
| **Objetos de vuelo** ([#14](carga-b-orden-fumigacion.md)) | S3 con filtro por prefijo: `PutRequests`, `BytesUploaded` y `4xxErrors`. Propias: minutos entre el aterrizaje y `VOLADA_REGISTRO_PERSISTIDO` | Eventos de datos de S3 (los mismos de la auditoría) | X-Ray en la función que valida la bitácora |

Las métricas propias las publica cada función con el formato EMF de CloudWatch dentro de su log, sin llamadas extra a la API de métricas.

## 2. Alarmas de degradación

Hay tres destinos, cada uno un topic SNS:

- **`ops-critical`**: SMS y correo a la guardia de plataforma (DevOps). Se atiende de inmediato.
- **`ops`**: correo a plataforma y un ticket en la mesa de ayuda. Se atiende en horario laboral.
- **`campo`**: correo al técnico del acopio del departamento y al agrónomo coordinador. Son avisos que se resuelven en terreno, no en la nube.

| Aviso del enunciado | Regla | Destino |
| --- | --- | --- |
| **Finca sin telemetría más de 24 h** | Una función programada cada hora consulta el índice `last_seen` por finca y publica `FarmsSilent24h`. Alarma si es mayor que 0. A las 12 h publica `FarmsSilent12h` como aviso temprano, según la [#6](conectividad-sin-senal.md). El mensaje lista los `FincaID` | 12 h: `campo`. 24 h: `campo` y `ops` |
| **Nodo sin telemetría más de 24 h** | La misma función, agrupada por `ThingName`, para separar el nodo de cultivo del de secado en una misma finca | `campo` |
| **Alerta de cultivo no entregada** | `AlertsUndelivered`: alertas en `DESPACHADA` o `ACEPTADA_PROVEEDOR` sin `RECIBIDA_DISPOSITIVO` a los 5 minutos de `occurred_at`. Alarma si es mayor que 0 durante 2 periodos de 1 minuto | `ops-critical` |
| **Vuelo sin registro persistido** | `FlightsWithoutLog`: órdenes en `VOLADA_REGISTRO_PENDIENTE` hace más de 24 horas, que es la ventana de sincronización de la cuadrilla. Alarma si es mayor que 0 | `campo` y `ops` |
| **Fumigación sin cierre** | `SprayingsWithoutClosure`: órdenes en `VOLADA_REGISTRO_PERSISTIDO` sin verificación del servicio 4 a los 10 días, el límite de la ventana biológica de la [#13](carga-b-servicio-drones.md). Alarma si es mayor que 0 | `campo` |
| **Invocación fallida que no mutó el estado** | `ApproximateNumberOfMessagesVisible` de la DLQ de cada función de la [#16](carga-e-funciones.md) mayor que 0. Como esas funciones no cambian el expediente al fallar, un mensaje en la DLQ es un caso detenido | `ops-critical` para confirmación del foco; `ops` para las demás |
| Enlace WAN caído | Los dos túneles de un acopio con `TunnelState` en 0 durante 5 minutos | `ops-critical` |
| Enlace WAN degradado | Un solo túnel en 0 durante 15 minutos | `ops` |
| Cola de ingesta atrasada | Edad del mensaje más antiguo de la cola en vivo mayor que 120 s, porque el presupuesto de 300 s de la alerta ya no alcanza | `ops-critical` |
| Réplica atrasada | `ReplicationLatency` mayor que 60 s durante 5 minutos, muy por debajo del RPO de 15 minutos | `ops` |

Las métricas de estado (`FlightsWithoutLog`, `SprayingsWithoutClosure` y `AlertsUndelivered`) salen de índices sobre el estado y la fecha en DynamoDB. Así la función programada consulta solo los casos abiertos y nunca recorre la tabla completa.

## 3. Los dos SLO

### SLO 1: entrega de la alerta de cultivo

- **SLI:** proporción de alertas de cultivo **con señal** cuya recepción en el teléfono llega en menos de 5 minutos.

  `SLI₁ = alertas con señal y (recibida_en − occurred_at) < 300 s / alertas con señal`

- **Alerta con señal:** la que sale de una lectura que llegó a la plataforma en menos de 60 s desde `occurred_at`, o sea, no se drenó desde el buffer de 24 h. Las alertas de lecturas atrasadas se miden aparte, porque el enunciado solo exige 5 minutos cuando hay señal.
- **Recibida:** el estado `RECIBIDA_DISPOSITIVO` de la #12, con el recibo autenticado de la app. Que SNS acepte el mensaje no cuenta como entrega.
- **Objetivo:** 95 % en una ventana móvil de 28 días.
- **Por qué 95 % y no más:** la última milla depende del operador móvil y de que el teléfono tenga la app abierta o reciba el SMS, y nada de eso es de la plataforma. Un objetivo más alto se gastaría en factores que el equipo no controla.

### SLO 2: disponibilidad de la consulta del saco

- **SLI:** proporción de consultas válidas que responden sin error del servidor.

  `SLI₂ = consultas con respuesta 2xx, 404 o 429 / consultas totales`

  Un 404 es un código que no existe y un 429 es el límite de tasa funcionando; ninguno es una caída. Se mide en el borde de la API, no dentro de la función.
- **Sonda sintética:** un canario de CloudWatch Synthetics consulta cada 5 minutos un código testigo desde `us-east-2`. Así la medición no depende de la región que se está midiendo.
- **Objetivo:** 99,9 % mensual, como propone el borrador. Deja un presupuesto de error de 43 minutos al mes, que es compatible con el failover a `us-east-2` de la #15, de menos de 60 s.

### Alarmas por consumo del presupuesto

Cada SLO tiene dos alarmas de tasa de consumo del presupuesto de error, con matemática de métricas de CloudWatch:

- **Rápida:** consumo 14,4 veces la tasa sostenible durante 1 hora, que equivale al 2 % del presupuesto. Va a `ops-critical`.
- **Lenta:** consumo 6 veces la tasa sostenible durante 6 horas. Va a `ops`.

Si el presupuesto del mes se agota, se congelan los cambios de producción que no sean correcciones. Es la misma compuerta del pipeline de la [#26](https://github.com/aromapacifico-platform/planning/issues/26) que se usa en cosecha.

## 4. Tablero operativo

Un tablero de CloudWatch, `aromapacifico-prod-operacion`, organizado en filas que se leen de arriba abajo:

1. **Estado de los SLO:** los dos SLI del periodo, el presupuesto restante y las alarmas activas.
2. **Fincas:** lecturas por hora, fincas sin telemetría a las 12 h y a las 24 h, y lista de `FincaID` afectados. Se filtra por departamento con la etiqueta `AcopioID`.
3. **Alertas de cultivo:** generadas, recibidas y pendientes, y el tiempo por tramo (T1 a T7 de la #12) en p50 y p95.
4. **Acopios:** estado de los dos túneles de Cauca, Huila y Tolima, y su tráfico de entrada y salida.
5. **Drones:** objetos recibidos, vuelos sin registro y fumigaciones sin cierre, filtrables por `DronID`.
6. **Funciones:** invocaciones, errores y mensajes en la DLQ por función.
7. **Base:** throttles, latencia y retraso de la réplica.

Los filtros del tablero son variables de CloudWatch sobre las dimensiones `FincaID`, `DronID` y `AcopioID` que publica cada métrica propia.

## 5. Tablero de costo

El costo se parte con las etiquetas obligatorias de la landing zone de la [#1](gobierno-landing-zone.md), activadas como etiquetas de asignación de costos en la cuenta raíz. Sobre ellas se define una **categoría de costo** en AWS Cost Categories con cinco valores, que se evalúan en este orden:

| Valor | Regla | Qué junta |
| --- | --- | --- |
| **Pruebas** | `Ambiente` es `pruebas` o `desarrollo` | Todo lo que no es producción |
| **Drones** | `DronID` distinto de `NO-APLICA` | Objetos, funciones de inferencia y almacenamiento de misiones |
| **Acopio** | `AcopioID` distinto de `MULTICENTRO` | VPN, tráfico y recursos de cada centro |
| **Fincas** | `FincaID` distinto de `GLOBAL` | Cosas de IoT, mensajes y telemetría por finca |
| **Plataforma compartida** | Lo demás | Red central, seguridad y auditoría |

El orden importa: un recurso de un dron en pruebas cuenta como pruebas, no como dron.

Para tener los dos tableros en el mismo lugar, una función diaria consulta Cost Explorer agrupando por esa categoría y por `AcopioID`, y publica el costo del día como métrica de CloudWatch. El tablero `aromapacifico-prod-costo` muestra:
- El costo diario y del mes por categoría.
- El costo por acopio.
- Las 10 fincas más caras del mes.
- La proyección del mes contra los presupuestos de la #1.

El detalle por finca o por dron se abre en Cost Explorer con el mismo filtro de etiqueta.

La consulta a Cost Explorer cuesta USD 0,01 por llamada. Con 3 llamadas al día son unos USD 0,90 al mes, más unas 20 métricas propias a USD 0,30 cada una.

## 6. Verificación de los criterios de la #18

| Criterio | Dónde se cumple |
| --- | --- |
| Dos SLO con SLI medible, objetivo y ventana | Sección 3 |
| Cada alarma de degradación del enunciado tiene su regla y su destino | Sección 2: las seis primeras filas son las del enunciado |
| El tablero de costo se parte por fincas, drones, acopio y pruebas | Sección 5 |
