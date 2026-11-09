# Auditoría de los cuatro eventos del caso

## Qué pide el enunciado

La Federación tiene que poder reconstruir cualquier reclamo durante los cinco años de retención. Para eso el enunciado nombra cuatro eventos que deben quedar auditados:

1. Quién leyó un saco.
2. Quién cambió un umbral.
3. Qué telemetría se publicó.
4. Qué objeto de vuelo se entregó.

Este documento dice, para cada uno, qué servicio lo registra, qué campos guarda, en qué cuenta queda, cómo se protege contra borrado y cuánto cuesta guardarlo. Se apoya en la landing zone de la [#1](gobierno-landing-zone.md): la cuenta `AromaPacifico-Security`, el bucket `aromapacifico-audit-logs-*` y la SCP `protect-audit-and-security`.

## 1. Dónde vive la auditoría

Todo termina en un solo bucket de la cuenta `AromaPacifico-Security`: **`aromapacifico-audit-logs-security`**, en `us-east-1`.

- **Object Lock en modo Compliance con retención de 5 años.** En ese modo nadie puede borrar ni sobrescribir un objeto antes de que venza su retención, ni siquiera la cuenta raíz de la organización.
- **Versionado activo**, que Object Lock exige.
- **Cifrado SSE-KMS** con la llave `alias/aromapacifico-audit-key` de la cuenta de seguridad, definida en la [#5](seguridad-datos-saco.md). Las cuentas de trabajo pueden cifrar con ella, pero no descifrar.
- **Bloqueo de acceso público** y TLS obligatorio.
- **Prefijos por evento:** `cloudtrail/`, `api-access/`, `iot-telemetry/` y `app-audit/`.

Las cuentas de producción no escriben con sus propias identidades. Escriben **servicios de AWS** en su nombre: CloudTrail con su principal de servicio, y Amazon Data Firehose con un rol que solo tiene `s3:PutObject` sobre su prefijo. La política del bucket solo admite esos principales, con la condición `aws:SourceOrgID` de la organización.

## 2. Los cuatro eventos

| Evento | Origen del registro | Quién | Cuándo | Qué | Camino hasta la cuenta de seguridad | Retención |
| --- | --- | --- | --- | --- | --- | --- |
| **Lectura de un saco** | Logs de acceso de API Gateway de la consulta del saco y de las apps | Comprador anónimo: IP de origen y agente. Usuario de app: `sub` de Cognito y perfil | `requestTime` en UTC | Código del saco consultado, método, ruta, estado HTTP, `requestId` | Logs de acceso de API Gateway enviados directo a Firehose → prefijo `api-access/` | 5 años |
| **Cambio de un umbral** | Registro de auditoría de la aplicación (transacción de la [#12](carga-a-ingesta-telemetria.md)) y eventos de datos de CloudTrail sobre la tabla `thresholds` | `sub` de Cognito del funcionario de la Federación (la app) y rol que escribió (CloudTrail) | Fecha UTC de la transacción | Versión anterior y nueva, motivo, `request_id` y puntero activo | Streams de la tabla → Firehose → `app-audit/`. CloudTrail de la organización → `cloudtrail/` | 5 años |
| **Publicación de telemetría** | Segunda acción de la regla de IoT Core sobre cada mensaje aceptado | `clientid()` y `principal()` del certificado X.509 del nodo | `timestamp()` del broker y `occurred_at` del nodo | Tema, `FincaID`, valores medidos y secuencia | Regla de IoT → Firehose → `iot-telemetry/` | 5 años |
| **Entrega de un objeto de vuelo** | Eventos de datos de CloudTrail `PutObject` sobre el bucket de objetos de dron | Rol de la cuadrilla y `sub` de Cognito del operador, en la etiqueta de sesión | `eventTime` en UTC | Llave del objeto, `versionId`, tamaño y checksum SHA-256 | CloudTrail de la organización → `cloudtrail/` | 5 años |

### Por qué se combinan dos fuentes en el cambio de umbral

El cambio lo hace una persona desde la app, pero la escritura en DynamoDB la ejecuta el rol de la función. Si solo se mirara CloudTrail, el registro diría "lo cambió la Lambda". Por eso la propia transacción de la #12 guarda el `sub` de Cognito de quien hizo el cambio, y CloudTrail queda como prueba independiente de que esa escritura ocurrió. El cambio solo se da por auditado cuando las dos fuentes coinciden por `request_id`.

### Por qué la telemetría no usa los logs de IoT Core

Los logs de IoT Core en nivel `INFO` registran cada publicación, pero van a CloudWatch Logs, que cobra por GB ingerido y no es inmutable. La segunda acción de la regla escribe directamente en Firehose el mensaje que la plataforma aceptó, con la identidad del certificado. Es más barato y ese registro es justo el que sirve en un reclamo: lo que llegó y quién lo firmó. Los logs de IoT Core quedan en nivel `ERROR`, para diagnóstico.

### Lectura del saco sin datos personales de más

En la consulta pública la única pista del lector es la IP. Se guarda completa porque es la evidencia de un abuso o de un reclamo, pero no sale de la cuenta de seguridad. El perfil de auditor de la #1 solo la consulta por incidente.

## 3. Nadie de producción puede borrarlo

Hay tres barreras independientes, para que fallar una no alcance:

1. **Object Lock en modo Compliance.** El objeto no se puede borrar ni acortar su retención durante 5 años, sin importar los permisos de quien lo intente.
2. **Otra cuenta.** El bucket vive en `AromaPacifico-Security`. Las identidades de `AromaPacifico-Prod` no tienen permisos sobre él, y los servicios que escriben solo pueden poner objetos.
3. **SCP `protect-audit-and-security`.** Niega en toda la organización `cloudtrail:StopLogging`, `cloudtrail:DeleteTrail` y `cloudtrail:UpdateTrail`, y las acciones de borrado y de cambio de configuración sobre `aromapacifico-audit-logs-*`. Esta historia le agrega `s3:PutBucketObjectLockConfiguration`, `s3:PutBucketPolicy` y `firehose:DeleteDeliveryStream` sobre los streams de auditoría.

Para auditar al auditor, cualquier lectura del bucket queda a su vez en CloudTrail.

## 4. Cuánto cuesta guardar cinco años

### Volumen

| Fuente | Registros al día en cosecha | Tamaño aprox. por registro | Por año |
| --- | ---: | ---: | ---: |
| Telemetría aceptada (#12) | 3.600 lecturas agronómicas | 0,5 KB | 0,7 GB |
| Accesos a la API: posiciones, eventos del saco y consultas | ~12.000 | 1 KB | 4,4 GB |
| CloudTrail de la organización: eventos de gestión de las 6 cuentas | ~50.000 | 2 KB | 36,5 GB |
| CloudTrail de datos: objetos de dron y tabla de umbrales | ~1.100 | 2 KB | 0,8 GB |
| **Total** | | | **~42 GB al año** |

Se toma el volumen de cosecha todo el año, para no quedarse corto. Al quinto año el bucket guarda unos **210 GB**.

### Clase de almacenamiento

Una regla de ciclo de vida mueve los objetos a **S3 Glacier Deep Archive a los 90 días**. Object Lock se conserva al cambiar de clase. Los primeros 90 días quedan en S3 Standard, porque es cuando más se consulta un reclamo reciente. Lo más viejo se recupera en 12 a 48 horas, que es aceptable para reconstruir un reclamo de años atrás.

### Costo

Precios de lista de `us-east-1`. Se verifican contra la página de precios al consolidar los costos de la plataforma en la [#29](https://github.com/aromapacifico-platform/planning/issues/29).

| Concepto | Precio | Cálculo | Costo |
| --- | --- | --- | ---: |
| S3 Standard, últimos 90 días | USD 0,023 por GB-mes | ~10,5 GB | USD 0,24 al mes |
| Glacier Deep Archive, quinto año | USD 0,00099 por GB-mes | ~200 GB | USD 0,20 al mes |
| Transiciones a Deep Archive | USD 0,05 por 1.000 objetos | ~2.600 objetos al día: tres streams de Firehose que entregan cada 5 minutos y el trail de las seis cuentas | USD 47 al año |
| Firehose | USD 0,029 por GB | ~6 GB al año | USD 0,18 al año |
| Eventos de datos de CloudTrail | USD 0,10 por 100.000 eventos | ~400.000 al año | USD 0,40 al año |
| Primer trail de gestión de la organización | Sin costo | — | USD 0 |

**Total: unos USD 53 al año, o unos USD 265 en los cinco años.** Lo que más pesa son las transiciones, porque Firehose y CloudTrail generan muchos objetos pequeños. Si hiciera falta bajar ese costo, se sube el búfer de Firehose a 15 minutos, con lo que sus objetos caen a la tercera parte. Además, S3 no mueve por defecto los objetos de menos de 128 KB, y esos se quedan en Standard a un costo despreciable. Todo cabe holgado en los USD 50 al mes que la #1 le asigna a la cuenta de seguridad.

## 5. Verificación de los criterios de la #2

| Criterio | Dónde se cumple |
| --- | --- |
| Tabla con los cuatro eventos: origen, quién, cuándo, qué, cuenta destino y retención | Sección 2 |
| El registro vive en la cuenta de seguridad y ninguna identidad de producción puede borrarlo | Secciones 1 y 3 |
| Cuánto cuesta guardar cinco años y en qué clase de almacenamiento | Sección 4 |
