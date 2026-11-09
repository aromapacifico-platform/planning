# Políticas de firewall del perímetro de acopio y de la nube

**Historia:** [#9](https://github.com/aromapacifico-platform/planning/issues/9) · **Responsable:** Juan Ocampo (`juandavid175`) · **Fecha:** 7 de noviembre de 2026.  
**Estado:** propuesta de políticas para revisión y contrato de trazabilidad de IaC. No son reglas desplegadas.

## 1. Fuentes revisadas y límites del entregable

Se consultó GitHub mediante su integración: `planning/main` en `4c6fa27a31a5ac5c38c0da5711e36936024ba2cd`; [#7, direccionamiento integrado](red-direccionamiento-nube.md); [gobierno](gobierno-landing-zone.md); y [decisiones del senior](../governance-and-decisions/briefing-inicial-juniors.md). La dependencia #8 está propuesta en la [PR #53](https://github.com/aromapacifico-platform/planning/pull/53), commit `2399d9637c654fe3a73d483f1300cc95977f7db4`. Se revisó también la conectividad de [PR #49](https://github.com/aromapacifico-platform/planning/pull/49), commit `af64c56128198c4978d23f5f1fc8cc699b6b1ff7`. Ambas PR seguían abiertas al consultar; no se presume su aprobación ni se reemplaza su contenido.

`iac/main`, commit `9afc7f5b6ba3c5881f21d36865b3e9faf73e1fbc`, contiene únicamente README. Por tanto, los nombres de recursos y claves siguientes son un **contrato propuesto para #23**, no direcciones de recursos ya existentes ni evidencia de un plan ejecutado.

Esta historia entrega solo `docs/architecture/red-firewall.md`. Se conservan la segmentación y servicios de #8, Transit Gateway, CIDR y dos zonas de #7, Cognito para aplicaciones e IAM Identity Center para administración. Las correcciones de interpretación técnica se documentan aquí y deberán armonizarse en #19; no se editan otros archivos desde #9.

### Qué significa mapear una regla a IaC

Cada fila tiene un ID estable y una clave de catálogo única. #23 crea las reglas SG/NACL que correspondan a los componentes del patrón elegido y devuelve las políticas de otros controles a sus módulos propietarios. Una política permanente de consulta pública no obliga a instanciar el servicio de consulta cuando el patrón de las 100 horas es ingesta; se conserva en el catálogo para la arquitectura completa. Las temporales no se materializan en el módulo base.

Las reglas del firewall físico/host de acopio **no se implementan mediante un SG de AWS**. Su mapeo es a una política local por ID, que se exporta y aplica con el mecanismo del equipo seleccionado. La evidencia de exportación no acredita su aplicación. El backend/provider de gestión de ese equipo no está definido en #8: debe acordarse en #23 antes de afirmar que todas las reglas locales están automatizadas. Esta distinción evita presentar un archivo de configuración o un output como si fuera un firewall desplegado.

## 2. Objetos de red y parámetros

Los alias se resuelven antes del plan o de aplicar configuración. No se inventan IP públicas, direcciones de endpoints ni rangos de operadores. Un alias externo vacío o no validado produce bloqueo/error de validación, nunca sustitución por `0.0.0.0/0`. Un alias de identidad/SG no se interpreta como si fuera un CIDR.

| Alias | Definición verificable |
|---|---|
| `X` | 41 Cauca, 42 Huila o 43 Tolima. El patrón local se repite sin extender capa 2. |
| `GER-X`, `SOP-X`, `LOG-X`, `TRA-X`, `VIS-X`, `SRV-X` | `10.X.1.0/24`, `.2.0/24`, `.3.0/24`, `.4.0/24`, `.5.0/24`, `.10.0/24`, respectivamente; el prefijo completo comienza por `10.X`. |
| `U-X` / `VLAN-U-X` | Las cinco redes de usuarios, excluidos servidores y borde. |
| `GW de su VLAN` | `10.X.Z.1` únicamente en la VLAN correspondiente; invitados no acceden a gateways ajenos. |
| `ADMIN-X` / `FW-MGMT-X` | Puesto administrado reservado `10.X.2.20/32` / interfaz de gestión del firewall `10.X.10.1/32`. IP no sustituye identidad de administrador. |
| `NET-X`, `AP-X` | Switch `10.X.10.2/32` y AP `.3–.5/32`; `AP-X` excluye el switch si no usa RADIUS. |
| `PRINT-X`, `CTRL-X`, `RADIUS-X`, `BACKUP-X`, `LABEL-X` | `10.X.10.10/32`, `.11/32`, `.12/32`, `.13/32`, `.20/32`, en ese orden. |
| `LOG-AUT-X`, `DRON-X` | Reservas de IP concretas, aprobadas y vinculadas a equipos de Logística; no se abre todo LOG-X por comodidad. `LOG-AUT-CIDR`, `DRON-CIDR`, `BACKUP-CIDR` son las listas de esos /32 para el acopio patrón. |
| `VIS-CIDR` | `10.41.5.0/24`, `10.42.5.0/24`, `10.43.5.0/24`. |
| `INTERNO` | Redes de los tres acopios, todos los CIDR cloud, direcciones de equipos locales y otros rangos privados/especiales no navegables; se expande explícitamente en el perímetro. |
| `WEB-PUBLICA` | Internet público IPv4, excluidos INTERNO y destinos bloqueados. Destino amplio deliberado solo para navegación invitada con controles de #8; no es un origen de entrada. |
| `WAN-X` | `10.X.20.2/32` detrás del CPE según #8. `PUB-ACOPIOS-IP` son las /32 públicas reales de los CPE, obtenidas del ISP; no `10.X.20.2`. |
| `PUB-VPN-AWS-IP` / `TUNNEL-*` | Dos IP públicas de AWS por conexión / IP internas de los dos túneles del customer gateway y AWS, desde outputs de #22. |
| `DNS-X`, `DNS-CIDR` | Origen de forwarding del firewall fijado en `10.X.10.1/32`; DNS-CIDR contiene las /32 de los sitios que se conectan al ambiente. |
| `DNS-PUBLICO-IP`, `NTP-PUBLICO-IP` | Listas de IP concretas de forwarders y servidores de hora seleccionados por operación; pendientes de configuración, sin permiso genérico. |
| `API-PUBLICA`, `COGNITO-FQDN` | FQDN de la API y autenticación del piloto, obtenidos de sus recursos. Alias FQDN solo en el perímetro que lo soporte; un SG no admite nombres DNS. |
| `ADMIN-CLOUD-FQDN` | Lista aprobada de destinos HTTPS necesarios para IAM Identity Center, MFA, consola y API de administración de AWS; operación la mantiene por servicio/región, sin comodín de navegación general. Solo se consume en el firewall local. |
| `RESOLVER-IN-IP`, `RESOLVER-OUT-IP` | /32 reales de las ENI de entrada y salida de Route 53 Resolver en hub, obtenidas de sus recursos; las respuestas conservan rutas hacia DNS-CIDR. |
| `MOVIL-IP` | CIDR públicos de salida de los operadores/accesos autorizados para eventos no telemétricos, verificados y mantenidos. No hay lista aportada todavía: ese permiso queda bloqueado hasta definirla o aprobar un cambio de requisito. |
| `SUB(t,a)` | Prefijo /24 de la categoría `t` y zona `a` del plan integrado. En prod: telemetría 1/101, dron 2/102, app 10/110, datos 20/120, objetos 30/130, admin 40/140, pública 50/150, todos bajo `10.70`. |
| `APP-CIDR`, `FUNCION-CIDR`, `ADMIN-CIDR` | Respectivamente `SUB(app,a/b)`, `SUB(dron,a/b)`, `SUB(admin,a/b)` del ambiente concreto, no mezclas de dev/test/prod. |
| `PRIV-AUT` | Prefijos privados del propio ambiente, prefijos de endpoints/resolvers de hub que tengan ruta autorizada, LOG-AUT-CIDR, BACKUP-CIDR y DNS-CIDR. Excluye invitados, otros ambientes y tránsito a otros acopios. |
| `SG-*` | IDs reales de SG del ALB, backend de consulta, Lambda ingesta, Lambda patrón, nodos de administración y endpoints; provienen de outputs, no se inventan ni se conectan a servicios sin ENI compatible. |
| `SG-CLIENTES-LOG/KMS` y sus `*-CIDR` | Subconjuntos enumerados de ingesta/función/admin que realmente llaman esos servicios. Cada SG o CIDR genera una entrada individual con sufijo, no una regla comodín. |
| `VPCE-*-IP/ID` | IP privadas /32 o ID de endpoints de S3, execute-api, Logs, KMS, Rekognition y SSM/resolvers; obtenidos de la red aprobada. No se presupone que todos estén ya creados. |
| `PL-S3`, `PL-DDB`, `S3-DDB-IP` | Prefix lists administradas de S3/DynamoDB de la región / expansión a sus CIDR actuales para NACL. Los IDs de prefix list son válidos en SG, no en NACL. |
| `ADMIN-HUB-IP` | /32 privada de un puesto/nodo de soporte de hub aprobado para un incidente, nunca todo el rango de internet. |

En dev/test se usan sus CIDR de #7, sin acceso a acopios reales por defecto. `X` es un parámetro de patrón: no se permite sumar todos los departamentos a una regla de un solo acopio sin una necesidad concreta. Las IP de ENI, endpoints y peers se actualizan con sus recursos; no se copian como valores permanentes inmutables.

## 3. Tabla única de políticas

**P:** permanente en el diseño del piloto. **T:** temporal, deshabilitada por defecto. **Ámbito:** componente donde aplica, no un permiso de despliegue. Los puertos indicados son de destino salvo que aparezca `origen → destino`. Todos los controles requieren también ruta, autenticación y permisos del recurso cuando corresponda.

La columna «Contrato #23» es una clave dentro de `module.security.rule_catalog`. Su traducción concreta por tipo se define en sección 4. Las filas de una misma capa se ordenan por su prioridad; las políticas de capas distintas se evalúan en conjunto, no como una lista universal de firewall.

| ID | Control | Origen | Destino | Protocolo / puerto | Acción | Vigencia | Ámbito | Contrato #23 |
|---|---|---|---|---|---|---|---|---|
| L01 | LOCAL | Clientes sin dirección de VLAN-U-X | DHCP de su VLAN / broadcast local | UDP 68 → 67 | Permitir | P | Local | `local_policy["L01"]` |
| L02 | LOCAL | U-X y SRV-X | GW de su VLAN | TCP/UDP 53 | Permitir | P | Local | `local_policy["L02"]` |
| L03 | LOCAL | U-X y SRV-X | GW de su VLAN | UDP 123 | Permitir | P | Local | `local_policy["L03"]` |
| L04 | LOCAL | LOG-AUT-X | PRINT-X | TCP 631 / TLS | Permitir | P | Local | `local_policy["L04"]` |
| L05 | HOST | PRINT-X | LABEL-X | TCP 631 / TLS | Permitir | P | Local | `host_policy["L05"]` |
| L06 | LOCAL | ADMIN-X | FW-MGMT-X | TCP 443 / TLS | Permitir | P | Local | `local_policy["L06"]` |
| L07 | LOCAL | ADMIN-X | CTRL-X | TCP 443 / TLS | Permitir | P | Local | `local_policy["L07"]` |
| L08 | HOST | CTRL-X | NET-X | TCP 443 / TLS | Permitir | P | Local | `host_policy["L08"]` |
| L09 | HOST | AP-X | RADIUS-X | UDP 1812 | Permitir | P | Local | `host_policy["L09"]` |
| L10 | HOST | AP-X | RADIUS-X | UDP 1813 | Permitir | P | Local | `host_policy["L10"]` |
| L11 | LOCAL | LOG-AUT-X | BACKUP-X | TCP 443 / TLS | Permitir | P | Local | `local_policy["L11"]` |
| L12 | LOCAL | LOG-AUT-X | VPCE-API-IP | TCP 443 / TLS | Permitir | P | Privado | `local_policy["L12"]` |
| L13 | LOCAL | DRON-X y BACKUP-X | VPCE-S3-IP | TCP 443 / TLS | Permitir | P | Privado | `local_policy["L13"]` |
| L14 | LOCAL | DNS-X | RESOLVER-IN-IP | TCP/UDP 53 | Permitir | P | Privado | `local_policy["L14"]` |
| L15 | LOCAL | DNS-X | DNS-PUBLICO-IP | TCP/UDP 53 | Permitir | P | Local | `local_policy["L15"]` |
| L16 | LOCAL | DNS-X | NTP-PUBLICO-IP | UDP 123 | Permitir | P | Local | `local_policy["L16"]` |
| L17 | LOCAL | U-X | API-PUBLICA y COGNITO-FQDN | TCP 443 / TLS | Permitir | P | Aplicacion | `local_policy["L17"]` |
| L18 | LOCAL | VIS-X | INTERNO | Todos | Denegar | P | Local | `local_policy["L18"]` |
| L19 | LOCAL | TRA-X | INTERNO | Todos | Denegar | P | Local | `local_policy["L19"]` |
| L20 | LOCAL | GER-X y SOP-X | Otras VLAN de usuarios y SRV-X | Todos | Denegar | P | Local | `local_policy["L20"]` |
| L21 | LOCAL | VIS-X | WEB-PUBLICA | TCP 80 y 443 | Permitir | P | Local | `local_policy["L21"]` |
| L22 | LOCAL | PUB-VPN-AWS-IP | WAN-X | UDP 500 y 4500 | Permitir | P | VPN | `local_policy["L22"]` |
| L23 | LOCAL | WAN-X | PUB-VPN-AWS-IP | UDP 500 y 4500 | Permitir | P | VPN | `local_policy["L23"]` |
| L24 | LOCAL | TUNNEL-AWS-IP | TUNNEL-CGW-IP | TCP 179 | Permitir | P | VPN | `local_policy["L24"]` |
| L25 | LOCAL | TUNNEL-CGW-IP | TUNNEL-AWS-IP | TCP 179 | Permitir | P | VPN | `local_policy["L25"]` |
| L26 | LOCAL | WAN-X y PUB-VPN-AWS-IP | Peer exacto de la conexión VPN | ICMP tipo 3 / código 4 | Permitir | P | VPN | `local_policy["L26"]` |
| L27 | LOCAL | RESOLVER-OUT-IP | DNS-X | TCP/UDP 53 | Permitir | P | Privado | `local_policy["L27"]` |
| L28 | HOST | Equipos no autorizados de SRV-X | PRINT-X, LABEL-X, CTRL-X y RADIUS-X | Todos | Denegar | P | Local | `host_policy["L28"]` |
| L29 | LOCAL | ADMIN-X | ADMIN-CLOUD-FQDN | TCP 443 / TLS | Permitir | P | Admin | `local_policy["L29"]` |
| L30 | INVARIANTE | Tráfico nuevo no cubierto por L01–L29 | Perímetro local y hosts | Todos | Denegar por defecto | P | Local | `assertions["L30"]` |
| C01 | SG-IN | 0.0.0.0/0 | SG-ALB-CONSULTA | TCP 443 / TLS | Permitir | P | Consulta | `sg_ingress["C01"]` |
| C02 | SG-OUT | SG-ALB-CONSULTA | SG-CONSULTA | TCP 443 / TLS | Permitir | P | Consulta | `sg_egress["C02"]` |
| C03 | SG-IN | SG-ALB-CONSULTA | SG-CONSULTA | TCP 443 / TLS | Permitir | P | Consulta | `sg_ingress["C03"]` |
| C04 | SG-IN | LOG-AUT-CIDR | SG-VPCE-API | TCP 443 / TLS | Permitir | P | Privado | `sg_ingress["C04"]` |
| C05 | SG-IN | DRON-CIDR y BACKUP-CIDR | SG-VPCE-S3 | TCP 443 / TLS | Permitir | P | Objetos | `sg_ingress["C05"]` |
| C06 | SG-OUT | SG-INGESTA | PL-DDB | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C06"]` |
| C07 | SG-OUT | SG-INGESTA | PL-S3 | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C07"]` |
| C08 | SG-OUT | SG-FUNCION | PL-S3 | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C08"]` |
| C09 | SG-OUT | SG-FUNCION | PL-DDB | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C09"]` |
| C10 | SG-OUT | SG-FUNCION | VPCE-REKOG-IP | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C10"]` |
| C11 | SG-IN | FUNCION-CIDR | SG-VPCE-REKOG | TCP 443 / TLS | Permitir | P | Patron | `sg_ingress["C11"]` |
| C12 | SG-OUT | SG-CLIENTES-LOG | VPCE-LOGS-IP | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C12"]` |
| C13 | SG-IN | CLIENTES-LOG-CIDR | SG-VPCE-LOGS | TCP 443 / TLS | Permitir | P | Patron | `sg_ingress["C13"]` |
| C14 | SG-OUT | SG-CLIENTES-KMS | VPCE-KMS-IP | TCP 443 / TLS | Permitir | P | Patron | `sg_egress["C14"]` |
| C15 | SG-IN | CLIENTES-KMS-CIDR | SG-VPCE-KMS | TCP 443 / TLS | Permitir | P | Patron | `sg_ingress["C15"]` |
| C16 | SG-OUT | SG-ADMIN | VPCE-SSM-IP | TCP 443 / TLS | Permitir | P | Admin | `sg_egress["C16"]` |
| C17 | SG-IN | ADMIN-CIDR | SG-VPCE-SSM | TCP 443 / TLS | Permitir | P | Admin | `sg_ingress["C17"]` |
| C18 | SG-IN | DNS-CIDR | SG-RESOLVER-IN | TCP/UDP 53 | Permitir | P | Privado | `sg_ingress["C18"]` |
| C19 | SG-OUT | SG-RESOLVER-OUT | DNS-CIDR | TCP/UDP 53 | Permitir | P | Privado | `sg_egress["C19"]` |
| C20 | SG-OUT | SG-CONSULTA | PL-DDB | TCP 443 / TLS | Permitir | P | Consulta | `sg_egress["C20"]` |
| C21 | INVARIANTE | Cualquier origen no permitido explícitamente | SG de workloads y endpoints | Todos | Denegar implícito | P | Patron | `assertions["C21"]` |
| C22 | INVARIANTE | SG de workloads y endpoints | Destinos no enumerados | Todos | Denegar implícito | P | Patron | `assertions["C22"]` |
| N01 | NACL-IN | VIS-CIDR | Subredes privadas del ambiente | Todos | Denegar | P | Patron | `nacl_ingress["N01"]` |
| N02 | NACL-IN | PRIV-AUT | Subredes privadas del ambiente | TCP 443 | Permitir | P | Patron | `nacl_ingress["N02"]` |
| N03 | NACL-OUT | Subredes privadas del ambiente | PRIV-AUT y S3-DDB-IP | TCP 443 | Permitir | P | Patron | `nacl_egress["N03"]` |
| N04 | NACL-IN | PRIV-AUT | Subredes privadas del ambiente | TCP 53 | Permitir | P | Patron | `nacl_ingress["N04"]` |
| N05 | NACL-IN | PRIV-AUT | Subredes privadas del ambiente | UDP 53 | Permitir | P | Patron | `nacl_ingress["N05"]` |
| N06 | NACL-OUT | Subredes privadas del ambiente | PRIV-AUT | TCP 53 | Permitir | P | Patron | `nacl_egress["N06"]` |
| N07 | NACL-OUT | Subredes privadas del ambiente | PRIV-AUT | UDP 53 | Permitir | P | Patron | `nacl_egress["N07"]` |
| N08 | NACL-IN | PRIV-AUT y S3-DDB-IP | Subredes privadas del ambiente | TCP 1024–65535 | Permitir | P | Patron | `nacl_ingress["N08"]` |
| N09 | NACL-OUT | Subredes privadas del ambiente | PRIV-AUT | TCP 1024–65535 | Permitir | P | Patron | `nacl_egress["N09"]` |
| N10 | NACL-IN | PRIV-AUT | Subredes privadas del ambiente | UDP 1024–65535 | Permitir | P | Patron | `nacl_ingress["N10"]` |
| N11 | NACL-OUT | Subredes privadas del ambiente | PRIV-AUT | UDP 1024–65535 | Permitir | P | Patron | `nacl_egress["N11"]` |
| N12 | NACL-IN | 0.0.0.0/0 | Subredes de consulta pública | TCP 443 | Permitir | P | Consulta | `nacl_ingress["N12"]` |
| N13 | NACL-OUT | Subredes de consulta pública | Internet IPv4 | TCP 1024–65535 | Permitir | P | Consulta | `nacl_egress["N13"]` |
| N14 | NACL-OUT | Subredes de consulta pública | APP-CIDR | TCP 443 | Permitir | P | Consulta | `nacl_egress["N14"]` |
| N15 | NACL-IN | APP-CIDR | Subredes de consulta pública | TCP 1024–65535 | Permitir | P | Consulta | `nacl_ingress["N15"]` |
| N16 | INVARIANTE | Paquete sin coincidencia con N01–N15 | Subred protegida / destino no autorizado | Todos | Denegar implícito | P | Patron | `assertions["N16"]` |
| M01 | SERVICIO | 0.0.0.0/0 | Endpoint público IoT Core del piloto | TCP 8883 / MQTT-TLS | Permitir condicionado | P | Patron | `service_policy["M01"]` |
| M02 | SERVICIO | 0.0.0.0/0 | API pública de posición /telemetria/posicion | TCP 443 / HTTPS | Permitir condicionado | P | Movil | `service_policy["M02"]` |
| M03 | SERVICIO | MOVIL-IP y PUB-ACOPIOS-IP | API pública de eventos de aplicación | TCP 443 / HTTPS | Permitir condicionado | P | Movil | `service_policy["M03"]` |
| M04 | SERVICIO | 0.0.0.0/0 | Adaptador /telemetria/satelite | TCP 443 / HTTPS | Permitir condicionado | P | Satelite | `service_policy["M04"]` |
| M05 | SERVICIO | VPCE-API-ID + LOG-AUT-CIDR | API privada de recepción | TCP 443 / HTTPS | Permitir condicionado | P | Privado | `service_policy["M05"]` |
| M06 | SERVICIO | VPCE-S3-ID + roles de cuadrilla/respaldo | Bucket de objetos del piloto | TCP 443 / HTTPS | Permitir condicionado | P | Objetos | `service_policy["M06"]` |
| M07 | INVARIANTE | S3 / regla IoT / API Gateway autorizados | Función Lambda correspondiente | Invocación de servicio; sin puerto TCP | Permitir por permiso de servicio | P | Patron | `assertions["M07"]` |
| T01 | LOCAL | ADMIN-X | Un equipo NET-X individual | TCP 22 / SSH | Permitir | T | Deshabilitada | `local_policy["T01"]` |
| T02 | SG-IN | ADMIN-HUB-IP | Una instancia administrada individual | TCP 22 / SSH | Permitir | T | Deshabilitada | `sg_ingress["T02"]` |

### Condiciones por regla

- **L01:** Solo interfaz de acceso y asignación DHCP; no reenviar a nube.
- **L02:** DNS local; vista pública exclusiva para invitados.
- **L03:** Sincronización de hora local, sin acceso a consola.
- **L04:** Recepción envía trabajos al spooler, no directamente a impresora.
- **L05:** Misma VLAN 110: firewall de host y ACL/filtrado de puerto del switch.
- **L06:** Administración local por puesto autorizado y credencial de administrador.
- **L07:** Consola de gestión; no autoriza a todos los clientes de Soporte.
- **L08:** Equipos con gestión HTTPS; otros puertos de fabricante no quedan autorizados implícitamente.
- **L09:** Autenticación WLAN EAP-TLS; solo AP registrados.
- **L10:** Contabilidad de acceso desde AP registrados.
- **L11:** Interfaz HTTPS de respaldo cifrado; únicamente puestos autorizados.
- **L12:** Aplicación privada por VPN; identidad y autorización adicionales en la API.
- **L13:** Objetos y respaldo por endpoint privado; QoS de #8 sigue vigente.
- **L14:** Reenvío exclusivo de zonas privadas; origen del DNS fijado en VLAN 110.
- **L15:** Forwarders públicos expresamente configurados; no DNS arbitrario desde usuarios.
- **L16:** Servidores de tiempo autorizados; lista real previa al despliegue.
- **L17:** Acceso de aplicación/autenticación y retorno; solo destinos aprobados, sin acceso cloud administrativo.
- **L18:** Bloqueo explícito de Gerencia, Logística, gestión, otros acopios y prefijos cloud; después de L01–L03.
- **L19:** Conductor no alcanza servidores ni otras VLAN; utiliza su API pública autorizada.
- **L20:** Excepciones ADMIN-X→gestión ya definidas; sin comunicación lateral general.
- **L21:** Navegación pública filtrada y limitada; se evalúa después del bloqueo interno L18.
- **L22:** IKE y NAT-T solo desde los dos endpoints públicos reales de AWS.
- **L23:** Inicio de negociación y mantenimiento de ambos túneles.
- **L24:** BGP dentro de túneles; no se abre TCP 179 en internet.
- **L25:** BGP de origen acopio; filtros de rutas y ASN de #8.
- **L26:** PMTU entre peers conocidos; comprobar MSS/MTU sin permitir ICMP general.
- **L27:** Solo resolución inversa de zonas locales declaradas; sin consulta recursiva pública.
- **L28:** Protección dentro de VLAN 110, después de excepciones L05/L08/L09/L10; no se atribuye al router.
- **L29:** Inicio de sesión y consola/API administrativa desde el puesto administrado; Identity Center con MFA y roles aprobados, sin abrir entrada a la VPC.
- **L30:** Retornos establecidos permitidos por estado; no es una regla allow general.
- **C01:** Excepción pública justificada: consulta del saco de solo lectura; WAF y autorización de la vista.
- **C02:** Backend de consulta y health check cifrados; se concreta 443 y no 8080 en claro.
- **C03:** Entrada del backend solo desde el ALB, no desde internet ni todo el acopio.
- **C04:** Entrada al endpoint execute-api privado; no al ENI de una Lambda.
- **C05:** Carga privada de objetos con origen acotado a estaciones/servidores autorizados.
- **C06:** Escritura de lecturas mediante Gateway Endpoint; DynamoDB no tiene SG propio.
- **C07:** Archivo de telemetría por Gateway Endpoint y permisos del rol.
- **C08:** Lectura del objeto de confirmación del foco.
- **C09:** Persistencia del resultado; no autoriza fumigación.
- **C10:** Invocación privada de inferencia; endpoint y costo deben figurar en #22/#25/#29.
- **C11:** Entrada al endpoint de inferencia desde subredes de la función patrón.
- **C12:** Canal de logs; expansión por SG y por IP sin referencias egress entre VPC distintas.
- **C13:** Endpoint de CloudWatch Logs; clientes y subredes autorizados, no todos los acopios.
- **C14:** Solo clientes que realmente invocan KMS; el cifrado realizado por otro servicio usa su rol.
- **C15:** Endpoint KMS; el permiso de red no reemplaza la key policy.
- **C16:** Solo nodos administrados mediante agente SSM; sin entrada SSH permanente.
- **C17:** Endpoints ssm/ssmmessages; ec2messages solo si la versión del agente lo requiere.
- **C18:** Entrada al resolver híbrido desde los DNS locales concretos de VLAN 110.
- **C19:** Reenvío únicamente a DNS locales registrados y sus zonas; no retorno genérico.
- **C20:** Lectura de la vista del comprador; IAM restringe tabla/acciones/campos.
- **C21:** SG sin reglas ingress adicionales; no se intenta crear un deny en un SG.
- **C22:** Eliminar la salida allow-all creada por defecto; conservar retornos stateful.
- **N01:** Prioridad 10; una entrada por CIDR invitado. Defensa adicional al perímetro local.
- **N02:** Prioridad 100; SG mantiene el control fino por recurso y rol.
- **N03:** Prioridad 100; S3/DDB se expanden a CIDR reales, no IDs de prefix list en NACL.
- **N04:** Prioridad 110; consultas DNS TCP a resolvers autorizados por SG.
- **N05:** Prioridad 120; consultas DNS UDP.
- **N06:** Prioridad 110; consultas DNS y forwarding privado.
- **N07:** Prioridad 120; consultas DNS y forwarding privado.
- **N08:** Prioridad 130; retorno de conexiones salientes. NACL no comprueba estado; SG sí.
- **N09:** Prioridad 130; respuestas de HTTPS/DNS a clientes privados.
- **N10:** Prioridad 140; respuesta DNS al puerto efímero del cliente.
- **N11:** Prioridad 140; respuesta DNS al puerto efímero del cliente.
- **N12:** Prioridad 100; misma excepción pública de consulta que C01, a nivel de subred.
- **N13:** Prioridad 100; respuestas del ALB a clientes públicos; no es una nueva entrada pública.
- **N14:** Prioridad 110; conexión y health check del ALB hacia backend.
- **N15:** Prioridad 110; retorno del backend al ALB.
- **N16:** Entrada final * de NACL personalizada; no mantener allow-all de la ACL por defecto.
- **M01:** Excepción de telemetría con certificado activo y política por dispositivo/tema; nunca MQTT 1883.
- **M02:** Excepción de telemetría de posición: Cognito, viaje autorizado y límites; no habilita escrituras genéricas de sacos.
- **M03:** CIDR reales aprobados + identidad; vacío implica bloqueo. No se sustituye MOVIL-IP por acceso universal.
- **M04:** Excepción de ingreso de telemetría satelital: entrega autenticada del proveedor, validación de firma y antirreplay; sin operaciones de sacos ni objetos.
- **M05:** Resource policy: aws:SourceVpce y aws:VpcSourceIp; Cognito/MFA en aplicación.
- **M06:** Endpoint y bucket policies limitan recursos/roles y TLS; URL prefirmada no anula estas condiciones.
- **M07:** No abrir 443 o 8883 entrantes al ENI de Lambda por una invocación administrada.
- **T01:** Diagnóstico local excepcional; ticket, equipo /32, operador, aprobación y expiración ≤4 h. Fuera del filtro permanente.
- **T02:** Solo si SSM no sirve y existe esa instancia; /32 interno, ticket y expiración ≤4 h. No se añade a la Épica 6 por defecto.

## 4. Mapeo uno a uno y filtro para la Épica 6

El módulo mantiene el mismo ID en descripción, etiquetas cuando el recurso las soporte y documento de verificación de #23. `rule_catalog` es un contrato propuesto, no un recurso existente. La estructura mínima por entrada es `id`, `control`, `source`, `destination`, `protocol`, `from_port`, `to_port`, `action`, `permanence`, `component`, `owner` y, para temporales, `ticket`, `approved_by`, `expires_at` y `enabled=false`.

| Tipo de entrada | Destino de implementación propuesto | Qué se verifica |
|---|---|---|
| `sg_ingress[id]` | `aws_vpc_security_group_ingress_rule.permanent[id_expandido]` dentro de security | SG real de destino; una fuente CIDR/SG por recurso; no reglas ingress inline paralelas. |
| `sg_egress[id]` | `aws_vpc_security_group_egress_rule.permanent[id_expandido]` | Destino /32, SG compatible de la misma VPC o prefix list; no salida general por defecto. |
| `nacl_ingress/egress[id]` | `aws_network_acl_rule.permanent[id_expandido]` | Asociación de ACL a la subred correcta, dirección, número, CIDR y retorno; no usar SG/prefix list ID donde se exige un CIDR. |
| `service_policy[M01]` | Documento IoT por dispositivo/tema, consumido por `modules/ingest` y `modules/farm` | El broker público no tiene SG; TLS, identidad activa y permisos de publicación/recepción acotados. |
| `service_policy[M02–M05]` | Políticas de API/authorizer/WAF y contrato de adaptador, en el módulo dueño de cada servicio | Source IP/CIDR o SourceVpce explícitos, ruta/método, identidad y rate limiting; no inventar una regla SG para API pública. |
| `service_policy[M06]` | Política del endpoint S3 y bucket, consumida por red/función/almacenamiento | Restricción de endpoint, rol, bucket/prefijo y transporte seguro. |
| `local_policy[id]`, `host_policy[id]` | Una entrada por ID en `local_firewall_policy` exportada por security; aplicación en firewall/host/ACL local mediante el backend de gestión acordado | Conservar ID y parámetros en la configuración efectiva. Un output o archivo exportado no demuestra aplicación. |
| `assertions[id]` | Comprobación de configuración/política del componente y evidencia de verificación, no un `deny` ficticio de SG | Denegación implícita, ausencia de reglas extra y permisos de invocación de servicios. |
| T01/T02 | Flujo separado de incidente; no dentro del `for_each` de permanentes | Estado inicial apagado, aprobación, vencimiento y prueba de retirada. |

Regla de selección del módulo base: `permanence == "P"` **y** `component` perteneciente al patrón de un ambiente. Ser permanente es condición necesaria, no autorización para crear todas las aplicaciones del diagrama. El catálogo documenta también las políticas permanentes de la arquitectura completa que no se instancian en estas 100 horas.

Una fila de plantilla puede contener listas finitas: se expande por departamento, SG/CIDR, protocolo y AZ de forma determinista, por ejemplo `C04.cauca.host_01` o `N04.prod.aza.peer_01`. Cada recurso hijo conserva `parent_policy_id`; **cada hijo debe corresponder a exactamente una fila padre**, y cada instancia aplicable debe quedar cubierta. La expansión a TCP y UDP genera dos recursos cuando el proveedor los exige. No se permite añadir reglas de retorno, health check o egress «de conveniencia» fuera de este catálogo.

Las prioridades NACL de las condiciones son **órdenes de familias**, no números repetidos para cada CIDR. Para cada ACL y dirección, se ordenan las familias por prioridad y los CIDR normalizados dentro de cada familia; se asignan números únicos consecutivos desde 10, conservando N01 antes de cualquier permiso y el rechazo implícito al final. Se materializan únicamente las familias necesarias para la función de esa subred y sus respuestas, nunca las de todas las categorías indiscriminadamente. Antes del plan se valida el número de entradas contra la cuota efectiva de esa ACL y dirección, incluidos los CIDR expandidos de S3/DynamoDB. Si excede la cuota, se bloquea el plan y se revisa la distribución o la cuota; no se resume a un origen universal ni se omiten retornos para hacerlo caber.

No se crean recursos independientes para retornos de SG stateful ni para su deny implícito. Eso no es ausencia de control: se comprueba que el SG no contiene otros permisos. Las NACL sí tienen retorno explícito N08–N11/N13/N15, porque no mantienen estado [A1]. La comprobación «sin reglas extra» compara recursos efectivos contra el catálogo expandido por capa, no solo el número de filas del Markdown.

## 5. Semántica y puntos de aplicación

### Servicios públicos frente a subredes

`0.0.0.0/0` aparece como origen únicamente en C01/N12 para **consulta pública**, M01 para **telemetría MQTT**, M02 para **telemetría de posición HTTPS** y M04 para **entrega de telemetría satelital HTTPS**. C01/N12 son la misma excepción en capas diferentes. M02/M04 solo aceptan esquemas de telemetría y no convierten la API de negocio completa en una entrada universal. No hay SSH, RDP, consola, bucket de dron ni endpoint privado con origen universal. IPv6 público se mantiene deshabilitado en este patrón; no se añade `::/0` como atajo.

La telemetría móvil tiene IP variable; M01 usa certificado y política IoT, y M02 exige identidad del transportador y autorización del viaje. La consulta expone solo la vista del comprador y métodos de lectura; no un backend de administración. Los endpoints de IoT Core y API Gateway públicos son administrados: no se ubican artificialmente dentro de `SUB(telemetría)` ni reciben SG de la VPC. La subred de ingesta aloja, si están configuradas para VPC, las ENI de sus funciones.

La tabla resumida de #7 mencionaba 8883 entrante «desde IoT Core» a la subred, tráfico «desde S3» a la función y 80/8080 para consulta. Esta especificación concreta MQTT en el endpoint IoT, invocación de servicio para Lambda y **HTTPS 443** entre cliente, ALB y backend. No abre 8883 a Lambda ni 80/8080 por arrastre. Los listeners/health checks deben ajustarse al mismo protocolo antes de aplicar.

### Objetos de dron, VPN y DNS

Se conservan carga de objetos por S3 privado desde el acopio, dos túneles IPsec y Transit Gateway. C05 protege el endpoint de interfaz, M06 su acceso al bucket; S3 y DynamoDB no tienen SG propio. La URL prefirmada autoriza una operación, pero no permite atravesar una red o bucket policy que la prohíba. Un teléfono en 4G sin VPN no alcanza ese endpoint: el diseño integrado utiliza la estación/wifi del acopio para archivos; no se añade una entrada universal a S3 para resolverlo.

En NAT-T se usa UDP 4500 para los datos encapsulados e IKE 500; este perfil no añade ESP nativo como regla permanente. Si se acuerda IPsec sin NAT-T, se debe añadir y revisar explícitamente protocolo IP 50 entre peers concretos: no habilitar ambas variantes sin necesidad. No hay SG asociado a Transit Gateway o al extremo administrado de VPN; sus rutas, peers y opciones son de #22. TCP 179 se limita al interior de los túneles y no transporta usuarios. El firewall del CPE que haga NAT debe conservar el mismo alcance de peers.

El DNS privado usa resolver de entrada/salida y sus SG en hub según #7. Invitados reciben solo resolución pública. Reenvío de una zona no implica acceso a todas las redes de esa zona. Las referencias entre SG en distintas VPC/cuentas no se presuponen válidas: donde exista tránsito híbrido se usan los CIDR/IP autorizados y rutas de ida/vuelta. Las NACL no aceptan referencias SG ni alias FQDN.

### Administración y tráfico dentro de la VPC

La administración normal usa IAM Identity Center con MFA y, cuando haya instancias administradas, Session Manager mediante salida HTTPS a endpoints SSM [A3]. **No se crea una instancia de administración solo para justificar C16/C17**: si el componente no existe, no se instancia esa regla. No hay ingreso SSH permanente. La consola pública de AWS no es un listener dentro de una subred de administración.

KMS, Logs y Rekognition se alcanzan por endpoints privados para funciones asociadas a VPC. S3/DynamoDB usan Gateway Endpoints desde la VPC. Los endpoints de Logs/Rekognition/execute-api necesarios pero no detallados en #7 deben quedar explícitos en #22/#25 y en el costo; no se declara que ya existan ni se abre una salida universal si faltan. La selección de inferencia y la privacidad continúan en #16/#17.

Las NACL privadas permiten pares de prefijos a nivel de subred y los SG limitan qué recurso realmente recibe. Las entradas efímeras de NACL son permisos sin estado y no prueban que el paquete sea una respuesta: el control stateful del SG debe seguir activo. Los rangos deben ajustarse si los sistemas elegidos usan otros puertos de cliente; no se asume que la tabla haya pasado una prueba real.

Se mantiene el AWS Network Firewall previsto en la arquitectura de gobierno como punto de inspección de los caminos que se enruten por él. **No se le atribuye protección de todos los servicios administrados o de endpoints que lo eviten.** Su incorporación al patrón, rutas simétricas y reglas efectivas deben armonizarse con #22/#23; esta tabla no inventa un rule group de contenido ni sustituye SG/endpoint policies por la mera presencia de ese recurso. No se habilita un pass-all adicional para eludir esa revisión.

Las consultas al resolver proporcionado por AWS y ciertos servicios de plataforma tienen excepciones de filtrado propias de AWS; no se promete controlarlas mediante un SG común. Se verifican esas limitaciones antes de presentar un bloqueo completo de DNS. El tráfico lateral dentro de VLAN 110 se filtra en host/switch, tal como exige #8, no en un firewall que el paquete no atraviesa.

## 6. Entradas pendientes y controles temporales

Son entradas normales de despliegue las /32 de CPE y peers de VPN, IP de ENI, IDs de SG/endpoint y estaciones autorizadas. No tener aún sus valores no autoriza poner un origen más amplio. El plan debe rechazar valores vacíos para cualquier fila que se pretenda activar.

Quedan estas condiciones de activación:

1. **Aplicaciones móviles no telemétricas:** #6 contempla eventos de saco desde datos móviles. El criterio de #9 solo admite origen universal para consulta/telemetría. M03 propone una allowlist real y mantenida de rangos de acceso móvil más identidad; falta obtenerla y demostrar su cobertura. Si eso no es viable, el equipo debe revisar el criterio o el camino de esos eventos. No se oculta el conflicto usando «usuarios autenticados» como si fuera una restricción IP, ni se afirma que los eventos móviles estén habilitados sin ella.
2. **Adaptador satelital:** M04 pertenece a la excepción de ingreso de telemetría admitida por #9. Antes de activarlo se concreta el contrato de autenticación del proveedor, la validación de firma, marca de tiempo e identificador contra repetición; se rechaza antes de procesar cualquier entrega no válida. Si el proveedor publica CIDR estables se restringe también a ellos. Esa ruta no acepta cambios de custodia ni carga de archivos.

La automatización del firewall local también requiere confirmar proveedor/backend. El catálogo permite el cruce por ID, pero el cumplimiento literal de «todas las permanentes desplegadas por Terraform» no se acredita exportando una lista local. #23 debe definir el mecanismo o delimitar formalmente la parte cloud antes de declarar esa automatización completa. No se encubre esa diferencia con recursos SG que no pueden proteger una LAN física.

T01/T02 son plantillas de incidente inicialmente inactivas. Para activarlas se requiere objetivo individual, origen /32, ticket, responsable, aprobación del senior y `expires_at` con vigencia máxima propuesta de cuatro horas. La retirada debe ejecutarse y verificarse al vencer; escribir una fecha en una etiqueta no apaga una regla. El flujo temporal es separado del filtro permanente y no admite origen universal. No se incluyen credenciales ni secretos.

## 7. Verificación documental y aceptación

| Criterio | Evidencia y límite |
|---|---|
| Origen, destino, puerto, acción y permanencia en cada regla | Tabla única con IDs, P/T y condiciones enumeradas. Las reglas de invocación administrada indican expresamente que no hay un puerto de red. |
| Sin origen universal salvo consulta/telemetría | Solo C01/N12, M01, M02 y M04 lo utilizan, con propósito y condiciones explícitas; eventos móviles no telemétricos requieren su allowlist. No se permite un alias que se expanda a acceso universal sin revisión. |
| Mapeo uno a uno con security | Clave única por fila, traducción y expansión determinista de sección 4. Es una especificación para #23; el código todavía no existe. El backend local requiere acuerdo y prueba de aplicación. |

Comprobaciones realizadas en esta entrega: IDs únicos; campos obligatorios y P/T presentes; catálogo sin origen literal universal fuera de las excepciones; temporales marcadas deshabilitadas y excluidas del filtro; CIDR del patrón alineados con #7/#8; parejas de retorno NACL identificadas; enlaces y formato UTF-8/LF. No se ejecutaron pruebas de firewall ni `terraform plan` porque esta HU es documental y `iac` aún no contiene esos módulos.

Validación posterior mínima: desde Visitantes comprobar denegación TCP/UDP hacia Gerencia/Logística y gestión, manteniendo DNS público/navegación autorizada; desde Transporte denegar acceso lateral y permitir su telemetría autenticada; probar impresión solo desde puestos autorizados; comprobar TLS/identidad de MQTT y revocación; carga privada de dron con rol correcto y rechazo de origen ajeno; consulta pública exclusivamente de lectura; conmutación de túnel y DNS; y comprobar que no hay SSH público ni salida SG allow-all.

Para NACL se prueba solicitud **y respuesta**, incluido health check del ALB y retorno S3/DynamoDB, sin abrir nuevos puertos fuera del catálogo. Para cada prueba se retienen ambiente, ID de política, commit, resultado y evidencia. #23 publica `docs/iac/verificacion-iac-vs-firewall.md` con padre/hijo, recurso real y resultado; la igualdad de IDs por sí sola no demuestra que el tráfico siga el camino protegido.

## 8. Referencias

- [Historia #9](https://github.com/aromapacifico-platform/planning/issues/9), [#23 módulo de seguridad](https://github.com/aromapacifico-platform/planning/issues/23), [red integrada](red-direccionamiento-nube.md), [PR #53 de acopio](https://github.com/aromapacifico-platform/planning/pull/53) y [PR #49 de conectividad](https://github.com/aromapacifico-platform/planning/pull/49). Los commits consultados están identificados en sección 1.
- **[A1] AWS:** [SG stateful y NACL stateless](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html) y [control de subred con NACL](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html).
- **[A2] AWS IoT:** [protocolos y puertos de dispositivos](https://docs.aws.amazon.com/iot/latest/developerguide/protocols.html).
- **[A3] AWS:** [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) y [endpoints privados de SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-privatelink.html).
- **[A4] AWS:** [API privadas](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html) y [condiciones de origen en resource policies](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-resource-policies-examples.html).
- **[A5] AWS:** [endpoint privado de Rekognition](https://docs.aws.amazon.com/rekognition/latest/dg/vpc.html).
- **[A6] HashiCorp:** [reglas SG ingress independientes](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_ingress_rule).

Consulta técnica: 7 de noviembre de 2026. Las decisiones de cierre de puertos, backend HTTPS, perfiles de endpoints, allowlists y catálogo son propuestas de esta HU; no se presentan como cambios ya aprobados en #7 ni se modifica el registro transversal desde este archivo.
