# Costo del hardware de una finca y del piloto

## Qué responde este documento

El caficultor necesita saber dos cosas antes de entrar al piloto: cuánto cuesta el equipo que se instala en su finca y cuánto se paga al mes por mantenerlo conectado. Este documento lo calcula para una finca con cobertura celular y para una sin cobertura, y suma el total de las 200 fincas del piloto.

Parte de la lista de materiales de la [#11](../architecture/carga-a-nodo-finca.md) y de los perfiles de conectividad de la [#6](../architecture/conectividad-sin-senal.md). Los precios de 2020 no se usan. La plataforma en la nube (IoT Core, base, funciones) no entra aquí: va en la [#29](https://github.com/aromapacifico-platform/planning/issues/29).

**Tasa de cambio:** TRM de COP 3.237,83 por dólar, vigente del 7 al 9 de noviembre de 2026 ([dolar-colombia.com](https://www.dolar-colombia.com/2026-11-06)). Los precios se cotizan en dólares y se convierten al final.

## 1. Conjunto de una finca con cobertura celular

Un solo controlador atiende el nodo de cultivo y el de secado (conjunto compartido de la #11). Usa LTE-M o NB-IoT, sin 2G ni 3G.

| ID | Ítem | USD | Fuente | Fecha |
| --- | --- | ---: | --- | --- |
| B01 | LilyGO T-SIM7080G-S3 (ESP32-S3 con módem LTE-M/NB-IoT, incluye antenas LTE y GPS) | 29,60 | [LilyGO](https://lilygo.cc/products/t-sim7080-s3); antenas en la [lista de empaque](https://grobotronics.com/lilygo-esp32-s3-t-sim7080g-s3-4g-lte-cat-4-and-gnss.html?sl=en) | 7 nov 2026 |
| B02 | DFRobot DFR0845, RS485 aislado | 19,90 | [DFRobot](https://www.dfrobot.com/product-2392.html) | 7 nov 2026 |
| B03 | Adafruit 4314, ATECC608 (llave del certificado) | 4,95 | [Adafruit](https://www.adafruit.com/product/4314) | 7 nov 2026 |
| B04 | Adafruit 3013, reloj DS3231 | 17,50 | [Adafruit](https://www.adafruit.com/product/3013) | 7 nov 2026 |
| B05 | Pololu D24V22F5, regulador de 5 V | 26,95 | [Pololu](https://www.pololu.com/product/2858) | 7 nov 2026 |
| B06 | Genasun GV-5-Li-14.2V, controlador solar para LiFePO4 | 104,00 | [Sunforge](https://sunforgellc.com/product/gv-5/) | 7 nov 2026 |
| B07 | Bioenno BLF-1206A, batería LiFePO4 de 12 V y 6 Ah | 79,99 | [Bioenno](https://www.bioennopower.com/products/12v-6ah-lifepo4-battery-pvc) | 7 nov 2026 |
| B08 | ACOPOWER HY015-12P, panel de 15 W | 33,90 | [ACOPOWER](https://www.acopower.com/products/hy015-12p) | 7 nov 2026 |
| B09 | DFRobot SEN0604, suelo, pH y conductividad | 69,00 | [DFRobot](https://www.dfrobot.com/product-2830.html) | 7 nov 2026 |
| B10 | DFRobot SEN0605, N, P y K | 59,00 | [DFRobot](https://www.dfrobot.com/product-2819.html) | 7 nov 2026 |
| B11 | Adafruit 2857, SHT31-D para el aire | 13,95 | [Adafruit](https://www.adafruit.com/product/2857) | 7 nov 2026 |
| B12 | DFRobot SEN0600, humedad y temperatura del grano (candidato, sin cualificar en café) | 29,00 | [DFRobot](https://www.dfrobot.com/product-2816.html) | 7 nov 2026 |
| | **Subtotal cotizado** | **487,74** | | |
| R01 | Gabinete IP67 con membrana y prensaestopas | 35,00 | Reserva de ingeniería | — |
| R02 | Poste y fijaciones | 25,00 | Reserva de ingeniería | — |
| R03 | Abrigo ventilado para el sensor de aire | 15,00 | Reserva de ingeniería | — |
| R04 | Cable, conectores, MOSFET, TVS, fusibles y NTC | 35,00 | Reserva de ingeniería | — |
| R06 | Respaldo del reloj y consumibles | 2,00 | Reserva de ingeniería | — |
| | **Subtotal de reservas** | **112,00** | | |
| | **Conjunto con cobertura, precio de lista** | **599,74** | | |

La #11 tenía una reserva R05 de USD 20 para antena y SIM. Se quita: la placa ya trae la antena LTE, y la SIM se cuenta en la conectividad de la sección 4.

**Las cinco reservas no son cotizaciones.** Suman USD 112, el 19 % del conjunto, y son las únicas líneas sin fuente. Se reemplazan por la cotización de un integrador antes de la compra. Como referencia de que la reserva del gabinete es razonable, un gabinete de policarbonato de la serie PN-1324 de Bud Industries aparece entre USD 19 y 24 en distribuidores ([element14](https://au.element14.com/bud-industries/pn-1324-c/enclosure-junction-box-polycarbonate/dp/2053573), [TestEquity](https://www.testequity.com/product/10013884-PN-1324-C)), pero ese modelo es IP65/IP66, no IP67.

## 2. Incremento de una finca sin cobertura

La finca que no pasa la validación de LTE-M o NB-IoT usa el canal satelital Iridium SBD de la #6. Se suma al conjunto anterior:

| Ítem | USD | Fuente | Fecha |
| --- | ---: | --- | --- |
| RockBLOCK 9603 con antena integrada | 302,00 | [Ground Control](https://store.groundcontrol.com/products/rockblock-9603) | 7 nov 2026 |
| Cables del RockBLOCK 9603 | 17,00 | [Ground Control](https://store.groundcontrol.com/products/rockblock-9603) | 7 nov 2026 |
| Segundo panel HY015-12P (30 W en total) | 33,90 | [ACOPOWER](https://www.acopower.com/products/hy015-12p) | 7 nov 2026 |
| Cambio a batería BLF-1212A de 12 Ah (USD 124,99 − 79,99) | 45,00 | [Bioenno](https://www.bioennopower.com/products/12volt-12ah-lifepo4-battery) | 7 nov 2026 |
| Arnés y control de encendido del módem | 15,00 | Reserva de ingeniería | — |
| **Incremento** | **412,90** | | |
| **Conjunto sin cobertura, precio de lista** | **1.012,64** | | |

## 3. Del precio de lista al costo puesto en la finca

Los precios de lista son de tiendas en Estados Unidos y China. Para llegar a la finca se suman tres cosas:

- **Logística e importación: 10 %** sobre el precio de lista, para envío, agenciamiento y arancel. Es un supuesto; se reemplaza por la oferta del integrador.
- **IVA de importación: 19 %** sobre el valor con logística.
- **Instalación: COP 350.000 por finca (USD 108,10).** Es una jornada de técnico con transporte rural, y cabe en la visita única de 4 h 30 min que diseñó la #11. Es un supuesto de tarifa, no una cotización.

| | Con cobertura | Sin cobertura |
| --- | ---: | ---: |
| Precio de lista | USD 599,74 | USD 1.012,64 |
| Con logística (× 1,10) e IVA (× 1,19) | USD 785,06 | USD 1.325,55 |
| Instalación | USD 108,10 | USD 108,10 |
| **Costo puesto en la finca** | **USD 893,16** | **USD 1.433,64** |
| En pesos | **COP 2.891.890** | **COP 4.641.892** |

El borrador junior estimaba unos USD 145 por nodo. No se sostiene: solo la batería, el controlador solar y las dos sondas de suelo ya suman USD 312. Esos USD 145 cubrían el microcontrolador y los sensores, sin energía, gabinete, importación ni instalación.

## 4. Cuota mensual de conectividad por finca

### Finca con cobertura

Se toma como referencia la SIM IoT de 1NCE ([precios](https://1nce.com/en-us/1nce-connect/pricing), consulta del 8 de noviembre de 2026):
- **Plan:** USD 14 de pago único por 10 años, con 500 MB y 250 SMS.
- **SIM:** USD 1.
- **Recarga:** USD 10 por otros 500 MB.

Una finca con cultivo y secado activos abre hasta 30 sesiones al día. Con unos 7 KB por sesión (handshake TLS, publicación y ACK), son unos 6,3 MB al mes. Si se duplica por reintentos, los 500 MB duran algo más de 3 años. En 10 años hacen falta unas dos recargas:

`(14 + 1 + 2 × 10) / 120 meses = USD 0,29 al mes`

**Cuota con cobertura: USD 0,30 al mes, unos COP 971.**

Falta confirmar la cobertura de 1NCE en Colombia: su documentación no lista países ([cobertura](https://help.1nce.com/docs/connectivity-services/connectivity-services-mobile-network-services/mobile-network-services-coverage.md)). Movistar Colombia aparece con LTE-M en servicio en otro proveedor IoT ([Onomondo](https://onomondo.com/es/coverage/lte-m/)). Si 1NCE no sirve, se cotiza un plan M2M local con Movistar. Aunque costara diez veces más, seguiría por debajo de USD 3 al mes.

### Finca sin cobertura

Se usan las tarifas de Iridium SBD que fijó la #6 ([Ground Control](https://www.groundcontrol.com/products/iridium/short-burst-data-range/short-burst-data-service-plans/)):

| Perfil | Datos al mes | Plan | Cuota |
| --- | ---: | --- | ---: |
| Cultivo y secado | 225.000 bytes | 250.000 bytes | **USD 147, unos COP 475.961** |
| Solo cultivo | 45.000 bytes | 25.000 bytes con excedente | USD 70,35, unos COP 227.781 |

La activación cuesta USD 31,50 por terminal. Como en la #6, se presupuestan USD 147 todos los meses del contrato, porque el terminal no cambia de plan entre cosecha y fuera de cosecha.

## 5. Total del piloto

### Cuántas fincas quedan sin cobertura

Nadie ha medido todavía cuántas de las 200 fincas tienen LTE-M o NB-IoT. El enunciado dice que el caficultor tiene datos en la cabecera municipal o en la vía principal, lo que sugiere que muchas fincas no los tienen. Para no quedarse corto, el escenario base supone **60 fincas sin cobertura (30 %)**. El número real sale de la preinspección por operador y sitio de la #6.

### Total en el escenario base: 140 con cobertura y 60 sin cobertura

| Concepto | Cálculo | USD |
| --- | --- | ---: |
| Fincas con cobertura | 140 × 893,16 | 125.042,40 |
| Fincas sin cobertura | 60 × 1.433,64 | 86.018,40 |
| Repuestos | 5 % del equipo importado | 9.472,05 |
| Conversores RS485 de campo, uno por acopio ([DFRobot FIT0832](https://www.dfrobot.com/product-2383.html)) | 3 × 16,90 | 50,70 |
| Activación satelital | 60 × 31,50 | 1.890,00 |
| **Inversión inicial del piloto** | | **USD 222.473,55** |
| En pesos | | **COP 720.331.534** |
| **Cuota mensual de conectividad del piloto** | 140 × 0,30 + 60 × 147 | **USD 8.862 al mes** |
| En pesos | | **COP 28.693.649 al mes** |

### Sensibilidad al número de fincas sin cobertura

| Fincas sin cobertura | Inversión inicial | Cuota mensual del piloto |
| ---: | ---: | ---: |
| 30 (15 %) | USD 204.502,96 | USD 4.461 |
| **60 (30 %)** | **USD 222.473,55** | **USD 8.862** |
| 100 (50 %) | USD 246.433,69 | USD 14.730 |

**Lo que dice este resultado:** la inversión crece poco con las fincas sin cobertura, pero la cuota mensual crece casi en proporción, porque cada terminal satelital cuesta USD 147 al mes frente a USD 0,30 de uno celular. Con 60 fincas, el satélite es más del 99 % de la cuota del piloto. Es el primer gasto que debe atacar la [#31](https://github.com/aromapacifico-platform/planning/issues/31). Por ejemplo, la #6 dejó abierta la opción de un enlace de largo alcance hasta un punto con señal, compartido entre fincas vecinas.

## 6. Cuánto paga una finca

| | Con cobertura | Sin cobertura |
| --- | ---: | ---: |
| Equipo puesto en la finca, una vez | COP 2.891.890 | COP 4.641.892 |
| Conectividad, cada mes | COP 971 | COP 475.961 |

El enunciado pide que el caficultor invierta poco. Este documento no decide quién paga: si la Federación financia el equipo, si se cobra una cuota o si el satélite se subsidia. Esa decisión sale en la #31 con el costo consolidado. Lo que sí deja claro es que con cobertura la cuota es casi nula, y sin cobertura el satélite, tal como está, no es viable para un caficultor.

## 7. Verificación de los criterios de la #28

| Criterio | Dónde se cumple |
| --- | --- |
| Cada ítem tiene precio, fuente y fecha de la cotización | Secciones 1 y 2. Las seis reservas de ingeniería, que suman USD 127 por finca, están marcadas como no cotizadas y se reemplazan antes de la compra |
| Se separa el costo de una finca con cobertura y de una fuera de cobertura | Secciones 1 a 3 y 6 |
| Se muestra la cuota mensual por finca | Secciones 4 y 6 |
