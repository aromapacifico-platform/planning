# Patrón de red del centro de acopio

**Historia:** [#8](https://github.com/aromapacifico-platform/planning/issues/8) · **Responsable:** Juan Ocampo (`juandavid175`) · **Fecha:** 6 de noviembre de 2026.  
**Estado:** diseño para revisión; no representa equipos instalados ni pruebas de red ejecutadas.

## 1. Base revisada y alcance

Se diseña un único centro patrón para recepción, aceptación/rechazo, despacho e impresión de códigos de sacos de 60 kg. Cauca usa `10.41.0.0/16`; Huila y Tolima reutilizan el mismo patrón sustituyendo el segundo octeto por 42 y 43. No se construyen tres diseños independientes.

La base integrada consultada es `planning/main`, commit `4c6fa27a31a5ac5c38c0da5711e36936024ba2cd`: [enunciado](../case-study/enunciado-original.md), [direccionamiento y rutas](red-direccionamiento-nube.md), [gobierno](gobierno-landing-zone.md) y [orden del dron](carga-b-orden-fumigacion.md). Se conservan AWS `us-east-1`, Transit Gateway centralizado, los CIDR de nube y el uso de VLAN Logística por las cuadrillas de drones.

La dependencia #6 está presentada en la [PR #49](https://github.com/aromapacifico-platform/planning/pull/49), commit `dd05724707f35217dcb09832066cad2940350c51`, aún sin integrar al consultar. Se tomó de allí la cola persistente de operaciones en puestos de logística, el spooler local y la sincronización posterior. Esta propuesta puede revisarse mientras se revisa #49; la dependencia no se declara cerrada.

También se consultaron las propuestas de identidades [PR #50](https://github.com/aromapacifico-platform/planning/pull/50) y de saco/viaje [PR #52](https://github.com/aromapacifico-platform/planning/pull/52). Siguen en revisión. Para evitar trasladar contradicciones de esos borradores, se conserva la identidad de aplicación **Cognito con MFA** del gobierno integrado; IAM Identity Center se reserva a la administración cloud. No se incorpora 3G ni se modifica el ciclo de vida del saco desde esta historia.

La entrega se limita a este documento y un diagrama con fuente editable. Las decisiones nuevas se enumeran en la sección 10, sin modificar archivos de otras historias ni presentar aplicaciones, firmware o infraestructura como implementados.

## 2. Inventario y direccionamiento del patrón

`X` representa el segundo octeto del departamento. El gateway de cada VLAN de usuarios o servidores es `10.X.Z.1/24`, donde `Z` es el tercer octeto. Los identificadores de VLAN se conservan en los tres sitios y no se confunden con el número de departamento.

| Zona | VLAN propuesta | Red | Clientes del caso | SSID del patrón | Acceso |
|---|---:|---|---:|---|---|
| Gerencia | 101 | `10.X.1.0/24` | 2 escritorios + 5 teléfonos = **7** | `AP-X-Gerencia` | Escritorios cableados y teléfonos con wifi. |
| Soporte | 102 | `10.X.2.0/24` | 2 escritorios + 5 teléfonos = **7** | `AP-X-Soporte` | Uso de oficina; administrar equipos exige autorización adicional. |
| Logística | 103 | `10.X.3.0/24` | 2 escritorios + 20 teléfonos = **22** | `AP-X-Logistica` | Recepción, despacho y estaciones registradas de cuadrillas. |
| Transporte | 104 | `10.X.4.0/24` | **20 teléfonos** | `AP-X-Transporte` | Aplicación del conductor y sincronización por API. |
| Visitantes | 105 | `10.X.5.0/24` | **10 teléfonos** | `AP-X-Visitantes` | Solo internet filtrado; sin acceso a redes internas ni VPN. |
| Servidores y gestión de red | 110 | `10.X.10.0/24` | Dimensionamiento de esta propuesta | **Sin SSID** | Conexión cableada; aloja servicios y gestión, no clientes móviles. |
| Borde / enlace a nube | 120 | `10.X.20.0/24` | Firewall del centro | **Sin SSID** | Tránsito cableado entre firewall y CPE del proveedor. |

Hay **66 clientes de usuario por acopio: 6 escritorios y 60 teléfonos**. El total no incluye impresora, servidores, AP, switch ni nuevas estaciones de drones. Los equipos adicionales se inventarían y admitirían antes de conectarlos; no se presupone capacidad ilimitada.

Las siete VLAN corresponden a las siete zonas del inventario. Los cinco SSID se asignan a las zonas que realmente tienen usuarios inalámbricos; no se crea una WLAN para servidores ni para tránsito WAN. Un SSID es el nombre de una red, no un AP físico: un mismo AP puede atender varias zonas mediante VLAN.

Propuesta de direcciones de usuario: gateway `.1`; reservas de escritorios/dispositivos `.20–.49`; DHCP `.50–.199`; resto reservado. Se documenta cada reserva para evitar que coincida con el pool. DHCP no se habilita en VLAN 120. Se bloquean servidores DHCP no autorizados cuando el switch lo soporte.

### Sustitución por departamento

| Elemento | Cauca (`X=41`) | Huila (`X=42`) | Tolima (`X=43`) |
|---|---|---|---|
| Bloque reservado | `10.41.0.0/16` | `10.42.0.0/16` | `10.43.0.0/16` |
| Gerencia / VLAN 101 | `10.41.1.0/24` | `10.42.1.0/24` | `10.43.1.0/24` |
| Soporte / VLAN 102 | `10.41.2.0/24` | `10.42.2.0/24` | `10.43.2.0/24` |
| Logística / VLAN 103 | `10.41.3.0/24` | `10.42.3.0/24` | `10.43.3.0/24` |
| Transporte / VLAN 104 | `10.41.4.0/24` | `10.42.4.0/24` | `10.43.4.0/24` |
| Visitantes / VLAN 105 | `10.41.5.0/24` | `10.42.5.0/24` | `10.43.5.0/24` |
| Servidores / VLAN 110 | `10.41.10.0/24` | `10.42.10.0/24` | `10.43.10.0/24` |
| Borde / VLAN 120 | `10.41.20.0/24` | `10.42.20.0/24` | `10.43.20.0/24` |
| Gateway Logística | `10.41.3.1` | `10.42.3.1` | `10.43.3.1` |
| SSID Logística | `AP-41-Logistica` | `AP-42-Logistica` | `AP-43-Logistica` |
| AcopioID | `ACOPIO-CAUCA` | `ACOPIO-HUILA` | `ACOPIO-TOLIMA` |
| ASN del customer gateway propuesto | `65041` | `65042` | `65043` |

Las subredes son disjuntas dentro de cada sitio. Los tres bloques tampoco se solapan entre sí ni con `10.50/16`, `10.60/16`, `10.70/16`, `10.71/16` y `10.80/16` del plan cloud. Los números de VLAN se reutilizan en LAN distintas: no se extiende la capa 2 entre departamentos.

## 3. Topología y componentes locales

![Patrón del centro de acopio](diagrams/carga-d-centro-acopio.svg)

Fuente editable: [Draw.io](diagrams/carga-d-centro-acopio.drawio).

Se propone un firewall de perímetro con interfaces WAN/LAN, enrutamiento entre VLAN, políticas con estado, QoS en ambos sentidos e IPsec hacia AWS. El switch es administrable, con puertos de acceso y troncales 802.1Q, al menos 24 puertos de 1 GbE y alimentación PoE dimensionada para los AP. El switch opera en capa 2: **no se habilita enrutamiento inter-VLAN que evite el firewall**.

Se consideran inicialmente tres AP administrados, con radios 2,4/5 GHz, VLAN por SSID, aislamiento de clientes y QoS inalámbrica. Es un punto de partida de diseño: número, ubicación, potencia y canales se ajustan mediante estudio de cobertura/capacidad en oficinas, recepción/bodega y patio. No se atribuye cobertura ni rendimiento real sin plano y medición. Cada AP anuncia solo los SSID necesarios para su área; los SSID sensibles no se difunden en todo el predio por comodidad.

Las conexiones AP–switch y switch–firewall son cableadas. Las troncales permiten únicamente las VLAN necesarias; los escritorios e impresora usan puertos de acceso, sin etiquetado aceptado del usuario. Los puertos no utilizados quedan deshabilitados. La gestión de AP/switch reside en VLAN 110 y nunca en la red de visitantes. No se usa VLAN 1 como red operativa por defecto.

Como verificación inicial de puertos: 6 escritorios + 3 AP + 1 host de servicios + 1 impresora + 1 firewall = **12 puertos**; un switch de 24 deja 12 libres antes de nuevas básculas, impresoras o redundancia. La potencia PoE se calcula con el consumo máximo de los AP seleccionados; el conteo de puertos no demuestra suficiencia eléctrica. El firewall debe comprobar el caudal WAN con IPsec y las políticas activas, no solo su velocidad nominal de interfaces.

### Servicios y direcciones locales propuestas

| Servicio | Dirección del patrón | Función y límite |
|---|---|---|
| Gestión del switch y AP | `10.X.10.2–5` | Cuatro direcciones de administración; solo equipo/usuarios de gestión autorizados. |
| Servidor de impresión | `10.X.10.10` | Cola persistente IPPS/IPP sobre TLS, TCP 631; spool cifrado y permisos por rol. |
| Controlador de red | `10.X.10.11` | Gestión de configuración y estado de los AP/switch; consola HTTPS administrativa. |
| Autenticación de WLAN | `10.X.10.12` | RADIUS local para equipos registrados; solo clientes de infraestructura autorizados. |
| Copia de continuidad | `10.X.10.13` | Recepción de respaldos cifrados de colas y configuración desde equipos permitidos. No sustituye la base cloud. |
| Impresora de etiquetas | `10.X.10.20` | Conexión cableada; recibe trabajos únicamente del servidor de impresión. |
| DHCP, DNS y NTP de LAN | Gateway `.1` de cada VLAN | Servicios mínimos del firewall; las interfaces no exponen la consola a usuarios o invitados. |

Los servicios pueden ejecutarse como instancias aisladas en un host local pequeño con almacenamiento cifrado. Es una propuesta de consolidación para moderar equipo, **sin alta disponibilidad física**. Como comparten VLAN 110, se aplican también firewalls de host/ACL de puertos: el firewall inter-VLAN no puede inspeccionar por sí solo todas las comunicaciones entre hosts del mismo segmento. Los protocolos de aprovisionamiento del fabricante se concretan antes de la instalación y alimentan #9.

La WLAN de personal y conductores utiliza autenticación individual de equipos mediante EAP-TLS/RADIUS local y asignación autorizada a su zona. Los certificados se provisionan antes del uso; conectarse a wifi no otorga permisos sobre sacos ni sustituye MFA. Para visitantes se propone una credencial temporal exclusiva de esa WLAN y aislamiento entre clientes. La administración de equipos se realiza desde un puesto autorizado de Soporte, no desde cualquiera de sus siete clientes. Especificaciones de identidad y credenciales se armonizan con #4; no se guardan secretos en este documento ni en Terraform.

## 4. Enrutamiento y aislamiento entre zonas

La política base es **denegar conexiones nuevas entre zonas**, con excepciones limitadas por destino, servicio e identidad. Las respuestas de sesiones autorizadas se permiten por estado; no se abre una regla inversa general. Esta sección entrega requisitos a #9, que consolidará la tabla definitiva de firewall; no pretende sustituirla.

| Origen | Destino / servicio | Decisión del patrón |
|---|---|---|
| VLAN 101/102/103/104/105 | Gateway de su propia VLAN: DHCP, DNS y NTP | Permitir únicamente esos servicios de infraestructura; no la consola. |
| **Visitantes 105** | **Gerencia 101 y Logística 103** | **Denegar explícitamente y registrar el intento.** |
| Visitantes 105 | Resto de LAN, gestión, tres acopios y prefijos privados de nube/VPN | Denegar; la red invitada solo puede usar los servicios mínimos de su gateway y la salida pública filtrada. |
| Visitantes 105 | Internet público permitido | Permitir después de los bloqueos internos, mediante NAT y límites de su clase. Sin acceso a destinos privados ni otras redes especiales. |
| Transporte 104 | Gerencia, Logística, servidores y gestión | Denegar, salvo los servicios mínimos del gateway. La aplicación del conductor sale por HTTPS a su API pública autorizada. |
| Gerencia 101 y Soporte 102 de uso general | Otras VLAN de usuarios | Denegar; la información de sacos se consulta por la aplicación con su rol. |
| Logística 103 | Servidor de impresión `10.X.10.10`, TCP 631/TLS | Permitir desde puestos y usuarios autorizados. No se abre la impresora directamente a los teléfonos. |
| Servidor de impresión | Impresora `10.X.10.20`, TCP 631/TLS | Permitir por ACL/firewall de host y puerto. Modelo de impresora debe soportar el protocolo elegido. |
| Puesto de administración autorizado en Soporte | IP concretas de gestión 110 y firewall | Permitir HTTPS y, si es necesario, SSH a equipos concretos. Resto de Soporte no tiene ese privilegio. |
| AP y switch | RADIUS/controlador locales | Permitir los protocolos de gestión y autenticación del equipo seleccionado; no tráfico de usuarios arbitrarios. |
| Puestos Logística autorizados | Servicios privados de aplicación de producción | Permitir HTTPS por VPN según #9; no acceso directo a DynamoDB ni administración cloud. |
| Estación registrada de cuadrilla en Logística | Endpoint privado S3 autorizado, HTTPS | Permitir carga/descarga de misión y objetos con su identidad; clasificar archivos grandes en cola masiva. |
| Puestos autorizados | Respaldo `10.X.10.13` | Permitir solo el canal cifrado de respaldo definido; impedir lectura entre clientes. |
| Cualquier zona no autorizada | Otro acopio, dev/test o administración de nube | Denegar; no se presume tránsito lateral a través de AWS. |

El bloqueo de invitados debe cubrir también IPv6, acceso a direcciones de los propios equipos y rutas alternativas. El resolver de invitados sirve solo la vista pública y no expone las zonas DNS privadas. Para el piloto se propone no habilitar IPv6 de usuario hasta disponer de una política equivalente. Aislar SSID o activar aislamiento de clientes en el AP **no sustituye** el bloqueo inter-VLAN del firewall. Se impide que un cliente evada su clase usando IP estática de otra zona o marcas DSCP elegidas por él.

## 5. WAN, VPN IPsec y resolución de nombres

Se conserva **un enlace por acopio de 100 Mbps simétricos**, compartido con toda la operación. El proveedor debe entregar IP pública estática o una solución de NAT-T compatible; no se asume que una conexión bajo CGNAT permita registrar directamente un customer gateway. Su disponibilidad y caudal se verifican antes de contratar.

La VLAN 120 es tránsito privado hacia el CPE: se proponen `10.X.20.1` para el CPE y `10.X.20.2` para la WAN del firewall. No se confunden con la IP pública del customer gateway ni con las direcciones internas `/30` de cada túnel que asigne AWS. Si el CPE hace NAT, configura NAT-T y las reglas hacia ambos endpoints de AWS; no publica la gestión del firewall.

Cada acopio tiene una conexión Site-to-Site VPN con **dos túneles** hacia el Transit Gateway de la cuenta `AromaPacifico-Network` [T1]. Se propone BGP con preferencia de un túnel y el otro disponible como respaldo; el TGW conserva ASN `64512` de #7 y los customer gateways usan los ASN de la tabla. Se validan rutas de ida/vuelta, parámetros de cifrado, MTU y conmutación. Dos túneles no duplican los 100 Mbps ni eliminan la dependencia de un solo ISP/firewall.

El acopio anuncia solo los prefijos operativos necesarios (`10.X.3.0/24` y los servicios autorizados de `10.X.10.0/24`); visitantes no se anuncia. El anuncio de una ruta no otorga acceso: siguen aplicando ACL y políticas. Desde AWS solo se aceptan los prefijos de producción y resolución DNS estrictamente necesarios, con filtros; no una ruta por defecto, dev/test ni las redes de otros departamentos. Los destinos y rutas exactos se cruzan con #7/#9/#22. Tráfico privado hacia la VPN conserva su dirección de origen y no usa NAT a internet.

El DNS local reenvía únicamente las zonas privadas de AromaPacífico al resolver híbrido diseñado en #7. Los nombres públicos se resuelven por la ruta pública autorizada. S3 desde acopio utiliza el endpoint de interfaz y su DNS privado según #7; no se intenta alcanzar desde on-premises un Gateway Endpoint de S3. Cognito, la aplicación del transportador y otros servicios públicos necesitan su salida HTTPS autorizada: no se presentan como si todos vivieran dentro de la VPC.

Si cae un túnel se utiliza el otro. Si cae el ISP, el firewall o ambos túneles, se activa la operación pendiente de sección 8. No se añade un segundo proveedor, otra región o una VPN directa a cada VPC sin una decisión de alcance y costo.

## 6. Capacidad y QoS durante cosecha

### Cálculo con el inventario completo

| Zona | Clientes | Bajada a 2 Mbps/cliente | Subida a 0,5 Mbps/cliente |
|---|---:|---:|---:|
| Gerencia | 7 | 14 Mbps | 3,5 Mbps |
| Soporte | 7 | 14 Mbps | 3,5 Mbps |
| Logística | 22 | 44 Mbps | 11 Mbps |
| Transporte | 20 | 40 Mbps | 10 Mbps |
| Visitantes | 10 | 20 Mbps | 5 Mbps |
| **Total** | **66** | **132 Mbps** | **33 Mbps** |

La bajada excede el enlace en **32 Mbps incluso antes de protocolos y archivos de dron**. Aunque se desconectaran los diez visitantes, los 56 clientes restantes pedirían 112 Mbps. Por tanto, no se declara que los 100 Mbps permitan ofrecer 2 Mbps simultáneos a todos, ni se oculta el problema suponiendo una concurrencia menor sin evidencia.

### Política propuesta de pico

Se fija inicialmente un techo global de **90 Mbps por sentido** en el borde, dentro de los 100 contratados, con margen operativo. Es un parámetro inicial de ingeniería, no una medición del circuito ni una garantía de que la sobrecarga sea exactamente 10 %. Se reduce si las mediciones muestran menor caudal o congestión del proveedor. La reserva no se usa para prometer más tráfico del contratado.

| Clase | Máximo por cliente o flujo | Techo agregado bajada | Techo agregado subida | Tratamiento en cosecha |
|---|---|---:|---:|---|
| Interactivo Gerencia + Soporte + Logística: 36 clientes | 2 Mbps bajada / 0,5 Mbps subida por cliente de uso interactivo | **72 Mbps** | **18 Mbps** | Prioridad a recepción/despacho/confirmación; luego oficina. |
| Transporte: 20 clientes | **0,5 / 0,25 Mbps** por teléfono | **10 Mbps** | **5 Mbps** | Aplicación operativa; descargas personales bloqueadas. |
| Visitantes: 10 clientes | **0,2 / 0,1 Mbps** por teléfono | **2 Mbps** | **1 Mbps** | Mejor esfuerzo, sin garantía; primera clase que se pausa ante congestión. |
| Objetos de dron y sincronización masiva | Excepción por flujo y estación registrada; no por pertenecer solamente a Logística | **4 Mbps** | **60 Mbps** | Menor prioridad que las transacciones; cargas acotadas y reanudables. |
| Control, DNS, autenticación y servicios autorizados | Solo infraestructura identificada | **2 Mbps** | **6 Mbps** | Conservar operación de red y control. |
| **Suma de techos de clase** | | **90 Mbps** | **90 Mbps** | Sujetos al techo raíz y al caudal real. |

**Se limita explícitamente la referencia de 2/0,5 Mbps para transporte y visitantes durante el pico.** Los 36 clientes de oficina/logística conservan ese perfil de referencia; sus valores son techos de acceso, no mínimos garantizados. La sobrecarga de encapsulado se contabiliza en la raíz WAN, por lo que no se promete que todas las clases alcancen simultáneamente cada máximo útil de la tabla.

Las clases se asignan de forma excluyente por dispositivo, destino y tipo de flujo: un objeto de dron usa la clase masiva y no se cuenta de nuevo como interactivo. La excepción de subida para esa estación no libera su navegación personal. La VPN comparte el mismo enlace físico: no se suma otro cupo de 90/100 Mbps por túnel [T2]. El equipo elegido debe admitir raíz global, techos por clase y límite individual antes de perder la identidad del cliente por NAT/cifrado; una limitación por IP sin techo agregado no evita sobresuscripción [T3]. La configuración concreta y la equivalencia entre sentidos se comprueban en el firewall seleccionado.

Se priorizan solicitudes de recepción, aceptación/rechazo, despacho y ACK frente a archivos; se bloquean P2P, streaming recreativo y actualizaciones masivas durante el pico, y se programan respaldos pesados fuera del horario operativo. No se confía en DSCP de clientes no administrados. Las marcas se asignan o normalizan en infraestructura de confianza y se comprueba su correspondencia con QoS wifi [T4]. No se promete clasificar todo HTTPS cifrado por contenido: se utilizan dispositivos y destinos operativos conocidos.

### Qué significan los 400 sacos diarios

Suponiendo una jornada de 10 h solo para dimensionar (no es un dato impuesto al acopio), 400 sacos equivalen a 40/h, uno cada 90 s en promedio. No prueba ausencia de ráfagas. Un escenario de cálculo de tres transacciones por saco y 20 kB totales por transacción produciría `400 × 3 × 20.000 = 24.000.000 bytes/día`, unos **0,0053 Mbps medios** durante esa jornada. Son supuestos, no mediciones del software ni la descripción final de #15.

La cola interactiva se valida con una prueba futura de ráfaga de 30 transacciones/s de ese tamaño: aproximadamente **4,8 Mbps agregados**, que caben como carga de datos en su clase y no demuestran por sí solos latencia de aplicación. Una foto de dron de 50 MB a 10 Mbps efectivos tardaría al menos 40 s; a 60 Mbps, al menos 6,7 s, antes de reintentos y sobrecarga. El máximo de 60 Mbps de la clase masiva no es una promesa de ese caudal sostenido. Estos contrastes justifican separar transacciones pequeñas y objetos grandes.

## 7. Recepción e impresión de códigos

1. El operario, en VLAN 103, entra a la aplicación con Cognito y MFA. Identifica el saco, registra hora, responsable y datos de recepción; la aplicación valida sus permisos, no solamente su dirección IP.
2. Si el saco ya tiene código, se reutiliza. Si falta, se asigna un identificador emitido o reservado para ese acopio por la plataforma; la etiqueta no contiene cédula ni datos personales. La definición canónica del código y la decisión aceptado/rechazado pertenecen a #15.
3. El trabajo se envía al servidor local de impresión por el canal autenticado y cifrado. Incluye `job_id`, identificador de saco y responsable; se controla la reimpresión y se impide usar la impresora desde invitados o transporte.
4. El spooler registra el resultado. Una pérdida de respuesta no garantiza que el papel no salió: antes de reimprimir se muestra el estado incierto al operario. La reimpresión conserva el mismo código; no da de alta otro saco.
5. El evento se considera persistido en nube solo tras su confirmación. Un comprobante local no convierte automáticamente el saco en aceptado por el sistema central.

La impresión es local y no depende de descargar de S3 cada plantilla ni de una cola cloud para cada etiqueta. Las plantillas y el cupo de identificadores preasignados se preparan durante la conexión normal. Se propone una reserva inicial de 1.000 identificadores por acopio (2,5 días a 400/día), exclusiva y conciliada por el servidor local; es un supuesto revisable de #15. Si no quedan identificadores válidos, se usa comprobante manual provisional y conciliación posterior; no se improvisan códigos canónicos ni se guardan secretos de firma en los teléfonos.

## 8. Continuidad sin WAN, energía y recuperación

Cada puesto de recepción conserva una cola local cifrada (SQLite o almacenamiento transaccional persistente equivalente de la aplicación), escrita antes de informar recepción local. Registra identificador único del evento, saco, acopio, responsable, hora UTC original, secuencia local, resultado propuesto y estado de sincronización. No se requiere compartir archivos SQLite entre puestos por la LAN.

Se respalda la cola cifrada en el servicio `10.X.10.13` al confirmar la escritura local si la LAN sigue disponible, y se informa si falta esa copia. Un fallo de ambos soportes puede perder pendientes: no se afirma protección cloud de un dato que aún no ha llegado a ella. No se aplica a las operaciones del acopio el descarte de lecturas de finca a las 24 h; los pendientes se conservan hasta confirmación, con alarma por antigüedad y espacio disponible, sin borrar eventos de custodia para liberar disco.

Con WAN caída, la LAN, el spooler y el controlador local continúan si tienen energía. Solo una sesión previamente autorizada y todavía válida puede registrar operaciones provisionales conforme a la política de #4/#15. Generar un TOTP sin conexión no significa que Cognito lo haya validado. No se permiten nuevos inicios de sesión ni se ignora la expiración del token; sin autorización vigente se usa contingencia manual y posterior conciliación. La revocación producida mientras el sitio está aislado no se conoce instantáneamente: al sincronizar se revalidan identidad y permisos, y los rechazos quedan para revisión.

Al restablecer conexión, cada puesto renueva su autenticación, envía lotes pequeños y conserva el mismo identificador al reintentar. El servidor deduplica, diferencia hora del hecho y hora de recepción, confirma por evento y aísla conflictos. Se retiran de la cola solo los confirmados. Transacciones de custodia preceden a objetos masivos y el límite de clase sigue vigente durante el drenado. El RPO cloud de 15 min no demuestra respaldo de eventos aún offline.

Se propone UPS para CPE, firewall, switch/PoE, host de servicios y puestos de recepción, con objetivo inicial de 30 minutos de autonomía y apagado ordenado. Se selecciona con potencia medida y energía utilizable a esa carga, no solo por VA nominales. La impresora se respalda únicamente si su carga y la UPS lo admiten. Si se agota la batería, se guarda la cola y se detiene la captura digital; queda el procedimiento manual. No se inventa un generador, un segundo ISP ni alta disponibilidad inexistente.

## 9. Verificación de aceptación

| Criterio de #8 | Evidencia documental | Comprobación de instalación pendiente |
|---|---|---|
| Visitantes no enruta hacia logística ni gerencia | Tabla de VLAN, política explícita de denegación y marca roja en el diagrama. | Probar TCP/UDP y acceso por IP a ambas redes desde invitado, además de internet permitido y bloqueo IPv6/rutas alternativas. Un ping fallido no basta. |
| Capacidad de 100 Mbps o límites explícitos | 66 clientes, cálculo 132/33 Mbps y perfil de pico con suma de techos 90/90 Mbps. | Medir caudal y colas con carga simultánea, VPN, tráfico de dron y visitantes; comprobar que no se contabiliza doble el enlace y que recepción conserva prioridad. |
| Un solo patrón para tres departamentos | Tabla de sustitución completa, VLAN invariantes y diagrama con `X=41/42/43`. | Verificar gateway, DHCP, SSID, rutas y ausencia de solape al instanciar cada sitio. |

También se planifican pruebas de impresión autorizada y reimpresión, corte/retorno de WAN con pendientes y respuestas perdidas, conmutación de túnel, reinicio de puesto, agotamiento de sesión y corte de energía. En esta entrega se verificaron documentalmente conteos, aritmética, CIDR, enlaces y XML; **ninguna de esas pruebas de red, equipos o aplicaciones está ejecutada**.

## 10. Supuestos nuevos y relación con otras historias

| Supuesto o decisión propuesta | Motivo / destino de validación |
|---|---|
| VLAN 101–105/110/120, cinco SSID de usuarios y servicios en las IP reservadas de sección 3 | Implementar las zonas del caso sin alterar sus CIDR; revisar con #9. |
| Tres AP iniciales, switch 24 puertos, host local consolidado y UPS objetivo 30 min | Punto de partida de capacidad; validar cobertura, potencia y disponibilidad antes de compra. |
| Autenticación WLAN local y credencial temporal invitada | Conservar acceso LAN sin WAN y separación de zonas; armonizar con #4. |
| Raíz 90/90 Mbps, perfiles reducidos para transporte/visitantes y clase masiva | Resolver sobresuscripción explícita; validar con tráfico real, #9 y #18. |
| Cola cifrada por puesto, copia local y spooler persistente | Concretar continuidad de #6; código de aplicación fuera del reto. |
| Cupo de 1.000 identificadores y captura provisional sin autoridad cloud offline | Evitar dependencia de WAN para cada etiqueta; contrato final de #15. |
| CPE `.20.1`, firewall `.20.2`, IP pública/NAT-T y ASN 65041/65042/65043 | Especificar el borde sin confundir LAN con identidad pública de VPN; verificar ISP y cruzar con #7/#22. |
| Jornada de 10 h, tres transacciones/saco de 20 kB y ráfaga de prueba 30/s | Escenarios de dimensionamiento, no cifras oficiales; sustituir por medición cuando exista software. |

Estas propuestas están visibles en el propio entregable; su incorporación al registro transversal corresponde a la integración del equipo. No se modifica dicho archivo desde esta HU. #9 consolida reglas permanentes/temporales; #22 codifica el patrón cloud y su conexión con un acopio, no el cableado o la configuración física de todos los centros. La aceptación de #8 no despliega infraestructura ni amplía las 100 horas.

## 11. Referencias técnicas

Consulta: 6 de noviembre de 2026. Las cifras del caso provienen del enunciado y las decisiones integradas del repositorio; las referencias siguientes sustentan mecanismos técnicos, no los supuestos de carga ni una cotización de equipos.

- **[T1] AWS:** [componentes de Site-to-Site VPN y sus dos túneles](https://docs.aws.amazon.com/vpn/latest/s2svpn/how_it_works.html).
- **[T2] Netgate:** [shaping y VPN sobre la misma WAN](https://docs.netgate.com/pfsense/en/latest/trafficshaper/vpns.html).
- **[T3] Netgate:** [limitadores por IP/red y necesidad de controlar el agregado](https://docs.netgate.com/pfsense/en/latest/trafficshaper/limiters.html). Se usa como referencia de mecanismo; no obliga a comprar una marca.
- **[T4] IETF:** [RFC 8325: correspondencia de QoS entre IP y WLAN](https://www.rfc-editor.org/rfc/rfc8325.html).
