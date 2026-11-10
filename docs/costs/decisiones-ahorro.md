# Costos de AromaPacífico y decisiones que bajan el gasto

## Qué responde este documento

Reúne los cuatro costos que pide la Épica 7: hardware de una finca, mes normal, mes de cosecha y campaña de drones. Muestra las decisiones que bajan o evitan gasto, cada una con el costo con y sin la decisión.

Los cálculos completos están en sus documentos:
- [Hardware de una finca y del piloto](costo-hardware-finca.md) (#28).
- [Plataforma en mes normal y de cosecha](costo-mes-normal-y-cosecha.md) (#29).
- [Campaña de drones](costo-campana-drones.md) (#30).

**Tasa de cambio:** TRM de COP 3.237,83 por dólar. Todos los supuestos están en el [registro de supuestos](../cross-cutting/assumptions-log.md).

## 1. Los cuatro costos

| Costo | Valor | Documento |
| --- | --- | --- |
| **Hardware de una finca con cobertura**, puesta en la finca | USD 893 (COP 2,9 millones) y USD 0,30 al mes de conectividad | #28 |
| **Hardware de una finca sin cobertura**, con satélite | USD 1.434 (COP 4,6 millones) y USD 147 al mes de conectividad | #28 |
| **Plataforma en un mes normal**, con pruebas y desarrollo | USD 1.586 (COP 5,1 millones) | #29 |
| **Plataforma en un mes de cosecha** | USD 1.618 (COP 5,2 millones), de los que USD 1,13 son funciones e inferencia | #29 |
| **Campaña de drones contratada** | USD 79.436 el año 1 y USD 67.082 los siguientes. Unos USD 10.192 en el mes pico | #30 |

Estas cifras son el diseño **antes** de las decisiones de la sección 2, salvo la de drones, que ya incluye la decisión de contratar.

## 2. Decisiones que bajan o evitan gasto

### Decisión 1: contratar el servicio de drones en vez de tener cuadrillas propias

| | Costo al año | Inversión inicial |
| --- | ---: | ---: |
| Sin la decisión: cuadrillas propias con equipo comprado | USD 262.435 | USD 105.486 |
| Con la decisión: un prestador por acopio | USD 67.082 | USD 0 |
| **Costo evitado** | **USD 195.353 al año** | **USD 105.486** |

**Por qué funciona:** el piloto vuela 1.300 veces al año. Con cuadrillas propias, el personal y los vehículos (el 72 % del costo) se pagan todo el año aunque fuera de cosecha haya unos 17 vuelos al mes.

**Qué no se pierde:** los controles de vuelo dependen de la plataforma y no de quién es dueño del dron. Siguen la identidad con MFA, la misión precargada, la bitácora con hash y la autorización exclusiva del agrónomo. Detalle en la #30.

### Decisión 2: enlace de largo alcance compartido en vez de satélite en cada finca sin cobertura

La #28 mostró que el satélite es más del 99 % de la cuota de conectividad del piloto. La #6 dejó abierta la alternativa: un enlace de largo alcance desde la finca hasta un punto con señal.

**Diseño:**
- Cada finca sin cobertura agrega un módulo LoRa a su nodo.
- Unas cinco fincas vecinas comparten un gateway LoRaWAN con salida LTE, instalado donde sí hay señal: la vía principal o la cabecera, como dice el enunciado.
- El gateway entrega las lecturas por TLS a AWS IoT Core para LoRaWAN, y de ahí entran a la misma regla de ingesta de la #12.
- El buffer de 24 horas y el ACK de persistencia del nodo no cambian.
- El gateway se registra en **AWS IoT Core para LoRaWAN**. Así cada nodo conserva su propia identidad, con sus claves LoRaWAN, y el gateway solo reenvía. La baja de un nodo se sigue haciendo por nodo.

**Supuesto principal:** 80 % de las 60 fincas sin cobertura (48) alcanzan un gateway. Las 12 restantes se quedan con satélite. En montaña el alcance depende de la línea de vista, así que el número real sale de la preinspección de la #6.

| Ítem | Precio | Fuente |
| --- | ---: | --- |
| Gateway RAK7289CV2 exterior con LTE | USD 435 | [Rokland](https://store.rokland.com/collections/gateways/products/rakwireless-wisgate-edge-pro-16-channel-outdoor-lorawan-gateway-rak7289cv2-us915-lte-eg95-na), consultado el 9 de noviembre de 2026 |
| Antena, mástil, panel, batería e instalación del gateway | USD 465 | Reserva de ingeniería |
| Módulo LoRa y antena en el nodo de la finca | USD 25 | Reserva de ingeniería |

A todo se le aplican la logística (10 %) y el IVA (19 %) de la #28.

| | Cuota de conectividad del piloto al mes | Inversión del perfil sin cobertura |
| --- | ---: | ---: |
| Sin la decisión: 60 fincas con satélite | USD 8.820 | USD 34.319 |
| Con la decisión: 48 fincas por LoRa (10 gateways) y 12 con satélite | USD 1.774 | USD 20.216 |
| **Costo evitado** | **USD 7.046 al mes (USD 84.552 al año)** | **USD 14.104** |

La cuota de conectividad del caficultor sin cobertura pasa de **USD 147 a unos USD 0,20 al mes**, porque el gateway reparte entre cinco fincas una SIM de USD 1 al mes.

### Decisión 3: bajar la red fija del piloto

La #29 mostró que la red fija es el 83 % del costo de la plataforma y se paga por hora, haya o no tráfico.

| Cambio | Sin la decisión | Con la decisión | Costo evitado al mes |
| --- | ---: | ---: | ---: |
| Quitar Network Firewall en el piloto | USD 577,68 | 0 | USD 577,68 |
| Dejar solo el Resolver de entrada | USD 365,00 | USD 182,50 | USD 182,50 |
| Endpoints de pruebas en una sola zona | USD 29,20 | USD 14,60 | USD 14,60 |
| **Total** | | | **USD 774,78 al mes (USD 9.297 al año)** |

**Por qué se puede quitar Network Firewall:**
- El tráfico del piloto va casi todo a servicios administrados (IoT Core, API Gateway y S3) que no pasan por ese firewall.
- El tráfico que sí cruza la VPC ya lo filtran los security groups y las NACL del catálogo de la #9 y los firewalls de los tres acopios.
- Si la operación crece o una auditoría pide inspección de contenido, se agrega de nuevo con un cambio de IaC.

**El Resolver de salida** solo servía para que la nube resolviera nombres del DNS de los acopios, y el diseño casi no lo usa.

**Con esta decisión la plataforma queda en USD 811 en un mes normal y USD 841 en cosecha.** Sigue por encima de los USD 480 y 750 de la #1, así que el presupuesto de la #1 se actualiza con estas cifras.

### Gastos ya evitados en el diseño

Estas decisiones se tomaron antes, en otras historias. Aquí se recalculan con números:

| Decisión | Sin la decisión | Con la decisión | Costo evitado | Historia |
| --- | ---: | ---: | ---: | --- |
| Health checks de Route 53 en vez de Application Recovery Controller para la conmutación de la consulta | USD 1.825 al mes (USD 2,50 por hora) | USD 1 al mes | **USD 1.824 al mes** | #19, #29 |
| Bedrock por invocación en vez de Rekognition Custom Labels | Unos USD 352 al mes, aun encendiéndolo solo 4 horas los días hábiles | Unos USD 0,47 en el mes pico | **~USD 351 al mes**, sin contar el entrenamiento | #16, #17 |
| Ciclo de vida de S3 hacia IA y Deep Archive para los objetos de dron (propuesta del borrador junior) | Unos USD 181 al mes en el año 5, con todo en Standard | USD 27 al mes en el año 5 | **USD 154 al mes en el año 5** | #30 |
| Funciones serverless en vez de contenedores siempre encendidos (propuesta del borrador junior) | Unos USD 70 al mes por dos tareas mínimas | USD 0,66 en el mes de cosecha | **~USD 69 al mes** | #16, #29 |

El borrador junior también proponía **hardware abierto** como ahorro, frente a una estación agroclimática comercial. Ese ahorro no se puede recalcular sin cotizar una estación comercial equivalente con LTE-M, así que no se suma aquí. La #28 sí corrigió su cifra: el nodo puesto en la finca cuesta USD 893, no USD 145.

## 3. El piloto con y sin las decisiones

Totales del piloto de 200 fincas, en el escenario base de 60 fincas sin cobertura:

| Concepto | Sin las decisiones 1 a 3 | Con las decisiones 1 a 3 |
| --- | ---: | ---: |
| Hardware de las 200 fincas, una vez | USD 222.474 | USD 208.370 |
| Conectividad de las fincas al mes | USD 8.862 | USD 1.816 |
| Plataforma al año | USD 19.227 | USD 9.916 |
| Drones al año | USD 262.435 (cuadrillas propias) | USD 79.436 el año 1 y USD 67.082 después |
| **Año 1** | **USD 610.479 (COP 1.977 millones)** | **USD 319.514 (COP 1.035 millones)** |
| **Cada año siguiente** | **USD 388.006 (COP 1.256 millones)** | **USD 98.790 (COP 320 millones)** |

Las tres decisiones bajan el costo recurrente del piloto en **USD 289.216 al año**, unos COP 936 millones. El año 1 baja USD 290.966. Los drones son la mayor parte del ahorro. La de conectividad es la que más le importa al caficultor, porque su cuota mensual sin cobertura pasa de USD 147 a centavos.

## 4. Verificación de los criterios de la #31

| Criterio | Dónde se cumple |
| --- | --- |
| Cada decisión muestra el costo evitado con números, no solo un porcentaje | Sección 2: tres decisiones nuevas y cuatro ya tomadas, cada una con su costo con y sin la decisión |
| El consolidado tiene los cuatro costos que pide la Épica 7 | Sección 1, y el PDF `costs-aromapacifico.pdf` con los tres documentos de detalle |
