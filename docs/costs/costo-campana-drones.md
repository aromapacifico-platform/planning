# Costo de la campaña de drones

## Qué responde este documento

El reto no pide comprar ni operar drones, pero sí costear la campaña. Este documento calcula cuánto cuestan al año y en cada tipo de mes los cinco servicios de dron, compara **comprar el equipo y tener cuadrillas propias** contra **contratar el servicio**, y elige.

Los vuelos salen del [servicio de drones](../architecture/carga-b-servicio-drones.md) (#13). La inferencia sale del [documento de inferencia](../architecture/carga-e-inferencia-administrada.md) (#17).

**Tasa de cambio:** TRM de COP 3.237,83 por dólar, vigente del 7 al 9 de noviembre de 2026 ([dolar-colombia.com](https://www.dolar-colombia.com/2026-11-06)).

## 1. Vuelos que se costean

Son los mismos de la #13, sin cambios:

| Servicio | Al año | Mes pico de cosecha | Mes fuera de cosecha con campaña | Mes fuera de cosecha sin campaña |
| --- | ---: | ---: | ---: | ---: |
| S1 Delimitar el lote (solo el año 1) | 200 | 0 | 0 | 0 |
| S2 Confirmar la alerta | 280 | 40 | 20 | ~7 |
| S3 Fumigar | 210 | 30 | 15 | ~5 |
| S4 Verificar la fumigación | 210 | 30 | 15 | ~5 |
| S5 Estimar la cosecha | 400 | ~67 | 0 | 0 |
| **Total** | **1.300** | **~167** | **50** | **~17** |

Para pasar de vuelos a hectáreas hacen falta dos datos más:

- **Tamaño de una finca: 2 hectáreas en promedio.** El enunciado no lo da. Es un supuesto de minifundio cafetero que se reemplaza por el área real cuando se haga la delimitación (S1).
- **Área de un foco fumigado: 0,2 a 0,5 hectáreas**, según la #13. Como un servicio contratado cobra por lo menos una hectárea por visita, se cuenta una hectárea por fumigación.

| Servicio | Unidad que se cobra | Cantidad al año |
| --- | --- | ---: |
| S1 y S5 | Hectáreas mapeadas | 400 (año 1) + 800 |
| S2 y S4 | Visitas puntuales con foto | 490 |
| S3 | Hectáreas fumigadas | 210 |

## 2. Opción A: contratar el servicio

Se contrata un prestador por cada acopio, que vuela con las reglas de la plataforma:
- Entra a la app con su identidad de operador de drones en Cognito, con MFA.
- Solo vuela misiones precargadas con el token de 48 horas.
- Sube la bitácora y las fotos por el mismo camino.

La autorización de cada fumigación sigue siendo exclusiva del agrónomo de la Federación.

| Concepto | Tarifa | Fuente | Al año |
| --- | --- | --- | ---: |
| Mapeo de S1 y S5 | COP 100.000 por hectárea | Rango de COP 80.000 a 150.000 por hectárea para ortomosaico en zona rural ([Geosat](https://geosat.com.co/es/blog/fotogrametria-drones-precios-colombia), 26 de mayo de 2026). Se toma un valor medio porque cada campaña junta unas 67 fincas, unas 134 hectáreas | COP 80.000.000 (+ COP 40.000.000 el año 1) |
| Fumigación S3 | COP 70.000 por hectárea | Aspersión con dron, entre COP 60.000 y 70.000 por hectárea, mapeo incluido ([Contexto Ganadero](https://www.contextoganadero.com/regiones/agrodron-integra-mapeo-y-aspersion-con-drones-en-un-solo-servicio), agosto de 2024) | COP 14.700.000 |
| Visitas de S2 y S4 | COP 250.000 por visita | **Supuesto.** No hay tarifa pública de una visita corta con foto. Cubre desplazamiento rural, piloto y equipo | COP 122.500.000 |
| **Total al año** | | | **COP 217.200.000 (USD 67.082)** |
| **Total del año 1, con la delimitación** | | | **COP 257.200.000 (USD 79.436)** |

La tarifa de fumigación es de 2024; con la inflación puede haber subido un 10 %, pero pesa poco en el total. Lo que más pesa son las visitas de S2 y S4, que son un supuesto. Por eso es la primera cifra que hay que cotizar.

**Por mes:**

| Mes | Cálculo | Costo |
| --- | --- | ---: |
| Pico de cosecha | 70 visitas + 30 ha fumigadas + 134 ha mapeadas | COP 33.000.000 (USD 10.192) |
| Fuera de cosecha con campaña | 35 visitas + 15 ha fumigadas | COP 9.800.000 (USD 3.027) |
| Fuera de cosecha sin campaña | ~12 visitas + 5 ha fumigadas | COP 3.275.000 (USD 1.011) |

## 3. Opción B: comprar el equipo y tener cuadrillas propias

Es el modelo de la #13: una cuadrilla por acopio, con un piloto y un auxiliar, un vehículo, un generador y los drones.

**Equipo por cuadrilla:**

| Ítem | USD | Fuente |
| --- | ---: | --- |
| DJI Agras T50, kit listo para volar con 2 baterías y cargador | 24.662 | [Grabarobot, guía de precios 2026](https://grabarobot.com/blog/dji-agras-t50-price-guide-2026/) |
| DJI Mavic 3 Multispectral, para mapeo y fotos de foco | 5.400 | Rango de USD 4.600 a 5.700 en distribuidores ([Dronefly](https://www.dronefly.com/products/dji-mavic-3m)) |
| Generador para carga en campo | 1.500 | Reserva, sin cotización |
| Dos baterías adicionales del T50 | 3.600 | Reserva, sin cotización |
| **Total por cuadrilla** | **35.162** | |
| **Tres cuadrillas** | **105.486** | |

**Costo al año:**

| Concepto | Supuesto | COP al año |
| --- | --- | ---: |
| Piloto certificado | COP 4.800.000 al mes, de ofertas de empleo en Colombia ([CazVid](https://cazvid.com/empleo/piloto-de-drone-en-bogota-colombia)), con 52 % de carga prestacional | 262.656.000 |
| Auxiliar de carga y mezcla | COP 2.800.000 al mes con 52 % de carga prestacional. Supuesto | 153.216.000 |
| Vehículo todo terreno en renting | COP 5.500.000 al mes por cuadrilla. Supuesto | 198.000.000 |
| Combustible y viáticos | COP 80.000 por vuelo × 1.300 vuelos. Supuesto | 104.000.000 |
| Póliza de responsabilidad civil y trámites RAC 100 | COP 6.000.000 por cuadrilla. Supuesto | 18.000.000 |
| Depreciación del equipo a 3 años | USD 105.486 / 3 | 113.848.578 |
| **Total al año** | | **COP 849.720.578 (USD 262.435)** |

## 4. Comparación y decisión

| | Contratar | Comprar |
| --- | ---: | ---: |
| Costo al año | **USD 67.082** | USD 262.435 |
| Costo por vuelo | **COP 167.077** | COP 653.631 |
| Inversión inicial | 0 | USD 105.486 |
| Riesgo de equipo ocioso fuera de cosecha | Del prestador | De la Federación |

**Se elige contratar el servicio.** Comprar cuesta casi cuatro veces más. La razón es que el piloto vuela poco: 1.300 vuelos al año, la mayoría cortos y concentrados en seis meses. Con cuadrillas propias se pagan todo el año el personal y los vehículos, que son el 72 % del costo, aunque en los meses sin campaña haya unos 17 vuelos.

La decisión aguanta los supuestos:
- Si el mapeo se cobra como proyecto pequeño, a COP 300.000 por hectárea, contratar sube a USD 116.498 al año y sigue costando menos de la mitad que comprar.
- Para que comprar empate, cada visita de S2 y S4 tendría que costar más de COP 1,4 millones.

**Qué no se pierde al contratar.** Los controles de la #13 y la #14 no dependen de quién es dueño del dron, sino de la plataforma:
- La identidad del operador con MFA.
- La misión precargada con token, polígono y zonas de no vuelo.
- La bitácora con hash.
- La foto de verificación para cerrar.
- La autorización del agrónomo.

El contrato exige además la certificación RAC 100 en categoría específica, el registro ICA de aplicador y la póliza de responsabilidad civil.

**Qué cambia frente a la #13.** La #13 proponía cuadrillas de la Federación por acopio. El modelo operativo se mantiene: un equipo por acopio con las mismas reglas. Lo que cambia es que ese equipo es de un prestador contratado. Esta es una de las decisiones que bajan gasto de la [#31](https://github.com/aromapacifico-platform/planning/issues/31).

## 5. Almacenamiento de ortomosaicos y fotos

Cada vuelo de S1 o S5 sobre una finca de 2 hectáreas deja unos **2 GB de fotos y 0,5 GB de ortomosaico**. Cada visita de S2 o S4 deja unas 20 fotos de 8 MB. Son supuestos que se ajustan con los primeros vuelos.

| | GB al año |
| --- | ---: |
| S1 y S5 (600 vuelos en el año 1) | 1.500 |
| S2 y S4 (490 visitas) | 78 |
| **Total** | **~1.580** |

Se conservan 5 años. Una regla de ciclo de vida los deja 30 días en S3 Standard, los pasa a Standard-IA hasta cumplir un año y luego a Glacier Deep Archive. Precios de lista de `us-east-1` ([S3](https://aws.amazon.com/s3/pricing/)):

| Momento | Standard (USD 0,023/GB) | Standard-IA (USD 0,0125/GB) | Deep Archive (USD 0,00099/GB) | Total al mes |
| --- | ---: | ---: | ---: | ---: |
| Año 1, en promedio | ~130 GB | ~650 GB | 0 | **USD 11** |
| Año 5 | ~130 GB | ~1.450 GB | ~6.300 GB | **USD 27** |

La réplica en `us-east-2` que pide la #15 se suma en el costo de la plataforma (#29).

## 6. Inferencia

Sale de la #17: unos USD 3,11 por cada 1.000 imágenes en el escenario conservador, incluyendo el filtro de personas con Rekognition, el diagnóstico con Bedrock, Lambda, S3 y KMS.

| | Imágenes | Costo |
| --- | ---: | ---: |
| Semestre de cosecha | 620 | USD 1,93 |
| Semestre fuera de cosecha | 70 | USD 0,22 |
| **Año** | **690** | **USD 2,15** |

La #17 cuenta una imagen por misión. Si se mandan a inferencia las 20 fotos de cada visita, el año sube a unos USD 43. En los dos casos la inferencia es despreciable frente al vuelo.

## 7. Resumen

| Concepto | Año 1 | Años siguientes |
| --- | ---: | ---: |
| Servicio de drones contratado | USD 79.436 | USD 67.082 |
| Almacenamiento de objetos | ~USD 130 | Hasta ~USD 325 en el año 5 |
| Inferencia | ~USD 2 a 43 | ~USD 2 a 43 |
| **Total de la campaña** | **~USD 79.600** | **~USD 67.400** |

En pesos son unos **COP 258 millones el año 1** y **COP 218 millones al año** después.

## 8. Verificación de los criterios de la #30

| Criterio | Dónde se cumple |
| --- | --- |
| El número de vuelos coincide con el documento de drones | Sección 1: 1.300 vuelos al año y 167 en el mes pico, iguales a la #13 |
| Se compara comprar contra contratar y se elige con razón | Secciones 2 a 4 |
