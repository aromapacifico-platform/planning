# Matriz de lo que se conserva y lo que se retira del diseño de 2020

## Para qué sirve esta matriz

El piloto de 2020 nunca llegó a producción. El enunciado lo retoma con una regla clara: se conserva
el requisito que sigue vigente y se reemplaza el supuesto que ya no se cumple. Esta matriz deja
escrito, en un solo lugar, qué pasa con cada pieza de 2020 y en qué historia del tablero se diseña
su reemplazo.

Del diseño de 2020 solo se conoce lo que describe el enunciado: el alcance, las capacidades y los
supuestos de conectividad. No hay inventario de equipos ni de servicios de nube, así que la matriz
trabaja sobre esos tres frentes y no inventa componentes que no se pueden verificar.

Hay tres decisiones posibles:

- **Se conserva:** el requisito sigue vigente y pasa tal cual al piloto de 2026.
- **Se reemplaza:** la necesidad sigue, pero la forma de resolverla de 2020 ya no sirve.
- **Se retira:** la pieza desaparece del diseño y nada ocupa su lugar.

## 1. Requisitos del negocio

El enunciado pide conservar el mismo territorio y las mismas capacidades. Ninguna de las cinco
capacidades se recorta ni se fusiona con otra.

| Requisito de 2020 | Decisión | Por qué | Dónde se diseña en 2026 |
|---|---|---|---|
| Alcance geográfico: Cauca, Huila y Tolima, hasta la entrega en Buenaventura | Se conserva | El piloto mantiene el territorio. Lo que cambia es que en Buenaventura no se instala nada de la Federación (ver sección 2) | #6 |
| Monitoreo del cultivo y del secado, con alerta al caficultor | Se conserva | Es el núcleo del piloto. Cambia el camino de la lectura: ya no se asume señal permanente | #11, #12 |
| Registro de la cosecha y del empaque en sacos de 60 kg | Se conserva | El saco de 60 kg sigue siendo la unidad que sale del beneficiadero | #15 |
| Seguimiento del viaje hasta el centro de acopio y hasta Buenaventura | Se conserva | Se mantiene, con un intervalo fijo de posición y qué evento queda guardado si el teléfono pierde datos | #6, #15 |
| Consulta de un saco por código para el caficultor, el centro de acopio y el comprador | Se conserva | Cada perfil ve una parte distinta del saco; el comprador nunca ve la cédula del caficultor ni la traza completa | #5, #15 |
| Servicio de drones: delimitar, confirmar la alerta, fumigar, verificar y estimar la cosecha | Se conserva | Los cinco servicios entran y ninguno reemplaza a otro. Se agrega lo que 2020 no definía: quién vuela, quién autoriza y con qué cadencia | #13, #14 |
| Tres aplicaciones: caficultor, transportador y consulta web | Se conserva | No se construyen; se deja la plataforma donde van a vivir y su sistema de diseño | #19, #38 |
| Rangos de alerta configurados por la Federación, no fijos en el dispositivo | Se conserva | El enunciado lo deja como supuesto vigente; los umbrales viven en la plataforma y su cambio queda auditado | #2, #12 |
| Retención de lecturas, fotos, vuelos e historia del saco por 5 años | Se conserva | Sigue siendo un requisito; ahora con cifrado en reposo y almacenamiento de archivo para que el costo no crezca cada año | #2, #5 |

## 2. Supuestos de conectividad

Aquí está la razón principal por la que el diseño de 2020 no se podía desplegar. Cada supuesto de
2020 tiene un reemplazo concreto.

| Supuesto o componente de 2020 | Decisión | Qué lo reemplaza | Dónde se diseña |
|---|---|---|---|
| Cobertura de datos en la mayoría de las fincas | Se reemplaza | La falta de señal es el caso normal, no la excepción. El nodo de finca guarda las lecturas hasta 24 horas y las envía al recuperar señal (store-and-forward) | #6, #11 |
| Dispositivo de finca publicando directo al punto de ingesta, en línea | Se reemplaza | El nodo publica por MQTT sobre TLS cuando hay señal y, si no hay, guarda en su buffer local. La alerta sale en menos de 5 minutos con señal, o al vaciar el buffer dentro de las 24 horas | #11, #12 |
| Fincas fuera de cobertura sin una solución definida | Se reemplaza | Sus lecturas entran sin instalar una radiobase nueva ni programar una visita semanal. La opción se elige y se costea en la historia de conectividad | #6, #28 |
| Red móvil de generaciones anteriores (2G y 3G) | Se retira | El piloto no usa 2G ni 3G en ninguna pieza: ni en el nodo de finca, ni en el dron, ni en el teléfono del transportador. El nodo usa LTE-M o NB-IoT, que están pensadas para dispositivos de bajo consumo | #6, #11 |
| Centros de acopio sin LAN ni enlace WAN | Se reemplaza | Cada centro tiene una LAN segmentada por zona, con SSID propio, y una salida WAN de 100 Mbps con túnel cifrado hacia la nube. Es el mismo patrón en los tres centros, cambiando el segundo octeto (41, 42 y 43) | #8, #9 |
| Puerto de Buenaventura sin LAN ni enlace WAN | Se retira | No se despliega infraestructura de la Federación en el puerto. La naviera conserva su telemetría y la plataforma solo registra el evento de entrega del saco, desde la aplicación del transportador o del operario | #6, #15 |
| Seguimiento del barco | Se retira | La naviera ya geolocaliza el barco. El recorrido de la plataforma termina en la entrega en puerto | #15 |
| Dron dependiente del enlace durante el vuelo | Se reemplaza | La misión se carga antes del despegue, en la cabecera municipal o en el centro de acopio. Si el enlace cae en el lote, el dron vuela la misión guardada y el registro de vuelo sube al recuperar el enlace | #13, #14 |

## 3. Costos y referencias de 2020

| Elemento de 2020 | Decisión | Qué lo reemplaza | Dónde se diseña |
|---|---|---|---|
| Precios de dispositivos, sensores y servicios de nube | Se retira | No sirven como cotización. Todo el costo se recalcula con precios actuales y con la fuente y la fecha de cada cotización | #28, #29, #30 |
| Arquitectura de nube de 2020 | Se reemplaza | No se replica. La plataforma de 2026 se monta en AWS con una landing zone de cuentas separadas, y Azure queda preparada como segunda nube | #1, #10 |
| Manual de marca o de interfaz de 2020 | Se retira | La Federación pide un sistema propio para este piloto, sin heredar el de 2020 | #35 a #38 |

## 4. Lo que esto significa para el resto del diseño

Los requisitos del negocio se conservan sin cambios. Lo que cambia es la ingeniería que los
sostiene, y en tres puntos:

1. **La conectividad deja de ser un supuesto.** Cada punto del recorrido (finca, dron,
   transportador, acopio y puerto) tiene que decir cómo sale el dato y qué pasa sin señal. Eso
   ahora vive en el cuerpo de la arquitectura (#6), no en un anexo.
2. **El acopio pasa de no tener red a ser la base de la operación en campo.** Ahí se precargan las
   misiones de los drones, se registran los sacos y se imprimen los códigos que falten.
3. **El puerto sale del alcance de la infraestructura.** Solo queda un evento en la historia del
   saco.

Los supuestos que esta matriz agrega están en
[`assumptions-log.md`](../cross-cutting/assumptions-log.md).
