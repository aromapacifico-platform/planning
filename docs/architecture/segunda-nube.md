# Segunda nube preparada: Azure

## Qué pide el enunciado

Quien presenta elige la nube principal y deja preparada una segunda, sin duplicar la plataforma.
La nube principal es AWS (`us-east-1`, con `us-east-2` de respaldo para la consulta del saco) y la
segunda es Microsoft Azure, según las decisiones base del proyecto.

"Preparada" en este documento significa que el día que haga falta usar Azure ya están decididos el
rango de red, la forma de conectarse, la identidad, el DNS y el lugar donde va el código. No hay
nada creado ni facturando en Azure. El costo de la segunda nube durante el piloto es cero.

## 1. Qué se movería primero y por qué

La primera pieza candidata es la **consulta pública del saco**:

- Es la única parte de la plataforma abierta a internet y la que tiene el compromiso de
  disponibilidad más alto (99,9 % mensual, RTO de 4 horas).
- Solo lee. No recibe telemetría, no maneja certificados de dispositivos ni órdenes de fumigación.
- Sus datos ya salen anonimizados: origen, fechas de proceso, estado y variables de secado. No lleva
  la cédula del caficultor ni la traza completa, así que llevarla a otra nube no mueve datos
  personales.
- Es pequeña. En pico de cosecha entran hasta 1.200 sacos al día y se leen hasta 30 consultas por
  minuto.

Lo que **no** se movería a Azure: la ingesta de telemetría, la identidad de los nodos y drones, las
órdenes de fumigación y los datos personales. Esas piezas dependen de IoT Core, de los
certificados X.509 y de la auditoría centralizada en la cuenta de seguridad de AWS. Duplicarlas sí
sería duplicar la plataforma.

La segunda candidata, si algún día se justifica, es el **servicio de inferencia**. La función de
confirmación del foco llama a un servicio de visión administrado; cambiar Rekognition por Azure AI
Vision afecta a esa llamada, no al resto del flujo. No se prepara nada más para este caso.

## 2. Rango de red reservado

| Bloque | Uso | Estado |
|---|---|---|
| `10.90.0.0/16` | VNet hub de Azure (gateway VPN y servicios de la consulta del saco) | Reservado, sin crear |

El bloque no se solapa con nada que ya exista o esté reservado:

| Bloque existente | Dueño |
|---|---|
| `10.41.0.0/16`, `10.42.0.0/16`, `10.43.0.0/16` | Centros de acopio de Cauca, Huila y Tolima |
| `10.50.0.0/16`, `10.60.0.0/16`, `10.70.0.0/16` | VPC de desarrollo, pruebas y producción en `us-east-1` |
| `10.71.0.0/16` | VPC de contingencia de producción en `us-east-2` |
| `10.80.0.0/16` | VPC hub de red compartida |

El segundo octeto de cada bloque es distinto (41, 42, 43, 50, 60, 70, 71, 80 y 90) y todos son
`/16`, así que ningún par de rangos comparte direcciones.

Los rangos de AWS salen del plan de direccionamiento de la #7, que está en revisión (PR #46). Si
ese plan cambia, esta tabla se actualiza; el bloque de Azure se eligió lejos de los rangos que hoy
usan AWS y los acopios para que un ajuste pequeño no lo afecte.

## 3. Cómo se conectaría con AWS

Si se activa, Azure se conecta al **Transit Gateway de la cuenta de red** de AWS, igual que los
centros de acopio:

- Una VPN sitio a sitio con IPsec entre el Transit Gateway y un VPN Gateway de Azure en la VNet hub
  `10.90.0.0/16`.
- Enrutamiento dinámico con BGP. Se reservan los ASN privados `64512` para el Transit Gateway y
  `65515` para el VPN Gateway de Azure (el valor por defecto de cada lado).
- Una tabla de rutas propia para Azure en el Transit Gateway, que solo propaga hacia la subred de
  consulta pública de producción. Azure no ve las subredes de ingesta, de drones ni de datos, ni
  las redes de los acopios.

La conexión no se usa para servir la consulta a los compradores, que entra por internet. Solo
sirve para copiar la vista anonimizada de los sacos de AWS a Azure.

## 4. Identidad

| Quién | Cómo entra hoy en AWS | Qué queda preparado para Azure |
|---|---|---|
| Ingenieros de plataforma | IAM Identity Center con MFA | Un solo directorio de personas para las dos nubes. Si la Federación ya usa Microsoft Entra ID, se conecta como fuente de identidad de IAM Identity Center (SAML 2.0 y SCIM). Si no, Identity Center sigue como directorio y Azure se federa contra él. La decisión se confirma con la Federación |
| Pipeline de GitHub Actions | OIDC contra AWS, sin llaves guardadas | El mismo patrón contra Azure: una credencial federada de OIDC en una identidad de aplicación de Entra ID, también sin secretos |
| Compradores en la consulta pública | No inician sesión | Igual en Azure: la consulta es pública y de solo lectura |
| Caficultores, transportadores y operarios | Cognito | No se mueven a Azure |

## 5. DNS

- **Público.** El dominio de la consulta del saco vive en Route 53. Si se activa Azure, el registro
  de la consulta pasa a enrutamiento por conmutación (failover) con chequeo de salud: responde AWS
  y, si AWS no responde, Azure. Hoy el registro apunta solo a AWS.
- **Privado.** Solo hace falta si se activa la VPN. Se usarían endpoints de entrada y salida de
  Route 53 Resolver del lado de AWS y Azure DNS Private Resolver del lado de Azure, cada uno
  reenviando solo su propia zona privada.

## 6. Dónde va el código

El repositorio `iac` queda listo para agregar Azure sin tocar lo de AWS:

```
iac/
├── modules/
│   ├── network/          # AWS (Épica 6)
│   ├── security/         # AWS (Épica 6)
│   ├── ingest/           # AWS (Épica 6)
│   ├── farm/             # AWS (Épica 6)
│   ├── function/         # AWS (Épica 6)
│   └── azure/            # Reservado: aquí irían los módulos con el proveedor azurerm
└── environments/
    ├── dev/  test/  prod/    # AWS
    └── azure-prod/           # Reservado: ambiente de Azure con su propio estado
```

- El ambiente de Azure tendría su propio archivo de estado en el mismo backend S3, con otra llave,
  para que un `plan` de Azure nunca toque el estado de AWS.
- El proveedor `azurerm` solo se declara dentro de `environments/azure-prod/`. Los módulos de AWS
  no cambian.
- Las variables `subscription_id` y `tenant_id` llegan desde el pipeline, no desde el repositorio.

Nada de esto se escribe dentro de las 100 horas de la Épica 6. Es solo la convención para que, si
se activa, no haya que reorganizar el repositorio.

## 7. Qué se prepara y qué no se construye

| Se prepara (en este documento) | No se construye |
|---|---|
| Rango `10.90.0.0/16` reservado y verificado sin solape | Suscripción, VNet o cualquier recurso en Azure |
| Diseño de la VPN con el Transit Gateway, con ASN y tabla de rutas | VPN Gateway ni conexión VPN |
| Modelo de identidad para personas y para el pipeline | Identidades ni credenciales federadas en Entra ID |
| Registro de failover para la consulta del saco | Chequeo de salud ni registro secundario en Route 53 |
| Carpeta y convención de Terraform para `azurerm` | Código de Terraform para Azure |
| Pieza candidata (consulta del saco) y lo que nunca se mueve | Réplica de datos hacia Azure |

## 8. Cuándo se activaría

La Federación decide la activación. Estos son los casos en los que tendría sentido:

1. La consulta del saco incumple su objetivo de disponibilidad por una falla regional de AWS que
   `us-east-2` no alcanza a cubrir dentro de las 4 horas.
2. Un comprador o una auditoría exige que la consulta corra en un proveedor distinto.
3. Aparece una condición legal o de precio que haga mejor usar el servicio de inferencia de Azure.

Al activarse, el costo de la VPN, del cómputo de la consulta y de la copia de datos se estima en el
documento de costos (#29) antes de construir nada.
