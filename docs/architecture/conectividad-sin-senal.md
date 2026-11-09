# Conectividad de los cinco puntos y operación sin señal

**Historia:** #6 · **Responsable:** Juan Ocampo (`juandavid175`) · **Fecha:** 6 de noviembre de 2026.  
**Estado:** propuesta documental para revisión; no representa infraestructura desplegada ni pruebas de campo.  
**Base:** `planning/main`, commit `4c6fa27a31a5ac5c38c0da5711e36936024ba2cd`.

## 1. Alcance y decisiones que se conservan

Este caso académico conecta 200 fincas, 60 transportadores y tres acopios de Cauca, Huila y Tolima hasta la entrega del saco de 60 kg en Buenaventura. La presente sección forma parte del cuerpo de la arquitectura y debe incorporarse al consolidado de #19, junto con su diagrama; no debe relegarse a un anexo.

Se conservan AWS en `us-east-1`, IoT Core para telemetría celular, API Gateway para aplicaciones, DynamoDB para registros y S3 para objetos; son decisiones de [gobierno](gobierno-landing-zone.md), [direccionamiento](red-direccionamiento-nube.md) y [operación de drones](carga-b-orden-fumigacion.md). No se modifican sus CIDR, la topología con Transit Gateway ni la autorización humana de fumigación.

La decisión nueva de #6 es un canal **Iridium SBD para telemetría de las fincas sin cobertura celular**, con RockBLOCK 9603 como referencia técnica y comercial, no como compra confirmada. Se agrega un adaptador de recepción satelital al diseño. Bluetooth no se incorpora como requisito ni como canal de alerta en esta historia.

## 2. Matriz de conectividad por punto

| Punto y datos | Red de salida y protocolo | Buffer local persistente | Comportamiento sin señal y recuperación |
|---|---|---|---|
| **Finca y beneficiadero.** Cultivo cada 4 h; secado cada hora mientras esté activo. | Con cobertura comprobada: LTE-M/NB-IoT, MQTT sobre TLS hacia IoT Core, TCP 8883. Sin cobertura celular permanente: SBD mediante satélite; el proveedor entrega por HTTPS/TCP 443 al adaptador de AWS. | Cola en flash del nodo, escrita antes de transmitir; antigüedad máxima de 24 h. Cultivo y secado comparten un equipo de comunicaciones solo si la instalación permite conectarlos sin añadir enlaces no diseñados. | Si la ruta asignada falla, conserva cada lectura, reintenta y drena sin esperar al siguiente muestreo. Solo retira registros confirmados por la plataforma. El canal satelital funciona sin traslados periódicos ni radiobase terrestre nueva. La excepción por agotamiento de 24 h se define en la sección 5. |
| **Dron.** Misión, fotos, polígonos y bitácora. | Misión descargada por HTTPS antes de salir. Transferencia dron–estación por USB o enlace local admitido por el equipo. Estación a S3 por HTTPS/TCP 443 con URL prefirmada, mediante 4G o wifi autorizado del acopio. | Memoria no volátil de la aeronave y copia en la estación de campo. El diseño integrado fija hasta 24 h para sincronización local; la capacidad real se dimensiona por tamaño de misión, no por número de lecturas de sensor. | La caída de internet no impide ejecutar una misión ya autorizada y precargada. La cuadrilla sincroniza al retornar a una zona con conexión, dentro de su operación de vuelo. Renueva las URLs vencidas. Sin bitácora persistida y evidencia exigida, el caso no pasa a cerrado. |
| **Transportador.** Posición cada 5 min y eventos de custodia del saco. | Aplicación con 4G/LTE o wifi autorizado del acopio; HTTPS/TCP 443 hacia API Gateway y autenticación de aplicación mediante Cognito. | SQLite cifrada en el teléfono; cola de salida independiente de la memoria temporal de la aplicación. | Sigue capturando posiciones si hay ubicación disponible. Si falta GNSS, registra el fallo de ubicación; no inventa coordenadas. Al recuperar datos en cabecera, vía principal o acopio, envía lotes acotados, reintenta los fallidos y conserva los pendientes sin confirmar. |
| **Centro de acopio.** Recepción, aceptación/rechazo, despacho y códigos. | WLAN segmentada y LAN; WAN de 100 Mbps simétricos compartidos. Tráfico privado por VPN IPsec hasta el Transit Gateway aprobado; objetos a S3 por HTTPS mediante el acceso privado diseñado. IKE UDP 500/4500 y ESP cuando corresponda a la configuración del túnel. | Cola cifrada de operaciones en los puestos de logística, como propuesta para concretar en #8. Los trabajos de impresión permanecen en el spooler local. | La LAN y el registro local pueden continuar si falla la WAN y hay energía. Las transacciones quedan pendientes; el usuario no ve una confirmación cloud ficticia. Reconexión: sincronizar con deduplicación y tratar conflictos. Si cae el puesto o su energía, no se promete continuidad de captura sin el respaldo que defina #8. |
| **Buenaventura.** Entrega aceptada o rechazada del saco. | Aplicación del transportador o del responsable autorizado, teléfono con 4G/LTE; HTTPS/TCP 443 hacia la API. No se presupone wifi del puerto. | Cola cifrada del teléfono con el evento de entrega y sus evidencias, si aplican. | Registra el evento con hora original y estado pendiente; sincroniza cuando vuelve la conexión. Hasta recibir confirmación, se distingue entrega registrada localmente de entrega persistida en plataforma. No se instala LAN, gateway ni otro equipo de la Federación; tampoco se sigue al barco. |

**Ninguna ruta usa ni necesita respaldo 2G o 3G.** La disponibilidad de LTE-M/NB-IoT se verifica por operador y sitio: una cobertura 4G en el mapa no demuestra que ambos servicios IoT estén habilitados. La finca que no supera esa validación entra en el perfil satelital.

![Conectividad de los cinco puntos](diagrams/conectividad-sin-senal.svg)

Fuente editable: [Draw.io](diagrams/conectividad-sin-senal.drawio). El SVG se puede visualizar directamente en el repositorio.

## 3. Finca sin cobertura: camino satelital completo

1. El nodo guarda la lectura, su identificador, hora UTC y secuencia. La codifica en un mensaje compacto y protege el contenido antes de entregarlo al módem.
2. El módem transmite por **SBD**, no por MQTT ni por una sesión TLS directa a AWS. Se propone un sobre cifrado y autenticado por dispositivo (AEAD), con contador persistente para impedir repetición y reutilización de nonce. La provisión y custodia de claves se coordinan con #4/#5/#11; no se generan secretos dentro de Terraform ni se escriben en su estado.
3. El proveedor llama a un endpoint HTTPS del adaptador satelital. Se configura validación del certificado TLS y se rechazan modos inseguros. El adaptador valida la firma del proveedor, la identidad activa del nodo y la autenticidad del mensaje. El IMEI no sustituye la identidad criptográfica del nodo.
4. El adaptador escribe el mensaje validado en una cola duradera antes de responder HTTP 200 al proveedor. La respuesta debe ser rápida: el proveedor documenta un límite de tres segundos [S3]. Si la cola falla, devuelve error y permite el reintento del proveedor. La infraestructura de este adaptador queda diseñada; no se añade automáticamente a las 100 horas de IaC.
5. Un consumidor normaliza el mensaje y lo publica, con un rol restringido, en el camino de ingesta definido para #12. Los temas y la regla exacta se acuerdan allí; se conserva el procesamiento de umbrales y el almacén existentes, sin crear una segunda lógica agronómica.
6. Solo después de persistir la lectura, la plataforma genera un ACK de aplicación que identifica los registros aceptados. Puede agrupar confirmaciones por secuencia. Lo devuelve mediante el servicio de mensajes hacia el módem [S4]. El nodo conserva los registros si no recibe ese ACK. El éxito de la sesión satelital, el HTTP 200 del webhook y el PUBACK MQTT no equivalen por sí solos a lectura persistida.

El equipo requiere antena con vista al cielo, alimentación adecuada a los picos del módem y protección contra humedad. La placa de referencia no es impermeable: su integración y balance energético deben validarse en #11. Una finca no se declara habilitada solo por la cobertura global del proveedor: se prueba la instalación, el envío, el retorno del ACK y la recuperación tras un corte. La disponibilidad comercial y el suministro para Colombia siguen sujetos a cotización.

Los objetos de las fincas sin cobertura se separan por tamaño: fotos, mapas y bitácoras del dron viajan con la estación de la cuadrilla y se cargan al volver de cada misión; no por SBD ni mediante una visita semanal de recolección. Los eventos pequeños del saco se guardan en la aplicación y se sincronizan en cabecera o vía principal, conforme al supuesto del caso. Si se exigieran objetos pesados automáticos desde una finca permanentemente aislada, este canal de mensajes cortos no los resolvería y habría que ampliar el diseño.

## 4. Costo de referencia de la excepción satelital

Fuentes consultadas el **6 de noviembre de 2026**, USD, sin conversión a COP. El costo se aplica a `N_sat`, número de fincas sin cobertura aún no determinado; no se multiplica automáticamente por las 200 fincas.

### 4.1 Inversión incremental por finca

| Concepto | USD | Naturaleza |
|---|---:|---|
| Módulo RockBLOCK 9603 con antena integrada | 302 | Precio publicado [S1]; no garantiza existencias ni entrega. |
| Protección, adaptación eléctrica y montaje | 50–100 | Reserva de ingeniería, no cotización. |
| Incremento de batería/panel por comunicaciones | 50–100 | Reserva de ingeniería; #11 debe justificarla con balance energético. |
| Instalación y prueba del enlace | 30–80 | Reserva de ingeniería, no cotización. |
| **Subtotal incremental estimado** | **432–582** | No incluye sensores, nodo base, impuestos, envío ni importación. |

### 4.2 Operación mensual calculada

Presupuesto de diseño: **200 bytes por envío completo**, incluida la protección del mensaje, y **50 bytes de retorno por lectura** para ACK y control. Es un supuesto de dimensionamiento por verificar con el formato definitivo; no una medición del firmware. Mes de 30 días y un terminal por finca.

| Perfil | Lecturas/día | Datos de salida/mes | Retorno/mes | Total estimado |
|---|---:|---:|---:|---:|
| Cultivo, sin secado activo | 6 | 36.000 bytes | 9.000 bytes | **45.000 bytes** |
| Cultivo y secado activo | 6 + 24 = 30 | 180.000 bytes | 45.000 bytes | **225.000 bytes** |

Para tráfico recurrente, [S2] publica contratos representativos de 12 meses: plan de 25.000 bytes a USD 36,75/mes, excedente USD 1,68/1.000 bytes; y plan de 250.000 bytes a USD 147/mes. Con esos valores:

- Sin secado: `36,75 + (45.000 − 25.000) / 1.000 × 1,68 = USD 70,35/mes`.
- Con secado: `225.000 < 250.000`, por lo que la referencia es **USD 147/mes** antes de extras. Quedan 25.000 bytes de margen; no es una garantía frente a cualquier número de reintentos.
- Activación publicada: USD 31,50 o USD 26,25, respectivamente. Las consultas vacías cuestan USD 0,02 cada una; se suman al consumo según la operación real. No se añade la línea de USD 17 del prepago a estos contratos.

Los reenvíos, mensajes adicionales, servicios del integrador y costos cloud del adaptador requieren presupuesto separado. La selección contractual debe considerar todo el año; no se supone que cambiar de plan sea gratis o inmediato. Si un mismo terminal tendrá secado activo durante el año y no hay cambio de plan pactado, se presupuesta **USD 147 por mes durante el contrato**, incluso fuera de cosecha. USD 70,35 es un escenario alternativo para un perfil de solo cultivo, no un ahorro estacional automático. Para el consolidado se usará `N_sat × tarifa_contratada`, más los extras reales.

**Justificación:** se utiliza satélite solo en las fincas que no tienen alternativa celular validada, evita construir una radiobase y elimina la recolección periódica de lecturas. Se aprovechan el nodo y la instalación inicial, y los archivos grandes usan la logística de vuelo existente. Esto justifica su función, pero **no demuestra por sí solo una cuota moderada para el caficultor**: #28/#29 deben validar financiación o tarifa de volumen. La propuesta queda económicamente condicionada; no se declara que el satélite sea la opción más barata del mercado ni que su compra esté aprobada.

## 5. Buffer, reintentos y límite de 24 horas

Cada lectura se escribe de forma atómica antes de intentar la red y sobrevive al reinicio. Al recuperar enlace se drena la cola sin esperar la próxima lectura programada. Se priorizan los registros cercanos a vencer; la prioridad y el envío de alertas se coordinan con #12, cuyos umbrales no quedan fijos en el dispositivo.

Se propone reintentar a los 1, 5 y 15 minutos tras el fallo, y después cada 15 minutos con variación aleatoria. La cadencia es un parámetro de diseño que #11 debe contrastar con energía y tarifa; no se acredita como rendimiento medido. Los temporizadores de transporte y de ACK son distintos. Un ACK perdido puede provocar reenvío legítimo: la plataforma deduplica por identificador y vuelve a confirmar lo ya persistido.

Una finca con ambos flujos activos produce **30 registros diarios**, no 24. Con una reserva de 256 bytes por registro persistido: `30 × 256 = 7.680 bytes`, antes de índices y journaling. Se propone reservar al menos 64 KiB para la cola y metadatos; la capacidad no autoriza retener lecturas activas por más de 24 h. La cifra de 180 bytes del documento de red es una estimación de carga útil, no el tamaño total del registro en flash.

El objetivo operativo es entregar antes de vencer. Se registra aviso local tras el fallo y, si el nodo puede comunicarlo, alarma por antigüedad a las 12 h y escalamiento a las 20 h. Desde AWS se vigila ausencia de telemetría sin depender de que el nodo desconectado logre avisar. Estos umbrales anticipados son supuestos nuevos para #18.

Si una interrupción de todas las rutas disponibles o una avería dura 24 h, **no puede garantizarse simultáneamente cero pérdida y un buffer de retención máxima de 24 h**. Al vencer un registro sin ACK se contabiliza como no confirmado, se retira su carga útil de la cola activa y se conserva únicamente metadato de incidente (identificador, hora, motivo y contador). El metadato no contiene la lectura. Al reconectar se concilia con la plataforma: un ACK perdido puede ocultar una escritura exitosa; solo se declara pérdida si la lectura tampoco quedó persistida. No se registra un ACK ficticio ni se llama éxito a la expiración. Un corte que alcance ese límite es un incumplimiento que se investiga, no el modo normal de operación.

La instalación solo se acepta si demuestra una ruta autónoma de salida dentro de la ventana. No se usa la llegada eventual del caficultor a cabecera como única solución para la telemetría continua de una finca permanentemente aislada.

## 6. Evento persistido en el teléfono del transportador

El evento patrón es `posicion_registrada`. Se crea cada cinco minutos durante el viaje, aun sin datos móviles. En una jornada de diez horas son 120 posiciones por transportador y 7.200 entre los 60 del piloto, conforme al caso.

| Campo | Uso |
|---|---|
| `event_id` | Identificador único creado offline; clave de idempotencia. |
| `event_type`, `schema_version` | Tipo del evento y versión del contrato. |
| `trip_id`, `actor_id`, `device_id` | Viaje y responsable autenticado; dispositivo de origen. |
| `occurred_at`, `sequence` | Hora UTC original y secuencia local persistente por viaje. |
| `latitude`, `longitude`, `accuracy_m`, `location_status` | Ubicación real y precisión; nulos y motivo si no hay posición disponible. |
| `sync_status`, `attempt_count` | Estado local y control de reintentos; no alteran la hora del hecho. |

Los sacos se relacionan con el viaje, sin repetir toda la lista en cada posición. Entrega de custodia, recepción, salida y entrega en puerto son eventos separados con identificador de saco, responsable y hora. El detalle del ciclo de vida pertenece a #15.

**Sincronización:** guardar en transacción local → detectar conexión utilizable → renovar autenticación si procede → enviar lote acotado por HTTPS → recibir resultado por `event_id` → marcar como sincronizados solo los confirmados. Ante timeout o respuesta parcial se reenvían los pendientes con el mismo identificador. El servidor aplica una escritura idempotente y conserva `occurred_at` separado de `received_at`. Cambiar de red o reiniciar la aplicación no vacía la cola.

Ejemplo: posiciones de 10:00, 10:05 y 10:10 guardadas sin datos llegan a las 10:14. Se almacenan con sus horas originales. Si la respuesta se pierde y llegan de nuevo, siguen siendo tres posiciones, no seis. Los eventos de custodia se sincronizan con prioridad sobre la posición y se ordenan por viaje y secuencia; los conflictos de estado requieren resolución explícita, no sobrescritura silenciosa.

El teléfono conserva pendientes hasta confirmación; el límite de 24 h del nodo de finca no se impone automáticamente al teléfono. Se dimensiona almacenamiento, se alerta antes de llenarlo y no se borran eventos de custodia para hacer espacio a posiciones. El RPO cloud de 15 minutos del saco no convierte un evento aún offline en un evento respaldado; #15 debe distinguir ambos casos.

## 7. Entrega de alertas: límite de esta historia

Se conserva la evaluación de umbrales en plataforma y el despacho mediante SNS planteados en #7. **#12 debe concretar el canal final y su confirmación de recepción**, además del tiempo de cada tramo; #18 define el SLI/SLO. No se añade Bluetooth, un teléfono satelital ni un modelo de umbrales distinto para cerrar artificialmente este requisito.

Con ruta de entrega disponible de extremo a extremo, el objetivo es menos de cinco minutos desde `occurred_at` hasta la recepción en el canal del caficultor. La ausencia de señal celular no implica ausencia de ruta de subida cuando SBD funciona, pero el ACK al módem no acredita entrega de una alerta a la persona. La recepción de la lectura, el despacho y la entrega de la alerta se miden por separado.

Sin ruta hacia el destinatario, la alerta permanece pendiente y debe emitirse al recuperar la ruta, dentro de la ventana de 24 h del caso. Si el destinatario permanece inaccesible más allá de esa ventana, se registra incumplimiento; el diseño de conectividad no elimina esa limitación. No se presenta la latencia satelital comercial como SLA garantizado de cinco minutos. La validación integral corresponde a #12/#18 y no está ejecutada en esta entrega.

## 8. Fronteras con las otras historias e IaC

| Historia | Insumo que recibe de #6 |
|---|---|
| #8 Acopio | Patrón de conexión, uso de VLAN Logística para cuadrillas, necesidad de cola local, WAN y sincronización. Define equipos, capacidad y respaldo eléctrico. |
| #9 Firewall | MQTT/TLS 8883, HTTPS 443 y túnel IPsec. Distingue endpoints administrados públicos de interfaces en VPC; no abre un puerto de subred suponiendo que IoT Core vive en ella. |
| #11 Nodo | Perfil celular/satelital, retención, mensajes, protección ambiental y reintentos para dimensionar energía y BOM. |
| #12 Ingesta | Sobre normalizado, deduplicación, ACK de persistencia y adaptación satelital. Define temas exactos, procesamiento y canal final de alertas. |
| #15 Saco | Eventos offline de custodia/entrega, secuencia y tratamiento de conflictos. |
| #18 Observabilidad | Edad del pendiente, lecturas vencidas, eventos sin ACK, ruta de alerta y fallos de sincronización. |
| #22 Red IaC | Conserva CIDR, endpoints y conexión de acopio mediante Transit Gateway de #7. #6 no bloquea el desarrollo de ese módulo. |

El adaptador satelital, el firmware, las aplicaciones y la cola del puesto no se presentan como implementados. Se describen sus interfaces. Añadir infraestructura del adaptador al patrón de la Épica 6 requiere ajustar el plan de horas; no se aumenta el alcance por omisión.

## 9. Verificación documental y pruebas por ejecutar

| Criterio de aceptación de #6 | Evidencia en esta entrega |
|---|---|
| Cinco puntos con protocolo, buffer y operación sin señal | Matriz de sección 2 y diagrama de cinco carriles. |
| Fincas sin cobertura, sin radiobase nueva ni visita semanal, con costo | Camino satelital de sección 3 y estimación explícita de sección 4. Viabilidad económica y comercial pendientes de validación. |
| Evento offline del transportador y carga posterior | Contrato y secuencia de sincronización de sección 6. |
| Ninguna pieza depende de 2G/3G | Exclusión expresa en sección 2 y perfiles dibujados. |

Comprobaciones futuras, no resultados de pruebas ejecutadas: reiniciar con pendientes y recuperar la cola; perder la respuesta y demostrar deduplicación; verificar envío y ACK satelital con la antena instalada; probar un vencimiento de 24 h y su alarma; cortar la WAN del acopio; guardar una entrega en puerto offline y sincronizarla; demostrar entrega de alerta con tiempos por tramo en #12. La aceptación documental no equivale a aceptación de campo.

## 10. Fuentes

- **Internas, base integrada:** [decisiones del senior](../governance-and-decisions/briefing-inicial-juniors.md), [red y rutas de datos](red-direccionamiento-nube.md), [servicio de drones](carga-b-servicio-drones.md), [orden y sincronización](carga-b-orden-fumigacion.md), [enunciado](../case-study/enunciado-original.md) e [historia #6](https://github.com/aromapacifico-platform/planning/issues/6).
- **[S1] Ground Control, RockBLOCK 9603:** [equipo, precio y condiciones físicas](https://store.groundcontrol.com/products/rockblock-9603).
- **[S2] Ground Control, Iridium SBD:** [planes contractuales y prepago](https://www.groundcontrol.com/products/iridium/short-burst-data-range/short-burst-data-service-plans/).
- **[S3] Ground Control:** [recepción mediante webhook y reintentos](https://docs.groundcontrol.com/iot/rockblock/web-services/receiving-mo-message).
- **[S4] Ground Control:** [mensajes hacia el dispositivo](https://docs.groundcontrol.com/iot/rockblock/web-services/sending-mt-message) y [avisos de mensajes pendientes](https://docs.groundcontrol.com/iot/rockblock/user-manual/ring-alerts).

Los tamaños, temporizadores y reservas de costo que no provienen del enunciado o de una cotización están identificados como propuestas y se registran en [supuestos](../cross-cutting/assumptions-log.md).
