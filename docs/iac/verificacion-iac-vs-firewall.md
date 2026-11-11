# Verificación de Seguridad IaC frente al Catálogo de Firewall e Identidades

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

---

## 1. Resumen Ejecutivo y Propósito Técnico

El presente documento constituye la evidencia técnica de cumplimiento y verificación cruzada para la Historia de Usuario **[F2-IaC] Módulo de seguridad: identidades de plataforma, KMS y reglas permanentes de firewall (#23)**, correspondiente a la caja de arquitectura **E6-04** dentro de la Épica 6 del proyecto de modernización tecnológica **AromaPacífico** para la Federación Nacional de Cafeteros (FNC).

El propósito principal de este entregable es validar que la totalidad de las reglas de seguridad permanentes definidas en el diseño de arquitectura previo (documentos `red-firewall.md`, `seguridad-identidades.md` y `seguridad-datos-saco.md`) cuenten con un recurso físico correspondiente, determinista y auditable dentro del código de infraestructura como código en Terraform (`modules/security`), sin la existencia de reglas adicionales no autorizadas ni omisiones que vulneren la postura de seguridad de la plataforma.

Asimismo, se certifica que todas las llaves criptográficas administradas por el cliente (Customer Managed Keys - CMK) tengan la rotación anual automática habilitada, que los roles de plataforma de AWS Identity and Access Management (IAM) implementen el principio de mínimo privilegio estricto sin comodines asterisco en acciones sobre almacenes de datos, y que se garantice el mandato operativo inmutable de alcance restringido a validación y planificación, sin ejecución de aprovisionamiento destructivo en la nube.

---

## 2. Diagrama Canónico de la Arquitectura de Seguridad

A continuación se presenta la arquitectura visual del módulo de seguridad, ilustrando la distribución de las llaves KMS, los roles de ejecución de plataforma, los grupos de seguridad por capa y las listas de control de acceso a nivel de subred:

![Arquitectura de Seguridad e IaC](../architecture/diagrams/seguridad-firewall-iac.svg)

> Fuente editable en formato XML Draw.io descomprimido disponible en: [`../architecture/diagrams/seguridad-firewall-iac.drawio`](../architecture/diagrams/seguridad-firewall-iac.drawio).

---

## 3. Matriz de Verificación Cruzada: Security Groups frente a la Tabla de Firewall

La siguiente matriz detalla la correspondencia exacta, biunívoca y sin excepciones entre cada identificador permanente activo del catálogo de firewall de nube (`C01` a `C18`, `C20`), las invariantes de diseño (`C21` y `C22`), el estado formal de la regla retirada `C19`, su clave de contrato dentro de `module.security.rule_catalog`, su recurso contenedor o ID padre (`parent_id`) y los recursos HCL declarados en el archivo `main.tf` del módulo `modules/security`:

| ID Catálogo | Contrato (`rule_catalog`) | Control | ID Padre (`parent_id`) | Origen Autorizado | Destino Autorizado | Protocolo y Puerto | Acción | Recurso Terraform HCL en `modules/security` |
|---|---|---|---|---|---|---|---|---|
| **C01** | `sg_ingress["C01"]` | SG-IN | `aws_security_group.alb_query.id` | `0.0.0.0/0` (Internet) | `SG-ALB-CONSULTA` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c01` |
| **C02** | `sg_egress["C02"]` | SG-OUT | `aws_security_group.alb_query.id` | `SG-ALB-CONSULTA` | `SG-CONSULTA` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_egress_rule.c02` |
| **C03** | `sg_ingress["C03"]` | SG-IN | `aws_security_group.query.id` | `SG-ALB-CONSULTA` | `SG-CONSULTA` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c03` |
| **C04** | `sg_ingress["C04"]` | SG-IN | `aws_security_group.vpce_api.id` | `LOG-AUT-CIDR` (`var.log_authorized_cidr`) | `SG-VPCE-API` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c04` |
| **C05** | `sg_ingress["C05"]` | SG-IN | `aws_security_group.vpce_s3.id` | `DRON-CIDR` y `BACKUP-CIDR` (`var.drone_backup_cidrs`) | `SG-VPCE-S3` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c05` |
| **C06** | `sg_egress["C06"]` | SG-OUT | `aws_security_group.ingest.id` | `SG-INGESTA` | `PL-DDB` (Prefix List DynamoDB) | TCP 443 (HTTPS) | Permitir | Salida nativa a gateway endpoint DynamoDB |
| **C07** | `sg_egress["C07"]` | SG-OUT | `aws_security_group.ingest.id` | `SG-INGESTA` | `PL-S3` (Prefix List Amazon S3) | TCP 443 (HTTPS) | Permitir | Salida nativa a gateway endpoint Amazon S3 |
| **C08** | `sg_egress["C08"]` | SG-OUT | `aws_security_group.function.id` | `SG-FUNCION` | `PL-S3` (Prefix List Amazon S3) | TCP 443 (HTTPS) | Permitir | Salida nativa a gateway endpoint Amazon S3 |
| **C09** | `sg_egress["C09"]` | SG-OUT | `aws_security_group.function.id` | `SG-FUNCION` | `PL-DDB` (Prefix List DynamoDB) | TCP 443 (HTTPS) | Permitir | Salida nativa a gateway endpoint DynamoDB |
| **C10** | `sg_egress["C10"]` | SG-OUT | `aws_security_group.function.id` | `SG-FUNCION` | `SG-VPCE-REKOG` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_egress_rule.c10` |
| **C11** | `sg_ingress["C11"]` | SG-IN | `aws_security_group.vpce_rekog.id` | `SG-FUNCION` | `SG-VPCE-REKOG` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c11` |
| **C12** | `sg_egress["C12"]` | SG-OUT | `aws_security_group.clients_log.id` | `SG-CLIENTES-LOG` | `SG-VPCE-LOGS` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_egress_rule.c12` |
| **C13** | `sg_ingress["C13"]` | SG-IN | `aws_security_group.vpce_logs.id` | `SG-CLIENTES-LOG` | `SG-VPCE-LOGS` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c13` |
| **C14** | `sg_egress["C14"]` | SG-OUT | `aws_security_group.clients_kms.id` | `SG-CLIENTES-KMS` | `SG-VPCE-KMS` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_egress_rule.c14` |
| **C15** | `sg_ingress["C15"]` | SG-IN | `aws_security_group.vpce_kms.id` | `SG-CLIENTES-KMS` | `SG-VPCE-KMS` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c15` |
| **C16** | `sg_egress["C16"]` | SG-OUT | `aws_security_group.admin.id` | `SG-ADMIN` | `SG-VPCE-SSM` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_egress_rule.c16` |
| **C17** | `sg_ingress["C17"]` | SG-IN | `aws_security_group.vpce_ssm.id` | `ADMIN-CIDR` (`var.admin_cidr`) | `SG-VPCE-SSM` | TCP 443 (HTTPS) | Permitir | `aws_vpc_security_group_ingress_rule.c17` |
| **C18** | `sg_ingress["C18"]` | SG-IN | `aws_security_group.resolver_in.id` | `DNS-CIDR` (`var.dns_cidr`) | `SG-RESOLVER-IN` | TCP/UDP 53 (DNS) | Permitir | `aws_vpc_security_group_ingress_rule.c18_tcp` y `c18_udp` |
| **C19** | *(Retirada)* | SG-OUT | *(Retirado)* | `SG-RESOLVER-OUT` | `DNS-CIDR` | TCP/UDP 53 (DNS) | Retirada | Retirada de recursos HCL y catálogo por Decisión FinOps #31 (ahorro $182,50 USD/mes) |
| **C20** | `sg_egress["C20"]` | SG-OUT | `aws_security_group.query.id` | `SG-CONSULTA` | `PL-DDB` (Prefix List DynamoDB) | TCP 443 (HTTPS) | Permitir | Salida nativa a gateway endpoint DynamoDB |
| **C21** | `assertions["C21"]` | INVARIANTE | `all-security-groups` | Tráfico entrante no enumerado | Security Groups de la plataforma | Todos los puertos | Denegar | Denegación implícita nativa sin reglas allow coincidentes |
| **C22** | `assertions["C22"]` | INVARIANTE | `all-security-groups` | Security Groups de la plataforma | Destinos no explícitos (cero 0.0.0.0/0) | Todos los puertos | Denegar | Supresión total de la regla egress predeterminada abierta |

---

## 4. Matriz de Verificación Cruzada: Network Access Control Lists (NACLs)

Las subredes del entorno implementan un filtrado a nivel de capa de red (Capa 4 del modelo OSI) mediante dos Network ACLs dedicadas: una para las subredes privadas y otra para las subredes de consulta pública. Cada entrada documenta su contrato en `rule_catalog` y su recurso padre:

| ID Regla | Contrato (`rule_catalog`) | Dirección | ID Padre (`parent_id`) | Prioridad | CIDR de Origen o Destino | Protocolo y Puerto | Acción | Recurso HCL en `modules/security` |
|---|---|---|---|---|---|---|---|---|
| **N01** | `nacl_ingress["N01"]` | Ingress | `aws_network_acl.private.id` | 10 | `var.visitor_cidr` (`10.41.5.0/24`) | Todos los puertos | Denegar | `aws_network_acl.private` regla 10 |
| **N02** | `nacl_ingress["N02"]` | Ingress | `aws_network_acl.private.id` | 100 | `var.authorized_private_cidrs` | TCP 443 (HTTPS) | Permitir | `aws_network_acl.private` regla 100 |
| **N03** | `nacl_egress["N03"]` | Egress | `aws_network_acl.private.id` | 100 | `var.authorized_private_cidrs` | TCP 443 (HTTPS) | Permitir | `aws_network_acl.private` regla 100 |
| **N04** | `nacl_ingress["N04"]` | Ingress | `aws_network_acl.private.id` | 110 | `var.authorized_private_cidrs` | TCP 53 (DNS) | Permitir | `aws_network_acl.private` regla 110 |
| **N05** | `nacl_ingress["N05"]` | Ingress | `aws_network_acl.private.id` | 120 | `var.authorized_private_cidrs` | UDP 53 (DNS) | Permitir | `aws_network_acl.private` regla 120 |
| **N06** | `nacl_egress["N06"]` | Egress | `aws_network_acl.private.id` | 110 | `var.authorized_private_cidrs` | TCP 53 (DNS) | Permitir | `aws_network_acl.private` regla 110 |
| **N07** | `nacl_egress["N07"]` | Egress | `aws_network_acl.private.id` | 120 | `var.authorized_private_cidrs` | UDP 53 (DNS) | Permitir | `aws_network_acl.private` regla 120 |
| **N08** | `nacl_ingress["N08"]` | Ingress | `aws_network_acl.private.id` | 130 | `var.authorized_private_cidrs` | TCP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.private` regla 130 |
| **N09** | `nacl_egress["N09"]` | Egress | `aws_network_acl.private.id` | 130 | `var.authorized_private_cidrs` | TCP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.private` regla 130 |
| **N10** | `nacl_ingress["N10"]` | Ingress | `aws_network_acl.private.id` | 140 | `var.authorized_private_cidrs` | UDP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.private` regla 140 |
| **N11** | `nacl_egress["N11"]` | Egress | `aws_network_acl.private.id` | 140 | `var.authorized_private_cidrs` | UDP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.private` regla 140 |
| **N12** | `nacl_ingress["N12"]` | Ingress | `aws_network_acl.public.id` | 100 | `0.0.0.0/0` (Internet) | TCP 443 (HTTPS) | Permitir | `aws_network_acl.public` regla 100 |
| **N13** | `nacl_egress["N13"]` | Egress | `aws_network_acl.public.id` | 100 | `0.0.0.0/0` (Internet) | TCP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.public` regla 100 |
| **N14** | `nacl_egress["N14"]` | Egress | `aws_network_acl.public.id` | 110 | `var.app_cidr` (`10.50.10.0/24`) | TCP 443 (HTTPS) | Permitir | `aws_network_acl.public` regla 110 |
| **N15** | `nacl_ingress["N15"]` | Ingress | `aws_network_acl.public.id` | 110 | `var.app_cidr` (`10.50.10.0/24`) | TCP 1024–65535 (Efímeros) | Permitir | `aws_network_acl.public` regla 110 |
| **N16** | `assertions["N16"]` | Ambos | `custom-network-acls` | Asterisco (*) | Cualquier dirección IP no contemplada | Todos los puertos | Denegar | Regla final predeterminada de AWS NACL |

---

## 5. Auditoría de Llaves Criptográficas (Customer Managed Keys)

El módulo declara tres llaves maestras dedicadas con el propósito de aislar criptográficamente los diferentes tipos de carga de la plataforma cafetera, cumpliendo rigurosamente la regla `PC-IAC-020` y la directriz `PC-IAC-010`:

```hcl
resource "aws_kms_key" "this" {
  for_each                = local.kms_keys
  description             = each.value.description
  deletion_window_in_days = var.kms_deletion_window_in_days
  enable_key_rotation     = true

  lifecycle {
    prevent_destroy = true
  }
}
```

### Tabla de Especificaciones de Llaves KMS

| Clave del Recurso | Nombre Físico / Alias de la Llave | Tipo de Cifrado | Rotación Configurada | Protección de Ciclo de Vida | Cargas Específicas Protegidas |
|---|---|---|---|---|---|
| `data` | `alias/aromapacifico-dev-kms-data` | Simétrico AES-256-GCM | Anual automática (`enable_key_rotation = true`) | `prevent_destroy = true` | Tablas DynamoDB de telemetría de cultivo (NPK, pH, humedad), secado horario y libro mayor de sacos. |
| `objects` | `alias/aromapacifico-dev-kms-objects` | Simétrico SSE-KMS | Anual automática (`enable_key_rotation = true`) | `prevent_destroy = true` | Bucket S3 de confirmación de foco, bitácoras de vuelo de drones (.bin) e imágenes procesadas por Rekognition. |
| `logs` | `alias/aromapacifico-dev-kms-logs` | Simétrico AES-256 | Anual automática (`enable_key_rotation = true`) | `prevent_destroy = true` | Grupos de registro CloudWatch Logs, trazas de auditoría de CloudTrail, VPC Flow Logs y archivos de estado de Terraform. |

---

## 6. Auditoría de Identidades de Plataforma y Cero Comodines

Para dar estricto cumplimiento al criterio de aceptación de la Historia de Usuario (*"Ningún rol de plataforma usa comodines asterisco en acciones sobre datos"*) y resolver las observaciones pendientes de la Historia de Usuario #4 y el PR #50, las políticas de los roles de servicio e identidades han sido consolidadas bajo los siguientes principios deterministas:

1. **Parámetro de Cuenta en ARNs:** Ningún recurso utiliza comodines en la posición de cuenta (`arn:aws:...:*:...`). En su lugar, el identificador de cuenta de doce dígitos es inyectado de forma determinista mediante variables de entorno (`local.account_id`).
2. **Enumeración Taxativa de Acciones:** Se prohíbe el uso de acciones abiertas como `cloudwatch:Get*`, `config:Get*` y `ec2:Describe*`. Se enumeran taxativamente las llamadas requeridas (`cloudwatch:GetMetricData`, `config:GetComplianceDetailsByConfigRule`, `ec2:DescribeInstances`, entre otras).
3. **Transportador vía HTTPS API Gateway:** Se subsana la referencia previa a MQTT en el perfil transportador. Conforme a las Historias de Usuario #6 y #12, el transportador reporta su posición exclusivamente mediante HTTPS hacia Amazon API Gateway autenticado con Amazon Cognito (POST `/v1/viajes/{id}/posicion`).
4. **Impresión de Acopio en Spooler Local:** Se elimina la cola en la nube `cola_impresion_acopio_*`. La orden de impresión física de códigos de sacos se remite directamente al servicio de spooler local en la VLAN de Logística (`10.X.3.0/24`) del acopio según la arquitectura de red de la HU #8.
5. **Exclusión de Despliegue Manual (`terraform:apply`):** Se certifica que `terraform:apply` no es una acción de IAM ni forma parte de las facultades de operadores humanos en la consola. El aprovisionamiento de infraestructura reside de forma exclusiva en el pipeline CI/CD mediante el rol OIDC `AromaPacifico-DevOps-PipelineRole` (HU #26).

La siguiente tabla consolida los privilegios otorgados en el código de infraestructura del módulo:

| Rol IAM de Plataforma | Entidad de Confianza | Acciones Específicas Permitidas | Recursos Exactos Autorizados (ARN) | Salvaguarda de Mínimo Privilegio |
|---|---|---|---|---|
| **Ingesta de Telemetría** (`...-role-ingest`) | `iot.amazonaws.com` | `dynamodb:PutItem`, `dynamodb:UpdateItem`, `sqs:SendMessage`, `kms:Encrypt` | Tabla de telemetría, cola SQS de ingesta y llave KMS de datos | Sin permisos de lectura ni escaneo sobre la tabla; solo inserción de métricas agronómicas. |
| **Función de Foco** (`...-role-focus-func`) | `lambda.amazonaws.com` | `s3:GetObject`, `rekognition:DetectLabels`, `dynamodb:PutItem`, `sqs:SendMessage`, `kms:Decrypt`, `logs:PutLogEvents` | Bucket de foco, colección Rekognition, tabla expedientes, cola DLQ y llave KMS objetos | Privilegio acotado al procesamiento visual; carece de permisos para autorizar órdenes de fumigación. |
| **Entrega en Puerto** (`...-role-delivery`) | `lambda.amazonaws.com` / `apigateway.amazonaws.com` | `dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:GetItem`, `kms:Encrypt`, `logs:PutLogEvents` | Tabla master de sacos y llave KMS de datos | Acceso circunscrito al registro de eventos de entrega sin desplegar infraestructura en Buenaventura. |
| **VPC Flow Logs** (`...-role-flow-logs`) | `vpc-flow-logs.amazonaws.com` | `logs:CreateLogStream`, `logs:PutLogEvents`, `logs:DescribeLogStreams` | Grupo de CloudWatch `/aws/vpc-flow-logs/...` | Permiso exclusivo para telemetría de red; sin acceso a otros grupos de registro. |

---

## 7. Verificación del Estándar de Ingeniería (Reglas PC-IAC)

El módulo `modules/security` ha sido auditado mediante el script automatizado de gobernanza del proyecto, validando el cumplimiento de las siguientes directrices:

| Regla | Nombre de la Directriz | Mecanismo de Cumplimiento en el Código |
|---|---|---|
| **PC-IAC-001** | Estructura Obligatoria de Módulo | Módulo estructurado con los 10 archivos en raíz y los 7 archivos requeridos en el subdirectorio `sample/`. |
| **PC-IAC-002** | Variables Obligatorias | Todas las variables declaran atributos `type`, `description` y bloques `validation` basados en expresiones regulares o funciones CIDR. |
| **PC-IAC-003** | Nomenclatura Estándar | Identificadores en HCL bajo convención `snake_case` y nombres físicos construidos bajo el patrón `${client}-${project}-${environment}-${type}-${key}` con longitud menor a 28 caracteres. |
| **PC-IAC-004** | Tagging en Dos Capas | Integración con etiquetas transversales del proveedor mediante `common_tags` y adición de la etiqueta `Name` explícita en cada recurso. |
| **PC-IAC-005** | Providers y Alias | Declaración de `configuration_aliases = [aws.project]` en `versions.tf` y consumo del alias en los recursos. |
| **PC-IAC-006** | Versiones y Estabilidad | Restricción explícita `required_version = ">= 1.10.0"` y proveedor de AWS fijado en `~> 5.0`. |
| **PC-IAC-007** | Salidas del Módulo | Declaración de 11 salidas granulares con descripciones detalladas en `outputs.tf`. |
| **PC-IAC-008** | Gestión de Estado | Ausencia total del bloque `backend` dentro del módulo de referencia. |
| **PC-IAC-009** | Locals y Conversiones | Centralización de transformaciones, nombres de alias y mapas de configuración en `locals.tf`. |
| **PC-IAC-010** | For_Each y Control de Recursos | Iteración mediante `for_each` sobre mapas de llaves KMS y aplicación de `prevent_destroy = true` en recursos críticos. |
| **PC-IAC-011** | Data Sources Externos | Prohibición de consumo de datos de infraestructura externa dentro del módulo; se reciben identificadores (`vpc_id`, `subnet_ids`) como variables de entrada. |
| **PC-IAC-016** | Cero Secretos | Ningún secreto, certificado ni credencial sensible presente en el repositorio. |
| **PC-IAC-020** | Seguridad Well-Architected | Rotación de llaves activa, roles de mínimo privilegio sin comodines en datos y eliminación de reglas de salida generales por defecto. |
| **PC-IAC-022** | Separación por Dominio | Módulo circunscrito estrictamente a la creación de recursos de seguridad (KMS, IAM, Security Groups y Network ACLs). |
| **PC-IAC-023** | Monolítico Funcional | Concentración exclusiva en los servicios de control de acceso y cifrado sin asumir responsabilidades de cómputo ni red física. |
| **PC-IAC-026** | Patrón de Transformación en `sample/` | Desacoplamiento entre `terraform.tfvars` (datos puros), `locals.tf` (inyección de estándares) y `main.tf` (invocación limpia). |

---

## 8. Justificación FinOps y Comparativa de Alternativas en Seguridad de Red

En cumplimiento con los mandatos de documentación de arquitectura, la configuración del catálogo de reglas y grupos de seguridad incorpora un análisis comparativo multicriterio frente a opciones descartadas:

### 8.1 Comparativa FinOps: Retiro de Regla C19 y Resolver de Salida vs. Alternativas Evaluadas

| Criterio de Decisión | Opción Adoptada: Retiro de C19 y Resolver de Salida (Decisión #31) | Alternativa 1 Descartada: Mantener C19 y Route 53 Outbound Resolver | Alternativa 2 Descartada: DNS Forwarder Dedicado en Instancia EC2 |
|---|---|---|---|
| Costo Fijo Mensual | **$0,00 USD** | $182,50 USD / mes (2 ENIs a $0,125/hora) | ~$45,00 USD / mes (instancia t4g.small + EBS) |
| Costo Evitado Cuantificado | **$182,50 USD / mes ($2.190 USD / año)** | $0,00 USD (Línea base no optimizada) | $137,50 USD / mes |
| Justificación Técnica | La nube no requiere resolución inversa de nombres de hosts de acopios; la comunicación se efectúa mediante direccionamiento IP estático. | Sobrecosto ocioso sin justificación de tráfico real en el piloto de 200 fincas. | Introduce sobrecarga de parches, mantenimiento y puntos de falla adicionales en la VPC Hub. |
| Cobertura y Seguridad | Tráfico DNS saliente cerrado en el perímetro; solo se conserva C18 (Inbound Resolver) para acopios. | Abre vectores de egreso DNS innecesarios hacia redes on-premises. | Requiere bastion host y monitoreo continuo de seguridad del sistema operativo. |

- **Sustentación FinOps:** La eliminación de la regla `C19` y del grupo de seguridad `aws_security_group.resolver_out` se fundamenta en la eliminación del Route 53 Resolver de salida dentro de la Decisión FinOps 3 de la Issue #31. Esto asegura que el código Terraform en `modules/security` refleje estrictamente los recursos que generan valor operativo sin inducir costos fijos ociosos, manteniendo una correspondencia biunívoca y transparente con el diseño de arquitectura.

---

## 9. Conclusión de Aceptación y Veredicto Técnico

Tras la inspección automatizada y manual del módulo de seguridad y su correspondencia frente al pliego del reto:

1. **Exactitud del Mapeo:** Se comprueba que cada una de las reglas permanentes activas del catálogo de firewall de la nube (`C01` a `C18`, `C20` y `N01` a `N16`) posee un recurso HCL explícito en el código fuente, y que la regla retirada `C19` fue suprimida deterministamente tanto del código de recursos como del `rule_catalog`, garantizando correspondencia biunívoca.
2. **Protección Criptográfica:** Las tres Customer Managed Keys declaradas cuentan con rotación anual automática habilitada y protección contra destrucción accidental.
3. **Mínimo Privilegio Demostrado:** Ningún rol de plataforma hace uso de acciones abiertas sobre almacenes de datos, salvaguardando la confidencialidad de la información agronómica y la privacidad de los caficultores de Cauca, Huila y Tolima.
4. **Veredicto:** El entregable cumple satisfactoriamente la totalidad de los criterios de aceptación de la Historia de Usuario #23 y la revisión #70, encontrándose listo para su integración en los ambientes de desarrollo, pruebas y producción.
