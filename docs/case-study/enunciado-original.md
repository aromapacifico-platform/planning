# Ejercicio académico · Junior DevOps · Senior DevOps

## Reto: Actualización de la plataforma cafetera

Transcripción en Markdown del enunciado entregado por la Universidad Icesi
(`Ejercicio-Junior-Senior-DevOps-AromaPacifico.pdf`). Si hay diferencias, manda el PDF.

> Caso de estudio académico. Las cifras, el piloto y el diseño de 2020 son material de clase. No
> describen un proyecto oficial de la Federación Nacional de Cafeteros. Sirve para el perfil
> Junior DevOps y para el perfil Senior DevOps.

## Contexto

En 2020 se diseñó un piloto de trazabilidad del café, desde la finca hasta el comprador:
telemetría de cultivo, registro de beneficiadero, transporte terrestre, centro de acopio y
entrega en el puerto de Buenaventura. El alcance geográfico era Cauca, Huila y Tolima. Esa
arquitectura no se desplegó.

La Federación Nacional de Cafeteros lo retoma en 2026. No se replica la arquitectura de 2020. Se
conserva el requisito que siga vigente y se reemplaza el supuesto de conectividad que ya no se
cumple. Precios, dispositivos y servicios de nube de 2020 no son cotización válida.

El piloto que hay que dejar listo conserva el mismo territorio y las mismas capacidades:

- Monitoreo del cultivo y del secado, con alerta al caficultor.
- Registro de la cosecha y del empaque en sacos de 60 kg.
- Seguimiento del viaje hasta el centro de acopio y hasta Buenaventura.
- Consulta de un saco, por código, para el caficultor, el centro de acopio y el comprador.
- Servicio de drones para delimitar el lote, confirmar la alerta, fumigar, verificar y estimar la
  cosecha. El diseño elige agricultura de precisión, agricultura de áreas, o una combinación, y
  lo sostiene.

Hay tres aplicaciones previstas. No hay que construirlas. Hay que dejar la plataforma donde van a
vivir:

- Aplicación del caficultor.
- Aplicación del transportador.
- Consulta web de reportes y lectura del código del saco.

## Qué se actualiza

El diseño de 2020 asumía cobertura de datos en la mayoría de las fincas y un dispositivo
publicando telemetría directo al punto de ingesta. El centro de acopio y el puerto quedaban sin
LAN ni enlace WAN.

La actualización cierra estos flujos. Cada uno indica protocolo de salida, buffer local y qué
pasa cuando no hay señal:

- Finca y beneficiadero no tienen acceso cableado. Con señal celular, la telemetría publica al
  punto de ingesta. Sin señal, el dispositivo hace store-and-forward. El buffer local no retiene
  más de 24 horas.
- Hay fincas del piloto fuera de cobertura. Sus lecturas y objetos entran sin desplegar una
  radiobase nueva ni programar una visita semanal.
- El dron opera lejos del teléfono del caficultor. La misión se carga antes del despegue. El
  registro de vuelo y los objetos bajan por el enlace definido. Si el enlace cae, la misión queda
  en el buffer del dron. Sin cierre de ese registro no se autoriza la fumigación.
- El transportador publica posición en ruta. El diseño fija el intervalo y qué evento queda
  persistido si el teléfono pierde datos.
- Cada centro de acopio nace sin LAN. Hay que diseñarla, con segmentación y salida WAN hacia la
  nube.
- En Buenaventura no se despliega infraestructura de la Federación. La naviera conserva su
  telemetría. La plataforma solo registra el evento de entrega del saco.
- La red de acceso móvil cambió desde 2020. La solución no depende de una generación de red que
  el operador ya apagó o que vaya a apagar durante el piloto.

## Restricciones

No técnicas:

- En varias veredas el desplazamiento es difícil. La instalación en finca se hace en una sola
  visita y con poco equipo.
- El caficultor invierte poco. El alza de costos de insumos sigue. El hardware por finca y la
  cuota mensual tienen que ser moderados.
- Parte de los caficultores desconfía de dejar el cuaderno. La aplicación del caficultor tiene
  pocas pantallas.
- El dron no lo opera cada caficultor por su cuenta. El diseño dice quién vuela, quién autoriza
  una fumigación, con qué permiso y con qué frecuencia en el piloto.
- La implementación de infraestructura como código cabe en 2 semanas y en 100 horas. El alcance
  de ese esfuerzo es el código: módulos, variables, estado remoto y un plan ejecutable de un
  ambiente. Quedan fuera arquitectura, estimación de costo, sistema de diseño, release notes y
  sustentación.

Técnicas:

- Instalar la menor cantidad posible de hardware fijo en la finca.
- La nube principal la elige quien presenta y la justifica. El equipo de campo y el de plataforma
  no tienen por qué ser el mismo.
- El nodo de finca es autónomo en energía. En el lote no hay suministro eléctrico confiable.
- El equipo de la finca tiene que soportar humedad alta y temperatura alta.
- El patrón de red y de ingesta escala de 200 a 1.000 fincas sin rediseñar el direccionamiento ni
  el punto de ingesta.

## Supuestos

- Caficultor y transportador tienen teléfono inteligente con datos cuando están en cabecera
  municipal o en vía principal.
- El terreno de una finca del piloto se trata como una zona de cultivo. Dentro de la zona puede
  haber lotes.
- El café sale del beneficiadero en sacos de 60 kg.
- La naviera ya geolocaliza el barco. No hay que seguir el barco por fuera de la entrega en
  puerto.
- Los rangos de alerta los configura la Federación. No quedan fijos en el dispositivo.

## Cifras del piloto

- 200 fincas: Cauca, Huila y Tolima.
- Tres centros de acopio, uno por departamento.
- Cada finca tiene zona de cultivo y zona de secado.
- Cultivo: nitrógeno, fósforo, potasio, humedad y temperatura de aire y de suelo, cada 4 horas,
  las 24 horas.
- Secado: temperatura y humedad del café, cada hora, mientras el lote está en secado.
- Latencia de alerta, con ruta de entrega disponible: menos de 5 minutos desde la lectura fuera
  de rango. Sin señal, la alerta se emite al drenar el buffer, dentro de las 24 horas.
- 60 transportadores. En ruta se espera ubicación cada 5 minutos.
- En cosecha, cada centro de acopio recibe hasta 400 sacos al día.
- Consulta del saco en cosecha: picos de 30 lecturas por minuto.
- Retención de lecturas, fotos, vuelos y de la historia del saco: 5 años.

Rangos iniciales, configurables:

| Variable | Cultivo, alerta | Secado |
|---|---|---|
| pH | Fuera de 4,5 a 6,0. Recomendado entre 4,9 y 5,6 | No aplica |
| Humedad | Fuera de 40 % a 80 % | Cierre de lote cerca del 12 % |
| Temperatura | Fuera de 14 °C a 30 °C. Recomendado entre 17 °C y 23 °C | Grano por encima de 40 °C |
| Nitrógeno, fósforo, potasio | Fuera del rango que publique la Federación para el piloto | No aplica |

## Drones: plagas, fumigación y servicios

El piloto necesita un servicio de drones, no un vuelo suelto. La plataforma crea la orden, la
autoriza, la entrega al equipo de vuelo y guarda el resultado. No se pide operar el dron ni
definir dosis, mezcla o producto.

Servicios del piloto. Los cinco entran. No se sustituye uno por otro:

- **Delimitar el lote.** El primer vuelo deja el polígono y las zonas donde no se fumiga. Sin eso
  la orden de fumigación no puede salir.
- **Confirmar la alerta del sensor.** El dron va al foco que marcó la lectura, no a recorrer toda
  la finca.
- **Fumigación.** Solo sobre un lote ya delimitado y con una orden autorizada. La plataforma
  guarda quién autorizó, quién voló, la ventana, el identificador del lote de producto usado y el
  cierre del vuelo. Si no hay polígono del lote o no hay cierre del registro, la orden no sale.
- **Verificar después de fumigar.** Una foto o un recorrido corto cierra el caso. Si ese archivo
  no llega, la fumigación sigue abierta.
- **Estimar la cosecha.** Un vuelo de área, una vez por cosecha, para que el centro de acopio sepa
  cuántos sacos vienen. No fumiga.

Modo de trabajo, lo elige el diseño:

- Agricultura de precisión: confirmar la alerta, fumigar el foco y verificar ese mismo lote.
- Agricultura de áreas: delimitar la finca y estimar la cosecha. No fumiga toda el área.
- Combinación: áreas para el polígono y la estimación, precisión para el foco y la fumigación. El
  diseño dice qué evento pasa de un modo al otro.

La orden de fumigación lleva: finca, lote, motivo, ventana, operador y quién autoriza. Hay zonas
donde no se vuela: casas, beneficiadero, vías y fuentes de agua. Esas zonas viven en la
plataforma antes del primer vuelo.

Si el enlace cae en el lote, la misión ya va cargada: se preposiciona en cabecera municipal o en
el centro de acopio. El registro de vuelo se publica al restablecer el enlace. El estado de la
fumigación no pasa a cerrado hasta persistir ese registro.

## Objetivo

Diseñar y sustentar la actualización del piloto: gobierno, seguridad, conectividad, red de los
centros de acopio, IoT, drones, trazabilidad del saco, funciones de inferencia, automatización,
observabilidad, costo y sistema de diseño.

Quien presenta no implementa lógica de negocio, aplicaciones ni firmware. Elige la nube principal
y deja preparada una segunda, sin duplicar la plataforma. Todo supuesto que no esté en este
enunciado queda escrito en la propuesta.

## Reto

### 1. Gobierno

- Landing zone: cuentas, suscripciones o proyectos separados para seguridad, red, producción y
  pruebas.
- Políticas, identidades, etiquetas y presupuestos aplicados desde la raíz. Las etiquetas
  alimentan el costeo por fincas, drones, acopio, viajes y ambientes.
- Auditoría de lectura de un saco, cambio de un umbral, publicación de telemetría y entrega de un
  objeto de vuelo.
- Registro de qué requisito de 2020 se conserva y qué componente se retira. Va en el documento de
  arquitectura.

### 2. Seguridad

- Identidades separadas y mínimo privilegio: caficultor, transportador, operario de acopio,
  comprador de solo lectura del saco, operador de drones y operador de plataforma.
- MFA para operario de acopio, operador de drones y operador de plataforma.
- Cifrado en tránsito (TLS) y en reposo. Telemetría de finca y objetos del dron no se publican en
  claro.
- El identificador del saco no expone la cédula del caficultor ni la traza completa al comprador.
  El comprador recibe origen, fechas de proceso, estado y variables de secado. Acopio recibe el
  viaje. El caficultor recibe sus fincas.
- Datos personales de caficultores y transportadores. Retención: 5 años.
- Baja de un nodo de finca o de un dron perdido: se revoca la identidad y el dispositivo deja de
  publicar.

### 3. Red y conectividad

El diseño de conectividad cubre finca, dron, transportador, centro de acopio y puerto, con el
comportamiento sin señal. No va en un anexo.

Inventario de cada centro de acopio. Estas direcciones quedan reservadas y la nube no puede
solaparse con ellas. Todavía no hay equipos: la tabla es el espacio al cablear el sitio. Se
repite el mismo esquema en los tres centros, cambiando el segundo octeto: 41 Cauca, 42 Huila, 43
Tolima.

Ejemplo Cauca:

| Zona | Uso | Clientes previstos | Red reservada |
|---|---|---|---|
| Gerencia | Escritorio y teléfonos | 2 escritorios, 5 teléfonos | 10.41.1.0/24 |
| Soporte | Escritorio y teléfonos | 2 escritorios, 5 teléfonos | 10.41.2.0/24 |
| Logística | Recepción de sacos e impresiones | 2 escritorios, 20 teléfonos | 10.41.3.0/24 |
| Transporte | Teléfonos de conductores en patio | 20 teléfonos | 10.41.4.0/24 |
| Visitantes | Invitados | 10 teléfonos | 10.41.5.0/24 |
| Servidores locales | Impresión y control de la red | Por diseñar | 10.41.10.0/24 |
| Enlace a la nube | Borde | Firewall del centro | 10.41.20.0/24 |

Se pide:

- WLAN segmentada por zona, con SSID propio. La VLAN de visitantes no enruta hacia logística ni
  gerencia.
- Capacidad de referencia por cliente activo: 2 Mbps de bajada y 0,5 Mbps de subida. Hay control
  de tráfico no operativo.
- Firewall de perímetro en cada centro y firewall de nube. Tabla de políticas: origen, destino,
  puerto, acción y si la regla queda en el piloto o es temporal.
- Plan de direccionamiento de la nube, sin solapar 10.41.0.0/16, 10.42.0.0/16 ni 10.43.0.0/16.
  Subredes mínimas: ingreso de telemetría, ingreso de objetos de dron, aplicación, datos, object
  storage, administración y consulta pública. Desarrollo, pruebas y producción usan CIDR
  distintos.
- WAN de cada centro: 100 Mbps simétricos, compartidos con la operación.
- Data path de telemetría de finca, de posición del transportador y de objetos del dron. Pueden
  ser distintos.

### 4. Automatización y cambio

- Infraestructura como código del patrón de red, seguridad y un ambiente. No se instancian las
  200 fincas: se entrega el módulo reutilizable de una finca.
- Pipeline de la plataforma, de la ingesta y de la recepción de objetos de vuelo.
- Ambientes de desarrollo, pruebas y producción, con promoción controlada.
- Secretos fuera del repositorio y fuera del estado.
- Dos plantillas de release notes, llenas con un ejemplo cada una. Aplicación: una salida de la
  consulta del saco o de las alertas. Infraestructura: un cambio de red, del firewall, de la
  ingesta o del camino del dron. En ambas se lee qué cambia, la ventana, el impacto, la
  aprobación, el aviso a la Federación y cómo se vuelve atrás.
- No hay cambio productivo entre las 05:00 y las 18:00 en semana de cosecha, salvo incidente.

### 5. Cargas

#### Parte A. Monitoreo de finca

- Ingesta de telemetría de cultivo y de secado, con los umbrales de la tabla de cifras.
- Historial para el caficultor y para el reporte del piloto.
- El síntoma visible del cafeto entra por el servicio de confirmación del dron, no por una
  revisión semanal aparte.

Cifras de ingesta en operación normal:

- Cultivo: 200 fincas × 6 lecturas al día.
- Secado activo, en cosecha: unas 100 fincas × 24 lecturas al día.
- Ubicación: 60 transportadores × 12 posiciones por hora, en una jornada de 10 horas.

#### Parte B. Drones de plagas y fumigación

Los cinco servicios, el modo de vuelo y el store-and-forward de la misión están en la sección de
drones. Aquí solo entra la cadencia del piloto.

En cosecha hay una campaña de revisión al mes y las fumigaciones que salgan de los casos
abiertos. Fuera de cosecha, una campaña de revisión cada tres meses. El diseño puede cambiar esa
cadencia si lo justifica. La inferencia de esos objetos está en la parte E.

#### Parte C. Saco y viaje

- Estados del saco: en preparación, en viaje al acopio, en acopio (aceptado o rechazado), en
  viaje al puerto, entregado en puerto (aceptado o rechazado).
- Alta del saco en la finca, con peso e identificador.
- Paso del saco al transportador y llegada al centro de acopio.
- Salida hacia Buenaventura y entrega.
- Cada evento guarda fecha, hora y responsable.
- La consulta pública lee un saco y muestra solo la vista del comprador.
- Un despliegue no pierde eventos de saco. RPO de esos eventos: 15 minutos. RTO de la consulta
  pública: 4 horas.

#### Parte D. Centros de acopio

- Wifi y firewall del inventario.
- Puestos de logística que registran la recepción.
- Impresión de hojas de códigos para los sacos que lleguen sin código.
- El mismo patrón, tres veces, sin redibujar tres redes distintas si el patrón ya está.

#### Parte E. Funciones e inteligencia artificial

La inferencia del piloto es orientada a eventos. La función se invoca con un disparador y termina
al persistir el resultado. Según la nube elegida: Lambda, Azure Functions o Cloud Functions. No
hay cómputo persistente en espera de objetos.

La función no es el almacén. Lee el objeto ya persistido, llama a un servicio de inferencia
administrado y escribe el resultado en el expediente.

- Telemetría de cultivo, secado y posición: base transaccional o serie de tiempo.
- Fotos, mapas, polígonos y registros de vuelo: object storage.
- Eventos de saco y órdenes de fumigación: base transaccional.
- Salida de cada función: mismo expediente, con marca de tiempo, confianza e identificador del
  objeto de origen.

Disparadores:

- **Objeto de confirmación del foco.** La función invoca visión y persiste si el foco se
  confirma. No autoriza la fumigación.
- **Objeto de verificación.** La función persiste si el caso puede pasar a cerrado. Si el objeto
  no llega o la invocación falla, el estado no cambia.
- **Objeto del vuelo de estimación.** La función persiste el número estimado de sacos para el
  centro de acopio. No genera una orden de empaque.
- **Lote de telemetría.** La función marca la lectura fuera de umbral y persiste el resultado.
  Las reglas configurables siguen vigentes.

La autorización de fumigación es una identidad humana. Ningún disparador la ejecuta.

Si la invocación falla, el objeto de origen permanece y el estado del caso no cambia. El diseño
define reintentos, cola de fallos y dónde se observa el error.

No se entrena un modelo. Se usa inferencia administrada. El diseño indica la región del servicio,
qué objetos salen del país y el costo por mil invocaciones en cosecha. Los objetos son del
cultivo. Si el objeto contiene una persona, no se envía a inferencia y se documenta el
tratamiento del archivo.

### 6. Observabilidad

- Métricas, logs y trazas de la ingesta, de las aplicaciones, de la base, de los tres enlaces WAN
  y de la llegada de objetos de vuelo.
- Nodos y fincas sin telemetría por más de 24 horas.
- Alertas de cultivo no entregadas.
- Vuelos sin registro persistido, fumigaciones sin cierre e invocaciones fallidas que no mutaron
  el estado.
- Dos SLO, cada uno con su SLI: entrega de la alerta de cultivo y disponibilidad de la consulta
  del saco.
- Tablero operativo y tablero de costo, partidos por las etiquetas de fincas, drones, acopio y
  pruebas.

### 7. Sistema de diseño

La Federación, para este piloto, pide un sistema propio de las tres aplicaciones. No se hereda un
manual de 2020.

- Logo principal, isotipo y versiones en una tinta y en negativo.
- Paleta: primario, secundarios, neutros, estados del saco (en preparación, en viaje, aceptado,
  rechazado) y alerta de cultivo.
- Tipografía para teléfono y para la consulta web.
- Espaciado y grilla.
- Componentes base: botón, campo, alerta, tarjeta de saco y distintivo de estado.
- Reglas de uso: contraste al aire libre, iconos entendibles sin un manual largo, y la vista del
  comprador sin datos de más.

No se construyen las aplicaciones. Se entrega el sistema aplicado en una lámina o documento.

## Épicas

Las épicas 1 a 5 y la 7 se diseñan en los puntos del reto. No se vuelven a especificar aquí y no
entran en las 100 horas. La épica 6 es la única que se implementa en código, en 2 semanas y en
máximo 100 horas. El diagrama se diseña entero. El código cubre el patrón de un ambiente, no las
200 fincas ni los tres centros.

| Épica | Qué cubre | Dónde está el detalle |
|---|---|---|
| 1. Base de la plataforma | Landing zone, identidades, etiquetas y qué se retira de 2020 | Punto 1 |
| 2. Red y firewall | Direccionamiento, VLAN, SSID, WAN y políticas | Punto 3 |
| 3. Ingesta del cultivo | Telemetría, umbrales y buffer de 24 horas | Parte A |
| 4. Drones | Los cinco servicios, la orden de fumigación y el enlace | Sección de drones |
| 5. Saco, viaje y consulta | Estados, RPO, RTO y códigos | Parte C |
| 6. Infraestructura como código | Módulos, plan y pipeline de un ambiente | Abajo. Máximo 100 horas |
| 7. Costo y sistema de diseño | Precios de ahora y las tres aplicaciones | Punto 7 y entrega de costo |

### Épica 6. Infraestructura como código

Única épica medida en las 100 horas y en las 2 semanas. El código debe poder generar un plan.

- Módulo de red del ambiente: subredes, rutas y asociación con el centro de acopio de un
  departamento.
- Módulo de seguridad: identidades de plataforma, cifrado y reglas de firewall marcadas como
  permanentes en el diagrama.
- Módulo de ingesta o de consulta del saco. Uno de los dos, el que el diagrama deje como patrón.
- Patrón de una función: disparador, permiso de lectura del objeto, permiso de escritura del
  resultado y permiso de invocación al servicio de inferencia. Las otras funciones quedan en la
  arquitectura y no se codifican en estas 100 horas.
- Variables de pruebas y de producción, sin secretos en el repositorio ni en el estado.
- Pipeline que ejecuta el plan y exige aprobación antes de aplicar en producción.

Observabilidad, SLO y las dos plantillas de release notes se entregan con el proyecto. No forman
parte de las 100 horas.

### Épica 7. Costo y sistema de diseño

Van en la entrega. No entran en las 100 horas.

- Costo del mes normal, del mes de cosecha, del hardware de una finca y de la campaña de drones,
  a precios de ahora.
- Sistema de diseño de las tres aplicaciones, aplicado en una lámina.

## Tareas de la entrega

1. **Arquitectura.** Documento de los siete puntos del reto y el diagrama completo. Incluye
   direccionamiento, firewall, store-and-forward, el flujo de plaga a fumigación y las funciones
   de inferencia.
2. **Plan de 100 horas.** Solo las tareas de la épica 6, con horas, responsable y orden. La suma
   no pasa de 100 ni de 2 semanas. Cada tarea apunta a una caja del diagrama que el código
   implementa.
3. **Infraestructura como código.** El patrón de la épica 6, alineado con ese diagrama.
4. **Costo y sistema de diseño.** Como están en la épica 7.
5. **Sustentación.** 20 minutos ante un arquitecto de la Federación, más preguntas. Hay que
   sostener la conectividad, el modo de vuelo y por qué el código de infraestructura cabe en 100
   horas.

## Criterios

1. Estrategia coherente con el piloto de 2020 actualizado: finca sin cable, poca inversión y
   consulta pública limitada.
2. Conectividad cerrada para finca, dron, transportador, acopio y puerto, incluido el caso sin
   señal.
3. Viabilidad: lecturas, casos de plaga, fumigación, sacos y cosecha salen de las cifras del
   caso. El modo de vuelo se sostiene. La infraestructura como código suma máximo 100 horas y
   cabe en 2 semanas.
4. Automatización y cambio: el código coincide con el diagrama, y las plantillas permiten
   aprobar, avisar y volver atrás.
5. Seguridad: identidades separadas, lecturas y fotos cifradas, firewall y vista del comprador.
6. Costo actual: supuestos visibles, hardware de finca, drones, invocaciones de las funciones en
   cosecha y al menos tres decisiones que bajan o evitan gasto.
7. Sistema de diseño aplicado a caficultor, transportador y consulta del saco.
8. Claridad de la sustentación.

## Entrega

- Diagramas.
- Plan de las 100 horas, solo de la infraestructura como código, con responsable y dependencia.
  Suma máxima: 100 horas y 2 semanas.
- Repositorio con la infraestructura como código.
