# Costo de la plataforma en mes normal y en mes de cosecha

## Qué responde este documento

Cuánto cuesta al mes la plataforma en la nube en un mes normal y en uno de cosecha:
- Ingesta, base, almacenamiento con 5 años de retención, funciones, inferencia, red, VPN de los acopios y observabilidad.
- Los ambientes de pruebas y desarrollo.
- Las invocaciones de funciones en cosecha, calculadas aparte.
- El costo partido por las etiquetas de la landing zone.

No incluye el hardware de las fincas ni su conectividad celular o satelital ([#28](costo-hardware-finca.md)), ni el servicio de drones ([#30](costo-campana-drones.md)).

**Precios:** lista oficial de AWS en `us-east-1`, consultada el 9 de noviembre de 2026. Se toman de las páginas de precios de cada servicio y de la [calculadora de AWS](https://calculator.aws/). No se aplican capas gratuitas, salvo donde se indica, para no quedarse corto. **Tasa de cambio:** TRM de COP 3.237,83.

## 1. De qué cifras del caso sale cada volumen

| Volumen | Mes de cosecha | Mes normal | Origen |
| --- | ---: | ---: | --- |
| Lecturas agronómicas | 108.000 | 36.000 | Caso: 200 fincas × 6 lecturas de cultivo + 100 fincas × 24 de secado al día. Fuera de cosecha no hay secado |
| Posiciones del transportador | 216.000 | 54.000 | Caso: 60 transportadores × 12 por hora × 10 horas al día. Fuera de cosecha se supone el 25 % |
| Sacos recibidos | 31.200 | 3.120 | Caso: hasta 400 sacos al día por acopio × 3 acopios × 26 días. Fuera de cosecha se supone el 10 % |
| Eventos del saco | 187.200 | 18.720 | 6 eventos por saco, de la [#15](../architecture/carga-c-saco-y-viaje.md) |
| Consultas públicas | 129.600 | 43.200 | El caso da picos de 30 por minuto. Se supone un promedio de 3 por minuto en cosecha y 1 fuera |
| Fotos a inferencia | 150 | 17 | Mes pico de la [#17](../architecture/carga-e-inferencia-administrada.md) y mes base de la #13 |
| Alertas al caficultor | 1.000 | 400 | Supuesto: unas 5 alertas por finca al mes en cosecha y 2 fuera |

## 2. Costo mensual por servicio

| Línea | Precio de lista | Normal (USD) | Cosecha (USD) | Sale de |
| --- | --- | ---: | ---: | --- |
| **Ingesta** | | | | |
| IoT Core | USD 0,08 por millón de minutos de conexión; USD 1 por millón de mensajes; USD 0,15 por millón de reglas y por acción | 0,80 | 0,98 | 206 dispositivos; cada lectura y su ACK |
| SQS | USD 0,40 por millón de solicitudes | 0,05 | 0,14 | Lecturas y posiciones |
| Lambda | Ver sección 3 | 0,16 | 0,66 | Sección 3 |
| API Gateway REST | USD 3,50 por millón de solicitudes | 0,25 | 0,87 | Posiciones en lotes de 20 y eventos del saco |
| **Base** | | | | |
| DynamoDB On-Demand | USD 0,625 por millón de escrituras; USD 0,125 por millón de lecturas; réplica a USD 0,625 por millón; PITR a USD 0,20 por GB | 2,19 | 2,94 | Lecturas con índice y outbox; eventos con su proyección y su réplica en `us-east-2` |
| **Almacenamiento con 5 años de retención** | | | | |
| S3 de objetos de dron, más su réplica en `us-east-2` con RTC | Standard USD 0,023; IA USD 0,0125; Deep Archive USD 0,00099 por GB; RTC USD 0,015 por GB | 22,70 | 26,55 | 1,6 TB al año de la #30, replicados por la #15 |
| Auditoría de los cuatro eventos | — | 4,42 | 4,42 | USD 53 al año de la [#2](../architecture/gobierno-auditoria.md) |
| KMS | USD 1 por llave al mes; USD 0,03 por 10.000 solicitudes | 10,00 | 10,00 | 9 llaves de la #5 y del estado |
| **Inferencia** | | | | |
| Rekognition y Bedrock | USD 3,11 por cada 1.000 imágenes | 0,05 | 0,47 | Escenario conservador de la #17 |
| **Consulta pública** | | | | |
| ALB en `us-east-1` y en `us-east-2` | USD 0,0225 por hora y USD 0,008 por LCU-hora | 44,53 | 44,53 | Consolidación de la #19 |
| CloudFront | Dentro del primer TB y los primeros 10 millones de solicitudes gratuitos | 0,00 | 0,00 | 129.600 consultas |
| WAF | USD 5 por ACL, USD 1 por regla y USD 0,60 por millón de solicitudes | 8,03 | 8,08 | 1 ACL con 3 reglas |
| Route 53 | USD 0,50 por zona; USD 0,50 por health check | 1,50 | 1,50 | Failover de la #19 |
| **Red y VPN de los acopios** | | | | |
| Transit Gateway | USD 0,05 por attachment-hora; USD 0,02 por GB | 182,80 | 183,50 | 2 VPC y 3 VPN, de la #7 |
| VPN sitio a sitio | USD 0,05 por conexión-hora | 109,50 | 109,50 | 3 acopios |
| Endpoints de interfaz | USD 0,01 por hora por zona | 87,65 | 87,65 | KMS, Logs, execute-api, S3, Rekognition y Bedrock en 2 zonas |
| Route 53 Resolver | USD 0,125 por ENI-hora | 365,00 | 365,00 | Entrada y salida con 2 ENI cada uno, de la #7 |
| Network Firewall | USD 0,395 por endpoint-hora; USD 0,065 por GB | 577,68 | 579,95 | 2 zonas en la cuenta de red, de la #1 |
| **Notificación e identidad** | | | | |
| SNS | SMS a unos USD 0,035 cada uno; push casi gratis | 14,00 | 35,00 | Alertas de la sección 1 |
| Cognito | Gratis hasta 10.000 usuarios activos al mes | 0,00 | 0,00 | Unos 400 usuarios |
| **Observabilidad** | | | | |
| CloudWatch y X-Ray | USD 0,30 por métrica; USD 0,10 por alarma; USD 0,50 por GB de logs | 12,00 | 13,50 | 20 métricas propias y 25 alarmas de la [#18](../architecture/observabilidad-slo.md) |
| Canario de Synthetics | USD 0,0012 por ejecución | 10,37 | 10,37 | Cada 5 minutos |
| API de Cost Explorer | USD 0,01 por llamada | 0,90 | 0,90 | 3 llamadas al día |
| **Seguridad** | | | | |
| GuardDuty | Por eventos analizados | 20,00 | 20,00 | 6 cuentas. Estimación |
| AWS Config | USD 0,003 por elemento; USD 0,001 por evaluación | 16,00 | 16,00 | Estimación |
| **Pruebas y desarrollo** | | | | |
| Pruebas (Test) | Endpoints en 2 zonas, 1 attachment y uso por demanda | 70,70 | 70,70 | Ambiente aislado de la #7 |
| Desarrollo (Dev) | Sin attachment; endpoints solo mientras se prueba | 25,00 | 25,00 | Estimación |
| **Total** | | **USD 1.586,26** | **USD 1.618,19** | |
| **En pesos** | | **COP 5.136.040** | **COP 5.239.424** | |

**En un año,** con 6 meses normales y 6 de cosecha: **USD 19.227, unos COP 62,3 millones.**

## 3. Invocaciones de funciones en cosecha

El enunciado pide este cálculo aparte. Todas las funciones corren en Lambda arm64 a USD 0,20 por millón de invocaciones y USD 0,0000133334 por GB-segundo.

| Función | Invocaciones en el mes de cosecha | Duración y memoria | Costo (USD) | Sale de |
| --- | ---: | --- | ---: | --- |
| Normalizador de lecturas | 108.000 | 300 ms, 256 MB | 0,130 | Una por lectura agronómica |
| FN-04 lote de telemetría | 10.800 | 800 ms, 512 MB | 0,060 | Lotes de 10 lecturas, de la #16 |
| Despacho de ACK y alertas | 108.000 | 150 ms, 256 MB | 0,076 | Una por lectura, de la #12 |
| Posición del transportador | 10.800 | 300 ms, 256 MB | 0,013 | Lotes de 20 posiciones |
| Eventos del saco | 187.200 | 200 ms, 256 MB | 0,162 | 6 eventos por saco |
| Proyección a `sacos_publicos` | 187.200 | 150 ms, 256 MB | 0,131 | Una por evento |
| Consulta pública | 129.600 | 100 ms, 256 MB | 0,069 | Consultas del mes |
| FN-01, FN-02 y FN-03 (fotos de dron) | 150 | 400 ms, 512 MB | 0,000 | Fotos del mes pico |
| Funciones programadas (observabilidad y costo) | 2.190 | 2 s, 256 MB | 0,015 | Cada hora y cada día, de la #18 |
| **Total** | **743.940** | | **0,66** | |

Con la inferencia de la #17 (USD 0,47 en el mes pico), **las funciones y la inferencia cuestan unos USD 1,13 en el mes de cosecha.** Con la capa gratuita de Lambda (1 millón de invocaciones y 400.000 GB-segundos al mes por cuenta), Lambda costaría cero.

## 4. Costo partido por etiquetas

Se usa la categoría de costo de la #18 sobre las etiquetas de la landing zone. Mes de cosecha:

| Categoría | Etiqueta que la define | Líneas que entran | USD |
| --- | --- | --- | ---: |
| **Pruebas** | `Ambiente` = `pruebas` o `desarrollo` | Pruebas y desarrollo | 95,70 |
| **Drones** | `DronID` ≠ `NO-APLICA` | S3 de objetos de dron y su réplica, e inferencia | 27,02 |
| **Acopio** | `AcopioID` ≠ `MULTICENTRO` | 3 VPN y sus 3 attachments del Transit Gateway | 219,00 |
| **Fincas** | `FincaID` ≠ `GLOBAL` | Topics de alerta por finca e IoT Core por dispositivo | 35,98 |
| **Plataforma compartida** | Lo demás | Network Firewall, Resolver, endpoints, attachments de las VPC, ALB, base, funciones, observabilidad y seguridad | 1.240,49 |
| **Total** | | | **1.618,19** |

Los servicios que comparten las 200 fincas, como la cola, el normalizador o la tabla de telemetría, llevan `FincaID = GLOBAL` y caen en plataforma compartida. Para ver el costo por finca, el tablero de costo de la #18 divide esa parte entre las fincas activas. No hace falta poner 200 etiquetas en recursos compartidos.

## 5. Lo que muestran los números

**La red fija es el 83 % del costo.** Network Firewall, Route 53 Resolver, el Transit Gateway, las VPN y los endpoints de interfaz suman USD 1.322 al mes. Se pagan por hora, haya o no tráfico. En cambio, todo lo que crece con el piloto (ingesta, base, funciones e inferencia) no llega a USD 10 al mes, incluso en cosecha.

Por eso la diferencia entre un mes normal y uno de cosecha es de solo USD 32. La cosecha multiplica por tres la telemetría y por diez los sacos, pero esos servicios son baratos por unidad.

**El presupuesto de la #1 se queda corto en red.** La #1 le asigna a la cuenta de red USD 120 al mes, y solo Network Firewall cuesta USD 578. El total de la organización (USD 480 en mes normal y USD 750 en cosecha) se pasa por el doble. Hay dos salidas: subir el presupuesto, o bajar la red fija. Lo segundo es tarea de la [#31](https://github.com/aromapacifico-platform/planning/issues/31), con estas tres palancas:

| Palanca | Ahorro al mes | Qué se pierde |
| --- | ---: | --- |
| Quitar Network Firewall en el piloto y dejar los security groups, las NACL de la #9 y los firewalls de los acopios | ~USD 578 | Inspección de contenido centralizada. El tráfico del piloto es casi todo hacia servicios administrados que no pasan por ese firewall |
| Dejar solo el Resolver de entrada (2 ENI) o resolver los endpoints con una zona privada | USD 183 a 365 | Reenvío de la nube hacia el DNS de los acopios, que el diseño casi no usa |
| Endpoints de interfaz solo en una zona en desarrollo y pruebas, y retirar los que las funciones fuera de VPC no usan | ~USD 40 a 80 | Algo de disponibilidad fuera de producción |

**Un costo que se evitó:** la #15 proponía Route 53 Application Recovery Controller para la conmutación de la consulta. Su clúster cuesta USD 2,50 por hora, unos USD 1.825 al mes. La consolidación de la #19 lo reemplazó por health checks de Route 53, que cuestan USD 1.

## 6. Verificación de los criterios de la #29

| Criterio | Dónde se cumple |
| --- | --- |
| Cada línea de costo dice de qué cifra del caso sale | Secciones 1 y 2, columna "Sale de" |
| Las invocaciones de funciones en cosecha están calculadas aparte | Sección 3 |
| Se puede ver el costo partido por las etiquetas de la landing zone | Sección 4 |
