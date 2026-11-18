# Evidencia de Ejecución del Plan Limpio de Infraestructura IaC (`terraform plan`)

**Historia:** #27 (`[F2-IaC] Ejecutar y documentar un plan limpio del ambiente`)  
**Fecha de evidencia:** 2026-11-17  
**Repositorio objetivo:** `aromapacifico-platform/iac`  
**Rama / Commit base verificado:** `upgrades` (base `ab383b01f8e233906cf6fb52a8f5c0300470c978`, integrando remediaciones locales de `TASK1`, `TASK2` y `TASK3`)  
**Cuenta AWS / Región verificada (solo lectura):** `273577169715` (`arn:aws:iam::273577169715:user/pacheco-developer`) en `us-east-1`  
**Estado de ejecución remota CI/CD:** Pendiente de push a `origin` y disparo de GitHub Actions tras fusión de PRs abiertos (`iac#7` y `iac#10`) hacia `main`.

---

## 1. Resumen Ejecutivo y Alcance Cero Apply

El presente documento registra la evidencia técnica de la ejecución limpia y sin errores del `terraform plan` integrado sobre los cinco módulos de la Épica 6 (`network`, `security`, `ingest`, `farm` y `function`) en los ambientes `dev`, `test` y `prod` de AromaPacífico (FNC 2026).

En cumplimiento estricto de la regla de alcance **Cero Apply** (`AGENTS.md` sección 2.9), no se ejecutó `terraform apply` ni se aprovisionó ningún recurso real en AWS. Debido a que los buckets remotos de estado (`aromapacifico-tfstate-<env>`) de `bootstrap/` no han sido aprovisionados en vivo bajo el mismo mandato, la planificación especulativa empleó el mecanismo documentado de respaldo temporal con backend `local` (equivalente al flujo de `.github/workflows/iac-cd-reusable.yml`, líneas 98–107), descartando los artefactos temporales inmediatamente después de capturar la salida del plan.

### Resultado consolidado por ambiente

| Ambiente | Bloque CIDR VPC | Resultado del `terraform plan` | Recursos a crear | Cambios / Destrucciones | Errores |
| --- | --- | --- | ---: | ---: | ---: |
| **dev** | `10.50.0.0/16` | Plan limpio (`exit code 0`) | 116 | `0 to change, 0 to destroy` | 0 |
| **test** | `10.60.0.0/16` | Plan limpio (`exit code 0`) | 116 | `0 to change, 0 to destroy` | 0 |
| **prod** | `10.70.0.0/16` | Plan limpio (`exit code 0`) | 116 | `0 to change, 0 to destroy` | 0 |

---

## 2. Correspondencia con Cajas de Arquitectura (`E6-01` a `E6-08`)

La siguiente tabla detalla la trazabilidad exacta entre cada caja del diagrama de arquitectura (Épica 6) y los **116 recursos** generados por `terraform plan` en el ambiente raíz integrado (`environments/dev`):

| Caja | Módulo / Componente | Cantidad | Recursos principales planeados en `terraform plan` |
| --- | --- | ---: | --- |
| **E6-01** | `bootstrap/` + `environments/*/backend.tf` | N/A | Contrato `backend "s3" {}` con `backend.hcl` cifrado SSE-KMS (`alias/aromapacifico-tfstate`) y bloqueo nativo `use_lockfile = true`; ejecución especulativa mediante estado temporal local sin aprovisionamiento. |
| **E6-02** | `module.network` (VPC y Endpoints) | 48 | `aws_vpc.this` (`10.50.0.0/16`), `aws_internet_gateway.this`, 14 `aws_subnet.this` (2 AZs), 14 `aws_route_table.this`, 14 `aws_route_table_association.this`, 2 `aws_route.public_internet`, `aws_vpc_endpoint.gateway["s3"]` y `aws_vpc_endpoint.gateway["dynamodb"]` con políticas sin comodines. |
| **E6-03** | `module.network` (Acopio híbrido) | 0 | Parámetro `collection_center_department = 41` (`ACOPIO-CAUCA`, `10.41.0.0/16`, BGP ASN `65041`) preparado con `transit_gateway_id = null` (`transit_gateway_attachment_id = null` en reposo sin solape CIDR). |
| **E6-04** | `module.security` (KMS, IAM, Firewall) | 45 | 3 `aws_kms_key.this` (`data`, `objects`, `logs` con rotación anual) y 3 `aws_kms_alias.this`; 4 `aws_iam_role` + 4 `aws_iam_role_policy` (`ingest`, `focus_function`, `delivery`, `flow_logs`); 14 `aws_security_group`; 15 `aws_vpc_security_group_{ingress,egress}_rule` (`C01`–`C18` con retiro de `C19`); 2 `aws_network_acl` (`private`, `public`). |
| **E6-05** | `module.ingest` (Telemetría IoT) | 7 | `aws_dynamodb_table.this["telemetry"]` (con GSI `history`, PITR, SSE-KMS y sin TTL), `aws_dynamodb_table.this["thresholds"]`, `aws_sqs_queue.this`, `aws_sqs_queue.dead_letter`, `aws_sqs_queue_redrive_allow_policy.this`, `aws_iot_policy.this` y `aws_iot_topic_rule.this`. |
| **E6-06** | `module.farm` (Finca patrón) | 4 | `aws_iot_thing.this` (`fnc-aromapacifico-dev-thing-cau-f001`), `aws_iot_certificate.this` (`active = false`, CSR público externo), `aws_iot_policy_attachment.this` y `aws_iot_thing_principal_attachment.this`. |
| **E6-07** | `module.function` (Confirmación foco) | 12 | `aws_s3_bucket.this` más endurecimiento (`ownership_controls`, `public_access_block`, `server_side_encryption_configuration`, `versioning`, `bucket_policy` TLS, `bucket_notification`), `aws_sqs_queue.dlq`, `aws_cloudwatch_log_group.this`, `aws_lambda_function.this`, `aws_lambda_function_event_invoke_config.this` y `aws_lambda_permission.allow_s3`. |
| **E6-08** | `.github/workflows/` (CI/CD OIDC) | N/A | Callers `iac-ci-pr.yml` y `iac-cd-platform.yml` pinneados a `@v1.1.0`; compuerta horaria de cosecha (`check_harvest_window.py`) y pruebas automatizadas `terraform test`. |
| **Total** | **Stack completo de ambiente** | **116** | **116 recursos planeados (`116 to add, 0 to change, 0 to destroy`), 0 errores.** |

---

## 3. Salida Capturada del `terraform plan` (`environments/dev`)

```text
module.function.data.archive_file.lambda_zip: Reading...
module.function.data.archive_file.lambda_zip: Read complete after 0s [id=fec860dd1dd8a77be09dcfd676c175bdb9024325]
module.function.data.aws_region.current: Reading...
module.function.data.aws_caller_identity.current: Reading...
module.security.data.aws_caller_identity.current: Reading...
module.function.data.aws_partition.current: Reading...
module.function.data.aws_partition.current: Read complete after 0s [id=aws]
module.function.data.aws_region.current: Read complete after 0s [id=us-east-1]
module.security.data.aws_region.current: Reading...
module.security.data.aws_region.current: Read complete after 0s [id=us-east-1]
data.aws_caller_identity.current: Reading...
module.security.data.aws_caller_identity.current: Read complete after 0s [id=273577169715]
module.security.data.aws_iam_policy_document.kms_key_policy["logs"]: Reading...
module.security.data.aws_iam_policy_document.kms_key_policy["data"]: Reading...
module.security.data.aws_iam_policy_document.kms_key_policy["objects"]: Reading...
module.security.data.aws_iam_policy_document.kms_key_policy["logs"]: Read complete after 0s [id=2028724806]
module.security.data.aws_iam_policy_document.kms_key_policy["objects"]: Read complete after 0s [id=2028724806]
module.security.data.aws_iam_policy_document.kms_key_policy["data"]: Read complete after 0s [id=2028724806]
data.aws_caller_identity.current: Read complete after 0s [id=273577169715]
module.function.data.aws_caller_identity.current: Read complete after 0s [id=273577169715]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

... (116 recursos planeados: module.farm[4], module.function[12], module.ingest[7], module.network[48], module.security[45]) ...

Plan: 116 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + farm           = {
      + certificate_arn = (known after apply)
      + thing_name      = "fnc-aromapacifico-dev-thing-cau-f001"
    }
  + function       = {
      + iam_role_arn         = (known after apply)
      + lambda_function_arn  = (known after apply)
      + lambda_function_name = "fnc-aromapacifico-dev-fn-focus-conf"
      + s3_bucket_id         = (known after apply)
      + sqs_dlq_arn          = (known after apply)
    }
  + ingest         = {
      + config_topic    = "aromapacifico/fincas/CAU-F001/config"
      + error_queue_url = (known after apply)
      + mqtt_topics     = {
          + cultivo = "$aws/rules/fnc_aromapacifico_dev_telemetry/aromapacifico/fincas/CAU-F001/telemetria/cultivo"
          + secado  = "$aws/rules/fnc_aromapacifico_dev_telemetry/aromapacifico/fincas/CAU-F001/telemetria/secado"
        }
      + tables          = {
          + telemetry  = {
              + arn        = (known after apply)
              + name       = "fnc-aromapacifico-dev-dynamo-telemetry"
              + stream_arn = (known after apply)
            }
          + thresholds = {
              + arn        = (known after apply)
              + name       = "fnc-aromapacifico-dev-dynamo-thresholds"
              + stream_arn = (known after apply)
            }
        }
    }
  + name_prefix    = "aromapacifico-dev"
  + network        = {
      + collection_center = {
          + bgp_asn           = 65041
          + cidr              = "10.41.0.0/16"
          + id                = "ACOPIO-CAUCA"
          + operational_cidrs = {
              + logistics = "10.41.3.0/24"
              + servers   = "10.41.10.0/24"
            }
        }
      + transit_gateway_attachment_id = null
    }
```

### Validaciones complementarias verificadas

- `terraform fmt -check -recursive` sobre `modules/` y `environments/{network,dev,test,prod}`: código de salida `0`.
- `terraform validate` en `environments/dev`, `environments/test`, `environments/prod`, `environments/network`, `modules/security/sample` y `modules/function/sample`: válido sin errores.
- `terraform test`: `modules/security` (`7/7`), `modules/function` (`4/4`), `environments/network` (`7/7`) y `environments/dev` (`7/7`).
- `validate_iac_rules.py --strict-warnings`: `[SUCCESS]` (0 errores y 0 advertencias) en los 5 módulos y en los 4 roots (`dev`, `test`, `prod`, `network`).

---

## 4. Comparativa de Esfuerzo frente al Plan de 100 Horas

De acuerdo con el presupuesto de esfuerzo establecido en [plan-100-horas.md](plan-100-horas.md) (máximo **100 horas / 10 días hábiles** para todo el código ejecutable de Épica 6), se presenta el seguimiento comparativo por tarea. Dado que el repositorio no almacena hojas de tiempo individuales por desarrollador, las horas registradas reflejan el presupuesto asignado y el estado de entrega verificado en el código; cualquier ajuste final queda sujeto al cierre remoto de PRs en GitHub.

| Tarea | Issue | Caja | Asignación planeada (h) | Estado técnico verificado | Desviación / Observación de alcance |
| --- | --- | --- | ---: | --- | --- |
| T1 · Base, backend y variables | `#21` | E6-01 | 6 | Implementada y alineada (`use_lockfile`, 7 tags) | Sin exceso de alcance; validada en los 4 roots. |
| T2 · Módulo `network` | `#22` | E6-02, E6-03 | 22 | Implementada (`48` recursos, 7/7 tests) | Retiro de Network Firewall y Route 53 Outbound (`#70`). |
| T3 · Módulo `security` | `#23` | E6-04 | 18 | Implementada (`45` recursos, 7/7 tests) | Regla `C19` retirada; cero comodines IAM en datos. |
| T4 · Pipeline CI/CD OIDC | `#26` | E6-08 | 10 | Callers pinneados a `@v1.1.0` + scripts | Pendiente sincronización de mejoras en `.github` (`TASK5`). |
| T5 · Módulos `ingest` y `farm` | `#24` | E6-05, E6-06 | 24 | Implementados y cableados en `dev`, `test`, `prod` | Pendiente cierre formal de PR `#7` en GitHub. |
| T6 · Módulo `function` | `#25` | E6-07 | 16 | Implementada (`12` recursos, 4/4 tests) | Bucket S3 endurecido TLS + Lambda privada + DLQ. |
| T7 · Plan limpio y evidencia | `#27` | Todas | 4 | Plan limpio ejecutado (`116` recursos en `dev`, `test`, `prod`) | Evidencia documentada en este archivo; falta ejecución remota en Actions tras merge. |
| **Total** | | | **100** | **100 % de los módulos integrados y planificados** | **Dentro del tope de 100 h; Cero Apply respetado.** |

---

## 5. Sustentación FinOps del Enfoque de Planificación y Arquitectura Desplegable

La estrategia de validación especulativa y la topología de los 116 recursos planeados priorizan costo `$0,00 USD` en reposo y evitan erogaciones innecesarias tanto durante el desarrollo de Épica 6 como en operación continua:

| Alternativa evaluada | Costo en fase de validación / reposo (USD/mes) | Costo evitado / Ahorro (USD/mes) | Riesgo técnico y cumplimiento | Decisión |
| --- | ---: | ---: | --- | --- |
| **1. Aprovisionamiento real por PR (`terraform apply` en dev/test/prod)** *(Descartada)* | `~USD 40–120/mes` en recursos persistentes o tráfico de pruebas y riesgo de huérfanos | `$0,00` de ahorro; viola mandato Cero Apply | Genera costos reales antes de aprobación y expone buckets/endpoints sin gobernanza de cierre | **Rechazada** |
| **2. Arquitectura previa con AWS Network Firewall + Route 53 Outbound Resolver (`C19`)** *(Descartada)* | `USD 774,78/mes` fijos en reposo (endpoints de inspección y resolver) | Supera por sí sola el presupuesto base (`USD 811/mes`) | Redundante frente a Gateway Endpoints S3/DynamoDB (`$0/GB`) y SGs/NACLs permanentes | **Rechazada** (Decisión `#31` / `#70`) |
| **3. Planificación especulativa OIDC (`terraform plan` Cero Apply) + Gateway Endpoints S3/DynamoDB + Lambda/DynamoDB On-Demand** *(Adoptada)* | **`USD 0,00` en validación Cero Apply** (`$0/GB` en Gateway Endpoints; serverless en reposo) | **`USD 774,78/mes` evitados** en red/firewall y `$0,00` gastados en cuentas durante Épica 6 | Verifica los 116 recursos y sus políticas sin mutar infraestructura AWS real | **Adoptada** |

---

## 6. Cumplimiento Jurídico (Ley 1581 de 2012)

1. El plan especulativo certifica que los datos operativos del caficultor permanecen cifrados en reposo con CMKs independientes de KMS (`data`, `objects`, `logs`) y rotación anual automática habilitada, sin mezcla con la capa pública de consulta del saco.
2. Ninguna credencial estática, llave privada de dispositivo IoT (`farm_certificate_csr` usa CSR público sin llave privada en el estado) ni dato personal sensible reside en archivos `.tfvars`, salidas o planes almacenados.
