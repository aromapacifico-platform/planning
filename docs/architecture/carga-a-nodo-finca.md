# Nodo autónomo de finca: cultivo y secado

**HU:** [#11](https://github.com/aromapacifico-platform/planning/issues/11). **Responsable:** Juan Ocampo (`juandavid175`). **Revisión:** 7 de noviembre de 2026.  
**Estado:** especificación propuesta para revisión. No se han fabricado nodos, medido consumos ni realizado ensayos de calibración desde esta historia. El sensor económico de humedad del grano requiere cualificación antes de aprobar su uso; una ficha de humedad de suelo no acredita precisión en café.

## 1. Base revisada y decisiones sobre el borrador

Se revisó mediante GitHub MCP `planning/main` en `4c6fa27a31a5ac5c38c0da5711e36936024ba2cd`: [enunciado](../case-study/enunciado-original.md), [decisiones senior](../governance-and-decisions/briefing-inicial-juniors.md), propuesta junior y red integrada. La dependencia #6 está en la [PR #49](https://github.com/aromapacifico-platform/planning/pull/49), commit `af64c56128198c4978d23f5f1fc8cc699b6b1ff7`, todavía abierta al consultar. Se contrastó la identidad de dispositivos de la [PR #50](https://github.com/aromapacifico-platform/planning/pull/50), commit `e50838f23ec27818ff3497590811106b20e945ee`, también abierta. No se consideran cambios ya aprobados.

Se conserva ESP32-S3, SIM7080G con LTE-M/NB-IoT donde el operador lo habilite, RS485, energía solar y cola local de máximo 24 h. Para fincas sin esa cobertura se conserva RockBLOCK 9603/Iridium SBD de #6. La recepción satelital requiere su adaptador de plataforma; no es una conexión MQTT directa del módem a AWS.

| Propuesta junior | Resultado de la revisión de #11 |
|---|---|
| ESP32-S3 + SIM7080G | Se mantiene como plataforma de referencia, con la placa LilyGO H606/T-SIM7080G-S3 y alimentación externa regulada. Es una placa de desarrollo que requiere integración y protección. |
| Sonda genérica «7 en 1» | No se aprueba sin fabricante, modelo y protocolo verificables. Se propone SEN0604 (suelo/pH/EC) + SEN0605 (NPK) como alternativa cotizable; una sonda combinada podrá sustituirlas si supera la misma cualificación. Ninguna cubre el aire. |
| SHT30/SHT35 para secado | Mide temperatura/humedad relativa del aire, no contenido de agua del café. Se usa SHT31-D para **aire de cultivo** y una sonda de contacto separada para **grano**. |
| Celda LiFePO4 3,2 V, 6 Ah y autonomía >30 días | Se rechaza esa autonomía sin balance completo. 6 Ah a 3,2 V son 19,2 Wh nominales, diferentes de 6 Ah a 12 V. Se aumenta la reserva según sección 4. |
| Entrada solar/cargador de la placa | No se conecta el panel nominal de 12 V a la placa ni la batería LiFePO4 a su zócalo de Li-ion. Se usa regulador solar específico para 4S LiFePO4 y conversión a 5 V. |
| MicroSD con meses de datos | Se omite: la flash integrada permite una cola de 64 KiB. Más capacidad no permite retener lecturas por más de 24 h. |

Este archivo especifica hardware e interfaces; no implementa firmware ni aplicaciones. Los nuevos supuestos de esta HU deben incorporarse al registro transversal durante la revisión, sin modificar otros entregables aquí.

## 2. Variables, sensores y cobertura de medición

### 2.1 Matriz de medición

| Zona / variable | Sensor de referencia e interfaz | Campo y unidad | Frecuencia / condición |
|---|---|---|---|
| Cultivo: nitrógeno | DFRobot SEN0605, RS485 Modbus | `soil_n_mg_kg` | Cada 4 h, 6 muestras/día. |
| Cultivo: fósforo | SEN0605 | `soil_p_mg_kg` | Cada 4 h. |
| Cultivo: potasio | SEN0605 | `soil_k_mg_kg` | Cada 4 h. |
| Cultivo: humedad de suelo | DFRobot SEN0604, RS485 Modbus | `soil_moisture_pct`, con base/metodología declarada | Cada 4 h; calibración al suelo del piloto. |
| Cultivo: temperatura de suelo | SEN0604 | `soil_temperature_c` | Cada 4 h. |
| Cultivo: pH | SEN0604 | `soil_ph` | Cada 4 h; incluye la variable de la tabla de rangos del caso. |
| Cultivo: humedad del aire | SHT31-D, I²C corto y protegido | `air_rh_pct` | Cada 4 h; bajo abrigo ventilado. |
| Cultivo: temperatura del aire | SHT31-D | `air_temperature_c` | Cada 4 h; fuera del calor del gabinete/panel. |
| Secado: temperatura del grano | Sonda de contacto SEN0600, RS485, **candidata a cualificar** | `grain_temperature_c` | Cada hora mientras exista lote activo, hasta 24 muestras/día. |
| Secado: contenido de humedad del grano | Canal dieléctrico SEN0600 **más curva específica de café validada**, o sustitución por sensor industrial apto para café | `grain_moisture_wb_pct` | Cada hora; porcentaje de agua en **base húmeda**, no %RH del aire ni porcentaje de suelo sin transformar. |

SEN0604 y SEN0605 son sondas IP68 de 5–30 V; sus fichas aportan registros y rangos [S2–S3]. Se alimentan a 12 V mediante salida conmutada y se configuran direcciones Modbus únicas en taller. Se registra el tipo de magnitud: EC no se usa como sustituto de las tres lecturas N/P/K. El campo de nutrientes es una estimación del instrumento contrastada con análisis de suelo, no una receta de fertilización.

Los rangos del caso se cargan como configuración versionada de plataforma: pH 4,5–6,0, humedad 40–80 %, temperatura 14–30 °C; recomendaciones pH 4,9–5,6 y temperatura 17–23 °C; N/P/K según Federación. La plataforma debe distinguir humedad del aire, humedad del suelo y humedad del grano, y definir la base del umbral de suelo antes de activarlo. No se copia un 40–80 % indistintamente entre magnitudes. En secado se vigila temperatura del grano >40 °C y proximidad al 12 % de humedad; la decisión de cierre del lote pertenece al flujo de negocio, no a una salida automática del sensor.

### 2.2 Cualificación obligatoria de humedad del café

La referencia económica SEN0600 tiene precio público, salida de humedad/temperatura e IP68, pero su ficha es de **suelo** y no suministra calibración certificada de café [S4]. No se presenta como medidor de café validado ni se aplica su precisión de suelo a `grain_moisture_wb_pct`.

Antes de enviar el equipo a campo, se realiza en taller/laboratorio una cualificación con el café pergamino y condiciones representativas del piloto:

1. Obtener muestras con humedad de referencia mediante procedimiento gravimétrico de laboratorio apropiado para café. Cenicafé documenta el seguimiento gravimétrico del secado y la distinción de humedad en base húmeda [S13].
2. Comparar al menos cinco niveles que cubran el secado, incluyendo 10, 12 y 16 %, además de niveles húmedos representativos; repetir con temperaturas y compactaciones distintas. No extrapolar por encima del rango ensayado.
3. Ajustar y versionar la curva que transforma la salida del sensor a porcentaje en base húmeda; verificarla con muestras independientes. Objetivo de diseño propuesto: error absoluto ≤1 punto porcentual cerca de 10–16 % y temperatura ≤1 °C respecto de referencia. Son criterios de aceptación de banco, **no resultados obtenidos**.
4. Verificar además compatibilidad de materiales con el café, limpieza y montaje representativo. Si hay saturación, curva no reproducible, incompatibilidad de contacto o no se cumple el error, **rechazar SEN0600 para grano**. Sustituir por sonda de humedad de granos con curva documentada para café y presupuesto actualizado. GMS1081-C-CER-AL3.0 es una alternativa industrial a cotizar, no una compra aprobada ni una calibración de café demostrada [S14].

No se declara cerrada la aceptación metrológica del secado mientras falte esa prueba o el modelo sustituto. La calibración sucede antes de la visita de instalación; durante ella solo se comprueba la curva cargada con un instrumento de referencia. Una lectura inválida se publica con calidad/motivo, nunca se rellena con un valor supuesto. Cerca del cierre, una lectura cuya incertidumbre abarque el umbral requiere comprobación de referencia.

Para NPK, pH y humedad de suelo también se documentan contrastes de banco, unidades, método y tolerancias acordadas con el agrónomo. Un registro Modbus que responde no prueba exactitud agronómica.

## 3. Patrón físico, alimentación y protección

Se distinguen **punto de cultivo C** y **punto de secado S**. Se propone un solo controlador/comunicador por finca cuando ambos puntos admitan un cable RS485 de hasta 30 m, con ruta protegida y caída de tensión validada. Es un límite conservador del diseño, no la distancia real de todas las fincas. El controlador compartido se ubica junto a C: I²C del sensor de aire queda corto y protegido, sin extenderlo hasta el secadero ni medir su aire caliente como aire de cultivo.

Si los puntos están más lejos o el tendido cruza zonas no protegibles, se instalan dos conjuntos autónomos C y S, sin inventar un enlace wifi/LoRa no definido. Cada controlador tiene identidad, energía y módem propios. La inspección previa decide esto; el presupuesto no asume automáticamente que una finca equivale a un solo gabinete.

| Elemento | Especificación del patrón |
|---|---|
| Controlador | LilyGO T-SIM7080G-S3 H606, ESP32-S3, flash integrada de 16 MB; fijar revisión de placa. GNSS, wifi, BLE, LEDs y periféricos no utilizados apagados. No se usa la corriente de sueño del chip como consumo total de placa. |
| Celular | SIM7080G + SIM/APN M2M comprobados en el predio, LTE-M o NB-IoT. Un mapa 4G no acredita estos servicios. No hay dependencia ni fallback 2G/3G. Si falla la habilitación IoT se asigna el perfil satelital de #6 antes de instalar. |
| Satelital | RockBLOCK 9603 con supercondensadores conservados y antena patch con vista al cielo a través de ventana RF plástica; módem celular desenergizado en ese perfil. No se requiere que el agricultor viaje para subir las lecturas. |
| Solar celular | Panel 15 W nominal 12 V, Vmp/Voc reales compatibles con el regulador. No es una salida directa de 12 V al ESP32. |
| Solar satelital | Dos paneles idénticos de 15 W en paralelo: 30 W totales. Verificar suma de Isc y Voc a temperatura mínima frente al controlador. |
| Reserva celular | LiFePO4 4S comercial nominal 12 V, 6 Ah, con BMS/PCM y limitación térmica de carga. |
| Reserva satelital | LiFePO4 4S comercial nominal 12 V, 12 Ah. No es la celda de 3,2 V del borrador. |
| Carga | Genasun GV-5-Li-14.2V de referencia, perfil de 4S LiFePO4 sin ecualización de plomo. Compatibilidad escrita batería/cargador antes de compra; si el fabricante exige otro perfil, usar versión configurada y actualizar costo. Se reserva reducción de capacidad por carga parcial. |
| Distribución | Batería → fusible cercano y protección de polaridad → regulador 5 V → USB/alimentación 5 V autorizada de la placa. No se usa a la vez el cargador Li-ion integrado. Buck Pololu D24V22F5 de referencia, con capacidad de pico y disipación verificadas. |
| Sensores y RS485 | Adaptador aislado DFR0845 (UART 3,3 V); salida de sensores conmutada. En conjunto compartido usar 12 V aislados y validar que sensores/cable caben dentro de 2 W de su salida. No puentear masas para anular aislamiento. Terminación solo en extremos, polarización única, cable trenzado, TVS y conectores etiquetados. |
| Identidad y reloj | Elemento seguro ATECC608 para clave privada y DS3231 con respaldo de reloj. Configuración/curva firmadas, secuencia persistente y hora UTC. |
| Gabinete | Objetivo IP67 ensamblado: policarbonato UV, prensaestopas y conectores con protección compatible, membrana de compensación, desecante y bucle antigoteo. La placa, reguladores y breakouts no son IP67 por sí solos. |
| Entorno | Bajo sombra, por encima de inundación y fuera de contacto con café/aspersión; sonda de aire ventilada bajo abrigo, nunca encerrada en la caja estanca. Controlar temperatura de batería y humedad interior; el RockBLOCK de referencia no es impermeable. |

La alimentación 5 V se diseña con reserva de pico, desacoplo junto al módem y prueba de caída de tensión; el presupuesto de energía media no dimensiona por sí solo esos picos. Ground Control exige fuente estable de al menos 500 mA para RockBLOCK 9603 Rev F y conservar sus supercondensadores [S9]. Se comprueba el pico celular de la revisión seleccionada y la temperatura del buck dentro del gabinete. No se ensambla en protoboard.

Se instala medición de tensión y temperatura de batería y se bloquea carga fuera de sus límites de fabricante; el BMS no se presume térmico sin documentación. Si no incorpora ese corte, el kit necesita protección térmica independiente en la ruta de carga, ensayada sin quitar alimentación al registrador; no se inventa un puerto NTC en el GV-5. El mantenimiento ordinario incluye limpieza y revisión visual por el productor, diagnóstico remoto y reposición por avería; no hay ruta de recolección semanal de datos ni se promete mantenimiento cero.

## 4. Balance de energía y días nublados

### 4.1 Supuestos explícitos del cálculo

El dimensionamiento usa **límites de ingeniería por verificar en banco**, no consumos medidos: 5 mA a 5 V de reposo del conjunto electrónico; 2 mA adicionales a 12 V para consumo propio de conversión, cargador, BMS y protecciones; ventanas activas de hasta 120 s; 2 W medios en ventana celular y 3,5 W en satelital, incluyendo controlador y módem pero no sensores. La corriente instantánea puede superar esos promedios. La referencia LilyGO publica corrientes distintas por revisión [S1]; los valores de menos de 50 µA del chip no se trasladan a todo el nodo.

Se energizan suelo/NPK hasta 60 s por muestra (1,2 W combinados, margen sobre fichas), aire hasta 60 s (0,06 W) y grano hasta 30 s (1 W). Lectura y comunicación se solapan dentro de la ventana activa; si el calentamiento/estabilización real necesita más, se recalcula. El contador de radio limita **128 ventanas totales en cualquier periodo móvil de 24 h**, incluidas sesiones con ACK, reintentos y comprobaciones. No son 128 por sensor. No hay OTA ni GNSS permanente incluidos en este presupuesto.

Energía de reposo/protección: `5 V × 0,005 A × 24 h + 12 V × 0,002 A × 24 h = 1,18 Wh/día`.

Sensores con cultivo y secado activo: `1,2 W × 60 s × 6 / 3600 + 0,06 W × 60 s × 6 / 3600 + 1 W × 30 s × 24 / 3600 = 0,326 Wh/día`.

Se añade 25 % de margen: `E_día = (1,18 + E_sensores + N_ventanas × P_activa × 120/3600) × 1,25`.

| Escenario | Ventanas/día | Celular, Wh/día | Satelital, Wh/día |
|---|---:|---:|---:|
| Solo cultivo | 6 | 2,13 | 2,51 |
| Solo secado activo | 24 | 3,73 | 5,23 |
| Cultivo y secado, un envío por registro | 30 | 4,38 | 6,26 |
| Interrupción y reintentos, ambos puntos | 128 máximo | **12,55** | **20,55** |

Un día tiene 6 registros de cultivo y 24 de secado activo: **30**, no 24. El perfil combinado es el dimensionamiento conservador; las coincidencias horarias no se descuentan como ahorro garantizado.

### 4.2 Reserva utilizable

Se usa 12 V nominal de ficha conservadoramente. Se aplican factores independientes: 80 % de profundidad de descarga, 80 % de capacidad al final de vida, 85 % de conversión y 90 % por carga parcial/margen térmico. El último factor es una reserva asumida, no una medición de SOC a 14,2 V; debe comprobarse con la batería y el perfil de carga elegidos. La carga recuperada del panel se compara ya descontando pérdidas.

`E_útil = 12 V × Ah × 0,80 × 0,80 × 0,85 × 0,90`.

| Perfil | Batería | E nominal | E útil presupuestada | Autonomía sin aporte solar, operación normal combinada | Sin aporte solar, reintentos máximos |
|---|---|---:|---:|---:|---:|
| Celular | 12 V / 6 Ah | 72 Wh | **35,25 Wh** | 8,04 días | 2,81 días |
| Satelital | 12 V / 12 Ah | 144 Wh | **70,50 Wh** | 11,27 días | 3,43 días |

La celda original de 3,2 V/6 Ah solo aportaría `19,2 × 0,80 × 0,80 × 0,85 × 0,90 = 9,40 Wh` con esos factores. No cubre ni un día del escenario celular de reintentos máximos. Por eso se aumenta la batería y no se repite «más de 30 días».

### 4.3 Prueba de escritorio de nubosidad

Hipótesis de diseño para **tres días consecutivos nublados**: 0,5 horas solares pico (HSP) por día y factor neto de captación/almacenamiento/conversión de 0,65. HSP es radiación equivalente, no horas de luz. No es un dato meteorológico medido en las 200 fincas: la preinspección y el ensayo deben confirmarlo para cada sitio y evitar sombras persistentes.

`E_solar = W_panel × HSP × 0,65`.

| Perfil | Aporte por día nublado | Demanda extrema/día | Déficit en tres días | Reserva útil | Resultado del modelo |
|---|---:|---:|---:|---:|---|
| Celular, 15 W | 4,88 Wh | 12,55 Wh | 23,02 Wh | 35,25 Wh | Cabe en la reserva inicial. |
| Satelital, 30 W | 9,75 Wh | 20,55 Wh | 32,40 Wh | 70,50 Wh | Cabe en la reserva inicial. |

Con 2 HSP/día el aporte sería 19,50 Wh celular y 39 Wh satelital: supera la demanda extrema modelada. Tras los tres días nublados, si continúa esa demanda extrema y vuelve ese aporte, la recuperación calculada es de 3,31 días y 1,76 días respectivamente. Esos tiempos presuponen batería inicialmente cargada, panel limpio, temperatura válida y cargas dentro de los límites; no son garantía frente a cualquier sucesión de clima o avería. Si el sitio queda por debajo del supuesto, se aumenta panel/reserva antes del envío o no se acepta la ubicación.

Batería baja no autoriza borrar registros antes de tiempo ni ignorar muestreos silenciosamente. Se reporta estado, se limita radio al presupuesto, se protege el hardware ante descarga profunda y se registra cualquier intervalo de medición perdido. Si para mantener energía se retrasa la entrega hasta vencer, es un incumplimiento observable, no una solución al requisito. La ventana de 24 h del buffer sigue siendo independiente de los días de autonomía.

## 5. Persistencia, reconexión y vencimiento de 24 horas

1. Medir y validar calidad; crear `event_id`, `device_id`, `farm_id`, punto C/S, `batch_id` si aplica, hora UTC, secuencia, versión de calibración/configuración, valores, unidades y motivo de error si existe.
2. Escribir en flash de forma atómica con checksum y diario de recuperación **antes de transmitir**. Reservar al menos 64 KiB de cola/índices; 30 registros × 256 bytes = 7.680 bytes/día como presupuesto local. El sobre de radio puede ser diferente.
3. Publicar por MQTT/TLS TCP 8883 con identidad individual y QoS 1, o enviar el sobre SBD del perfil satelital. Eliminar únicamente tras **ACK de aplicación de persistencia** del contrato de #12. PUBACK, éxito de SBD y HTTP 200 del proveedor no sustituyen ese ACK.
4. Reintentar según #6: 1, 5 y 15 minutos tras fallo, después cada 15 minutos con variación acotada. Se usa un planificador global, sin reiniciar la serie por cada registro nuevo, y se drena al detectar reconexión sin esperar el siguiente muestreo. Máximo 120 s por ventana y 128 ventanas/24 h; se cuentan también las fallidas. El límite que agote el presupuesto produce alarma y espera al siguiente hueco disponible, nunca un bucle sin cota. La prueba de banco valida compatibilidad entre esta cota, detección de reconexión y entrega antes de 24 h.
5. Dar prioridad a pendientes cercanos a vencer, conservar identificadores al reenviar y deduplicar en plataforma. Un ACK tardío permite conciliar, sin recrear una muestra.
6. Al alcanzar `ahora − occurred_at >= 24 h` sin confirmación: retirar la carga útil del buffer activo, contabilizar `expired_unconfirmed` y guardar solo identificador, tiempos y motivo del incidente. No archivar valores en otra partición para eludir el límite. Al volver a comunicar, conciliar si estaba persistida pese a perderse el ACK; solo declarar pérdida confirmada si no existe en plataforma.

El vencimiento se comprueba con temporizador de mantenimiento de hasta un minuto y antes de leer/enviar/arrancar; no solo al recibir la lectura número 25. La limpieza lógica se acompaña de compactación y borrado de bloques según el diseño de flash; no se afirma borrado forense instantáneo. Durante un apagado el equipo no puede ejecutar limpieza: al arrancar purga vencidos **antes** de exponer o reenviar datos. La prueba de firmware debe comprobar que no existe un histórico accesible de lecturas vencidas.

El reloj de respaldo evita rejuvenecer registros al reiniciar; ajustes de hora no reinician la edad. Si el reloj pierde confianza y no se puede acotar la edad con el último estado persistente, no se reetiqueta el dato como nuevo ni se conserva indefinidamente: se descarta conservadoramente con incidente `clock_invalid`. Cola llena antes de 24 h es avería/configuración anómala, dado el dimensionamiento: no sobrescribir en silencio, reportar y proteger la integridad.

Como en #6, un corte total de todas las rutas que alcance 24 h impide garantizar simultáneamente cero pérdida y retención máxima de 24 h. Esa situación se registra e investiga. La observabilidad de #18 vigila ausencia de telemetría desde nube aun si el nodo no consigue avisar; se conservan los avisos de antigüedad propuestos a 12 h y 20 h.

## 6. Alta de identidad y una sola visita

### 6.1 Preparación en taller y cabecera, antes de desplazarse

La visita única es viable mediante **preparación previa**, no haciendo calibración y compras en la vereda. Se recoge por teléfono información de separación C/S, secadero, acceso, sombras y cobertura. El operador confirma LTE-M/NB-IoT y APN; si no lo hace, se prepara el kit satelital y se confirma viabilidad comercial. Una sola visita no puede garantizarse para un predio desconocido que luego requiera obra civil o antena no prevista.

En taller se ensamblan, cargan y prueban los conjuntos, arneses, direcciones Modbus, conmutación, consumo, calibración y gabinete. Se preparan curva y configuración firmadas; no se lleva una sonda de grano pendiente de ensayo. Se etiqueta cada conjunto con serial, `farm_id`, punto y `device_id`, sin claves impresas. Para dos controladores se usan dos identidades físicas; para uno compartido se diferencian C/S y sensores dentro de la misma identidad.

**Alta del certificado:**

1. Generar una clave ECC P-256 individual dentro del elemento seguro correctamente configurado/bloqueado; obtener su clave pública y CSR. La clave privada no sale al portátil, al módem ni al repositorio. Flash encryption/Secure Boot complementan esa protección, pero no se describen los eFuses del ESP32-S3 como un elemento ECC intercambiable sin integración.
2. Un operador autenticado con IAM Identity Center y MFA emite/registra el certificado desde el CSR en AWS IoT Core `us-east-1`, inicialmente inactivo; crear Thing y adjuntar principal/política acotada. AWS admite CSR con clave ECC P-256 [S12]. No se usan certificados o credenciales de bootstrap compartidos entre fincas.
3. Instalar solo certificado público, CA de servidor, endpoint, `ThingName`/ClientId y configuración del ambiente. El cliente TLS se ejecuta en el ESP32 y usa la firma del elemento seguro; no se propone exportar la clave para cargarla al almacén TLS del SIM7080G. La compatibilidad exacta de driver, módem y TLS debe probarse antes de campo.
4. Usar los temas propuestos en PR #50: `aromapacifico/fincas/{ThingName}/telemetria/cultivo`, `/telemetria/secado` y `/config` propio para recepción. #12 define el sobre de ACK; si viaja por `/config`, diferenciar explícitamente tipo `ack` y configuración. Si el contrato requiere otro tema, actualizar política antes del plan, sin comodines globales.
5. Activar en la sesión autorizada de puesta en servicio; comprobar publicación y recepción del ACK, rechazo de identidad/tema ajenos y baja de un certificado de prueba. No revocar el certificado productivo solo para ensayar. Registrar serial, certificado público/fingerprint, finca y evidencia, sin llave privada ni secreto en logs.

Para SBD no hay mTLS directo a AWS IoT. El sobre necesita autenticidad, protección contra repetición y cifrado de aplicación por dispositivo; el IMEI no autentica al productor. Se propone firma con la clave del elemento seguro más cifrado autenticado con material individual aprovisionado por el proceso seguro, fuera de Terraform. El adaptador comprueba identidad activa antes de persistir y enviar ACK. No se presume que desactivar el certificado IoT revoque automáticamente el webhook: #12 debe aplicar la misma baja en ese camino.

Los presupuestos de #6 son 200 bytes MO y 50 bytes de ACK/control MT por lectura. Firma, nonce, etiqueta y metadatos **cuentan** dentro de ellos; se exige prueba de serialización, cifrado y retorno, o actualización del costo y energía si no caben. Los límites del transporte 9603 son 340 bytes MO y 270 MT [S9]; que un mensaje quepa no demuestra que cueste lo presupuestado.

### 6.2 Equipo y secuencia en el predio

Equipo del técnico: portátil con herramientas/driver y configuración autorizada; teléfono con datos en cabecera; conversor USB-RS485 aislado (FIT0832 de referencia), multímetro, registrador USB de corriente, termómetro/medidor de humedad de café de referencia verificado; herramientas manuales, crimpadora, taladro a batería, broca/barrena, EPP y kit de repuesto. No se requiere electricidad del lote, soldadura, servidor local ni visita semanal.

| Paso de la única visita | Duración objetivo | Evidencia |
|---|---:|---|
| Confirmar emplazamiento, sombras, ruta de cable y enlace previsto | 30 min | Perfil C/S y celular/satelital; fotos y lectura de señal/sesión. |
| Fijar soporte, panel y gabinete; conectar batería/protecciones | 60 min | Polaridad, tensiones, sujeción y entrada de carga. |
| Colocar sondas suelo/aire/grano y arnés prefabricado | 45 min | Ubicación/profundidad agronómica, dirección y curva; sensor de aire ventilado. |
| Vincular identidad ya preparada y probar entrega/ACK | 30 min | Lectura persistida en plataforma con hora original; confirmar ACK en nodo. |
| Cortar enlace, medir/guardar, reiniciar y restablecer | 30 min | Recuperación de pendiente e idempotencia; no se espera 24 h en campo. |
| Sellar, verificar temperatura/picos y capacitar al productor | 30 min | Lista firmada, seriales, referencia de café y canal de soporte. |
| Reserva de montaje/prueba | 45 min | Corrección con repuestos llevados. |
| **Total objetivo, un conjunto compartido** | **4 h 30 min** | Tiempo en sitio; no incluye desplazamiento ni la preparación de taller. |

Para dos conjuntos separados se reserva como objetivo hasta 7 h 30 min en sitio durante la misma visita, con ambos kits prearmados; ese tiempo debe verificarse en ensayo de montaje. Si no caben en la jornada o exigen obra, se rediseña/prepara antes de programarla. El técnico lleva repuesto compatible de sonda, arnés, fusible y controlador ya provisionado para sustituir una falla durante esa visita.

La prueba de campo adelanta los ciclos sin alterar permanentemente su frecuencia. El vencimiento de 24 h y los tres días de autonomía se ensayan previamente en banco; no se presentan los 30 minutos de desconexión como sustituto de esas pruebas. Un kit que no entregue/reciba ACK en el enlace elegido no queda aceptado.

## 7. Lista de materiales y precios consultados

**Consulta: 7 de noviembre de 2026, USD, cantidad 1 y precio público de referencia.** Son precios web observados, no ofertas vinculantes entregadas en Colombia. Se excluyen transporte, importación, impuestos, mano de obra, calibración y servicio de datos. Se separan los importes observados de reservas propias; no se reciclan costos de 2020 ni la conversión COP/USD del borrador. La historia de costos añadirá TRM de fecha, logística y cotización de volumen. La disponibilidad se confirma antes de comprar; las páginas de LilyGO/RockBLOCK mostraban etiquetas de agotado.

### 7.1 Conjunto celular compartido C+S

| ID | Elemento / modelo de referencia | Cantidad | USD unitario | USD subtotal | Evidencia / condición |
|---|---|---:|---:|---:|---|
| B01 | LilyGO T-SIM7080G-S3 H606 | 1 | 29,60 | 29,60 | [S1], fijar versión y disponibilidad. |
| B02 | DFR0845 UART/RS485 aislado | 1 | 19,90 | 19,90 | [S6], comprobar carga combinada de sensores. |
| B03 | ATECC608 breakout Adafruit 4314 | 1 | 4,95 | 4,95 | [S7], configurar/bloquear en taller. |
| B04 | DS3231 Adafruit 3013 | 1 | 17,50 | 17,50 | [S8], respaldo de reloj aparte. |
| B05 | Buck 5 V Pololu D24V22F5 | 1 | 26,95 | 26,95 | [S10], ensayo de pico y consumo. |
| B06 | GV-5-Li-14.2V-RETAIL, 4S LiFePO4 | 1 | 104,00 | 104,00 | [S11], no confundir con precio inicial de versión para plomo. |
| B07 | Bioenno BLF-1206A, batería sola 12 V/6 Ah | 1 | 79,99 | 79,99 | [S15], compatibilidad de carga/temperatura pendiente de confirmar. |
| B08 | ACOPOWER HY015-12P, panel 15 W | 1 | 33,90 | 33,90 | [S16], revisar stock y curvas eléctricas. |
| B09 | SEN0604 suelo/pH/EC | 1 | 69,00 | 69,00 | [S2], cualificación agronómica. |
| B10 | SEN0605 NPK | 1 | 59,00 | 59,00 | [S3], contraste con laboratorio. |
| B11 | SHT31-D Adafruit 2857, aire | 1 | 13,95 | 13,95 | [S5], protección/abrigo aparte. |
| B12 | SEN0600 contacto de secado, candidato | 1 | 29,00 | 29,00 | [S4], **precio de candidato, no aprobación como medidor de café**. |
| R01 | Gabinete IP67, membrana y prensaestopas | 1 juego | 35,00 | 35,00 | Reserva de ingeniería; falta cotización exacta del conjunto. |
| R02 | Soporte/poste y fijaciones | 1 juego | 25,00 | 25,00 | Reserva de ingeniería. |
| R03 | Abrigo ventilado para aire | 1 | 15,00 | 15,00 | Reserva de ingeniería. |
| R04 | Cable protegido, conectores, MOSFET, TVS, fusibles, NTC y montaje | 1 juego | 35,00 | 35,00 | Reserva de ingeniería; incluye protección térmica y conmutación. |
| R05 | Antena celular/conectores y SIM física | 1 juego | 20,00 | 20,00 | Reserva; descontar antena si está incluida en B01. Servicio de datos no incluido. |
| R06 | Respaldo RTC y consumibles | 1 juego | 2,00 | 2,00 | Reserva de ingeniería. |
| **Total de precios observados B01–B12** | | | | **487,74** | Antes de costos excluidos. |
| **Total de reservas R01–R06** | | | | **132,00** | No son cotizaciones comerciales. |
| **Presupuesto preliminar compartido** | | | | **619,74** | Solo válido si se cualifica B12 y la integración elegida. |

Si B12 falla, no se mantiene artificialmente el total: se solicita oferta de una sonda apta para café y se recalculan BOM, energía, montaje y horas. [S14] no publica un precio verificable; no se le asigna uno inventado. Calibración/laboratorio y herramientas compartidas se presupuestan aparte; el conversor de campo FIT0832 tiene referencia de USD 16,90 [S17], sin convertirlo en hardware fijo por finca.

### 7.2 Incremento del perfil satelital

| Cambio sobre el conjunto anterior | Cantidad | Incremento USD | Fuente / condición |
|---|---:|---:|---|
| RockBLOCK 9603, variante patch integrada | 1 | 302,00 | [S9], confirmar variante/stock y vista al cielo dentro de protección RF. |
| Cable tails RockBLOCK 9603 | 1 | 17,00 | [S9]. |
| Segundo panel HY015-12P | 1 | 33,90 | [S16]; total solar 30 W, conexión paralela verificada. |
| Sustituir BLF-1206A por BLF-1212A | 1 | 45,00 | USD 124,99 − 79,99, [S15]. |
| Arnés/control de encendido y fijación adicional | 1 juego | 15,00 | Reserva de ingeniería. |
| **Incremento preliminar** | | **412,90** | No incluye activación ni mensualidad. |
| **Conjunto compartido satelital preliminar** | | **1032,64** | Sujeto a las mismas condiciones de medición y montaje. |

Se conserva B01 como controlador de referencia con su módem celular apagado; sustituirlo por una placa ESP32 sin módem puede reducir costo solo después de comprobar el resto de interfaces y recotizar. No se resta un ahorro sin compra alternativa identificada. Una antena externa SMA, si la ubicación la exige, requiere cotización adicional y no está incluida en el total patch.

### 7.3 Cómo alimentar #28/#29 sin inventar el tamaño del piloto

El precio anterior es de **un conjunto C+S compartido**, no de cualquier finca. Para conjuntos separados se cotiza la base autónoma por controlador y el sensor correspondiente; no basta con sumar otra sonda. Los instrumentos de referencia y la cualificación de lote son costos compartidos identificables, no un supuesto costo cero.

`CapEx = Σ(unidades por perfil × BOM aceptada) + repuestos + cualificación + instalación + logística + impuestos`.

200 fincas tienen zona de secado aunque solo unas 100 estén activas simultáneamente en cosecha; esa concurrencia no demuestra que solo se compren 100 sondas. #28 debe contar controladores físicos, puntos S y `N_sat` reales, sin multiplicar automáticamente el precio compartido por 200 ni duplicar ambos escenarios.

El costo verificado es mayor que el borrador incompleto; no se sostiene su ahorro del 80 % ni su total por finca. Se conserva hardware de microcontrolador y se evita equipamiento fijo adicional cuando el cableado lo permite. El controlador MPPT es una referencia conservadora de bajo autoconsumo; una alternativa más barata requiere la misma compatibilidad de batería y consumo comprobado, no el cambio a un PWM sin recalcular energía.

El servicio satelital sigue siendo una excepción económicamente condicionada de #6: allí se presupuestó USD 147/mes para el escenario con secado según la referencia contractual examinada, no como tarifa garantizada por esta HU. A 30 registros/día, 200 bytes MO y 50 MT, serían 225.000 bytes/mes antes de reintentos. El máximo energético de 128 ventanas no equivale a una cuota incluida: si todas repitieran tráfico facturable, `128 × 250 × 30 = 960.000 bytes/mes`, sujeto a reglas reales de facturación. #28/#29 deben añadir sobreconsumo y financiación; no se oculta con un tope de energía ni se suspende silenciosamente la telemetría para abaratar la cuenta.

## 8. Validación y aceptación

| Criterio de #11 | Evidencia de diseño | Prueba que falta antes de instalación/compra de lote |
|---|---|---|
| Todas las variables C/S de la tabla | Matriz de sección 2, con aire, suelo, N/P/K, pH y humedad/temperatura del grano separados. | Cualificar exactitud y especialmente B12 en café; si falla, sustituirlo. No se declara cumplida metrología solo por haber campos. |
| Días nublados con panel/batería | Balance explícito, márgenes, perfiles C/S y celular/satelital, tres días a 0,5 HSP. | Medir nodo completo, picos y autoconsumo, descarga y recuperación. Confirmar recurso solar y perfil de carga. |
| Una visita con equipo descrito | Preparación previa, kit, herramientas y objetivo de 4 h 30 min para conjunto compartido. | Ensayar montaje y enlace; confirmar emplazamiento y duración para dos conjuntos. |
| Qué ocurre a las 24 h | Expiración por edad, metadato de incidente y conciliación de ACK; sin histórico alternativo. | Ensayo de 24 h, reinicio, corte durante escritura, reloj inválido y ACK tardío. |

El banco mínimo cubre 72 h con secado activo y aporte solar simulado, más escenario de radio fallida hasta 128 ventanas/día, medición de Wh y prueba de recuperación. Se exige registro de revisión de placa, firmware, sensores, calibración, batería, panel y condiciones. Las pruebas de certificado abarcan identidad propia, tema ajeno y revocación; SBD añade rechazo de identidad dada de baja y repetición. Ninguna de estas pruebas físicas se ha ejecutado en esta entrega.

La revisión documental comprueba las 10 variables de la matriz, 6+24 registros/día, 24 h de retención, cálculos dimensionales, sumas de BOM y distinción entre precio público/reserva. El módulo de finca de IaC recibirá identidad pública y parámetros del perfil; no contendrá claves privadas, secretos simétricos de SBD ni firmware. #12 concreta ingesta, ACK y entrega de alerta <5 minutos con ruta disponible; #18 mide incumplimientos. El diseño de nodo no acredita por sí solo ese SLA de extremo a extremo.

## 9. Fuentes consultadas

Precios y fichas consultados el **7 de noviembre de 2026**. Los fabricantes describen capacidades de producto; los márgenes, tiempos, pruebas y límites de diseño son propuestas de esta HU.

- **[S1] LilyGO:** [T-SIM7080G-S3, precio/versión](https://lilygo.cc/products/t-sim7080-s3), [comparación por revisión](https://wiki.lilygo.cc/products/t-sim-series/sim.html) y [repositorio oficial de placa](https://github.com/Xinyuan-LilyGO/LilyGo-T-SIM7080G).
- **[S2] DFRobot:** [SEN0604, suelo/pH/EC](https://www.dfrobot.com/product-2830.html).
- **[S3] DFRobot:** [SEN0605, NPK](https://www.dfrobot.com/product-2819.html).
- **[S4] DFRobot:** [SEN0600, humedad/temperatura de suelo](https://www.dfrobot.com/product-2816.html). No aporta curva de café validada.
- **[S5] Adafruit:** [SHT31-D 2857](https://www.adafruit.com/product/2857).
- **[S6] DFRobot:** [DFR0845 RS485 aislado](https://www.dfrobot.com/product-2392.html).
- **[S7] Adafruit:** [ATECC608 4314](https://www.adafruit.com/product/4314).
- **[S8] Adafruit:** [DS3231 3013](https://www.adafruit.com/product/3013).
- **[S9] Ground Control:** [RockBLOCK 9603 y accesorios](https://store.groundcontrol.com/products/rockblock-9603), [alimentación](https://docs.groundcontrol.com/iot/rockblock/electrical/power-supply) y [variantes](https://docs.groundcontrol.com/iot/rockblock/product-variants).
- **[S10] Pololu:** [D24V22F5](https://www.pololu.com/product/2858).
- **[S11] Sunforge:** [Genasun GV-5 y variantes de batería](https://sunforgellc.com/product/gv-5/).
- **[S12] AWS:** [certificado desde CSR](https://docs.aws.amazon.com/cli/latest/reference/iot/create-certificate-from-csr.html). [Espressif ESP-TLS](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/protocols/esp_tls.html) para contrastar la integración de seguridad seleccionada.
- **[S13] Cenicafé:** [Método Gravimet, Avance Técnico 387](https://publicaciones.cenicafe.org/index.php/avances_tecnicos/article/view/1643). Sustenta humedad de café en base húmeda y referencia gravimétrica; no certifica la sonda propuesta.
- **[S14] Mysentech:** [GMS1081-C-CER-AL3.0, sensor de granos](https://www.mysentech.com/productinfo/3588342.html), alternativa con curvas configurables; precio y curva de café por confirmar.
- **[S15] Bioenno:** [BLF-1206A, batería sola](https://www.bioennopower.com/products/12v-6ah-lifepo4-battery-pvc) y [BLF-1212A](https://www.bioennopower.com/products/12volt-12ah-lifepo4-battery).
- **[S16] ACOPOWER:** [HY015-12P, panel 15 W](https://www.acopower.com/products/hy015-12p).
- **[S17] DFRobot:** [FIT0832, herramienta USB-RS485 de campo](https://www.dfrobot.com/product-2383.html).
