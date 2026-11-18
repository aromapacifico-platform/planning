# Revisión Transversal de Consistencia (Código, Diagrama, Cifras y CIDRs)

## Plataforma Cafetera AromaPacífico (Federación Nacional de Cafeteros 2026)

**Historia:** #41. **Responsable:** Equipo Arquitectura & DevOps FNC 2026. **Fecha:** 17 de noviembre de 2026.  
**Estado:** Consolidado. **Fase:** Fase 7 - Revisión transversal y cierre.

---

## 1. Consistencia Código IaC (`iac/`) vs. Diagrama Consolidado (`vista-general.drawio`)

| Caja Diagrama | Qué representa en `vista-general.drawio` | Implementación verificada en `iac/` (rama `upgrades`) | Estado |
| --- | --- | --- | --- |
| **E6-01** | Estado remoto S3 + KMS + bloqueo por cuenta | `iac/bootstrap/` + `environments/{dev,test,prod}/backend.tf` y `backend.hcl` | Alineado |
| **E6-02** | VPC del ambiente (7 subredes en 2 AZs) + Gateway Endpoints S3/DynamoDB | `iac/modules/network/` integrado en `environments/{dev,test,prod}/main.tf` | Alineado |
| **E6-03** | Conexión VPN sitio a sitio con acopio parametrizado | `iac/modules/network/modules/hybrid/` + `environments/network/` | Alineado |
| **E6-04** | Llaves KMS, roles IAM sin comodines y reglas permanentes `#9` | `iac/modules/security/` integrado en `environments/{dev,test,prod}/main.tf` | Alineado |
| **E6-05** | Ingesta de telemetría (IoT Core policy/rules, SQS+DLQ, DynamoDB) | `iac/modules/ingest/` integrado en `environments/{dev,test,prod}/main.tf` | Alineado |
| **E6-06** | Finca patrón (IoT Thing, certificado X.509 CSR, etiqueta `FincaID`) | `iac/modules/farm/` integrado en `environments/{dev,test,prod}/main.tf` | Alineado |
| **E6-07** | Función de confirmación del foco (S3, Lambda, Rekognition/Bedrock, DLQ) | `iac/modules/function/` consumiendo rol de `security` (`PC-IAC-022`) | Alineado |
| **E6-08** | Pipeline CI/CD GitHub Actions con OIDC y compuerta de cosecha | `.github/.github/workflows/iac-{ci,cd}-reusable.yml` + `iac/.github/workflows/` | Alineado |

---

## 2. Consistencia de Direccionamiento IP (Cero Solapamiento)

| Segmento | Bloque CIDR | Uso | Solapamiento |
| --- | --- | --- | --- |
| Acopio Cauca | `10.41.0.0/16` | 7 VLANs locales (`.1`, `.2`, `.3`, `.4`, `.5`, `.10`, `.20`) | Ninguno |
| Acopio Huila | `10.42.0.0/16` | 7 VLANs locales | Ninguno |
| Acopio Tolima | `10.43.0.0/16` | 7 VLANs locales | Ninguno |
| AWS Desarrollo | `10.50.0.0/16` | VPC `dev` (7 subredes `/24` en 2 AZs) | Ninguno |
| AWS Pruebas | `10.60.0.0/16` | VPC `test` (7 subredes `/24` en 2 AZs) | Ninguno |
| AWS Producción | `10.70.0.0/16` | VPC `prod` en `us-east-1` | Ninguno |
| AWS Prod DR | `10.71.0.0/16` | VPC contingencia consulta pública en `us-east-2` | Ninguno |
| AWS Network Hub | `10.80.0.0/16` | Hub Transit Gateway + Route 53 Inbound | Ninguno |
| Azure Hub (Reserva) | `10.90.0.0/16` | Segunda nube preparada sin recursos | Ninguno |

---

## 3. Consistencia FinOps y Cifras del Caso

| Parámetro | Valor Verificado en Caso / Costos | Documentos Alineados |
| --- | --- | --- |
| Presupuesto mensual plataforma | **USD 811** (normal) / **USD 841** (cosecha) | `decisiones-ahorro.md`, `assumptions-log.md`, `vista-general.md`, `vista-general.drawio` |
| Conectividad sin señal (60 fincas) | **48 LoRaWAN** (10 gateways) + **12 Iridium SBD** (**USD 1.774/mes**) | `decisiones-ahorro.md`, `conectividad-sin-senal.md`, `vista-general.md`, `.drawio` |
| Alternativa descartada (SBD 100 %) | USD 8.820/mes (ahorro de USD 7.046/mes = USD 84.552/año) | `decisiones-ahorro.md`, `finops-framework.md` |
| Ingesta diaria en cosecha | 10.800 registros/día (1.200 cultivo + 2.400 secado + 7.200 transporte) | `enunciado-original.md`, `vista-general.md`, `carga-a-ingesta-telemetria.md` |
