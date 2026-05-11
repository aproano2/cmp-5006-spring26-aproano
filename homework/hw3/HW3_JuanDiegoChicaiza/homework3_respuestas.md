# Homework 3: Web Defense & Privacy Compliance

**Estudiante:** Juan Diego Chicaiza

## Investigación previa

Antes de resolver los literales revisé el enunciado, el OWASP Top 10:2025 vigente publicado por OWASP, entradas recientes de NVD para CVEs de 2025/2026, el texto de la Ley Orgánica de Protección de Datos Personales de Ecuador (LOPDP), material de la Superintendencia de Protección de Datos Personales (SPDP) y referencias del GDPR sobre derechos y sanciones. Para las partes prácticas preparé una carpeta reproducible con DVWA y una regla WAF local; las capturas reales de picoCTF requieren una sesión del estudiante en picoGym, por lo que no se deben fabricar imágenes.

## 1. OWASP & CWE Mapping

| OWASP Top 10:2025 | CWE específico | CVE 2025/2026 | Resumen de impacto |
|---|---:|---|---|
| A01:2025 - Broken Access Control | CWE-862: Missing Authorization | CVE-2025-5121, GitLab CE/EE | GitLab informó que versiones 17.11 antes de 17.11.4 y 18.0 antes de 18.0.2 tenían una verificación de autorización faltante. El defecto podía permitir que compliance frameworks se apliquen a proyectos fuera del grupo autorizado, afectando confidencialidad e integridad en ámbitos donde GitLab se usa para gobernanza de proyectos. |
| A04:2025 - Cryptographic Failures | CWE-327: Use of a Broken or Risky Cryptographic Algorithm | CVE-2025-59745, AndSoft e-TMS v25.03 | AndSoft e-TMS usaba MD5 para proteger contraseñas, algoritmo que ya no es apropiado para almacenamiento seguro. El impacto principal es exposición de credenciales porque hashes MD5 pueden romperse con hardware moderno y ataques de diccionario/rainbow tables. |
| A05:2025 - Injection | CWE-89: SQL Injection | CVE-2025-25257, Fortinet FortiWeb | Fortinet FortiWeb 7.0.x, 7.2.x, 7.4.x y 7.6.x vulnerables permitían a un atacante no autenticado ejecutar SQL no autorizado mediante peticiones HTTP/HTTPS manipuladas. NVD le asigna CVSS 9.8 crítico y CISA lo añadió al catálogo de vulnerabilidades explotadas, por lo que el riesgo incluye lectura/modificación de datos y posible compromiso del sistema de administración. |

## 2. Contexto ecuatoriano: LOPDP

La LOPDP reconoce estos ocho derechos del titular:

| Derecho | Explicación breve |
|---|---|
| Acceso | Conocer y obtener gratuitamente los datos personales tratados y la información del tratamiento. |
| Rectificación y actualización | Corregir o actualizar datos inexactos o incompletos. |
| Eliminación | Solicitar supresión cuando el tratamiento incumple principios, ya no es necesario, venció el plazo de conservación, se revocó el consentimiento u opera otra causal legal. |
| Oposición | Negarse al tratamiento en los casos permitidos, especialmente marketing directo y ciertos tratamientos basados en interés legítimo. |
| Portabilidad | Recibir los datos en formato compatible, actualizado, estructurado, común, interoperable y de lectura mecánica, y transmitirlos a otro responsable cuando corresponda. |
| Suspensión del tratamiento | Pedir que el responsable suspenda temporalmente el tratamiento cuando se impugne exactitud, licitud, necesidad o exista otra causal legal. |
| Anulación | Solicitar que se deje sin efecto un tratamiento cuando exista una causa legal para invalidarlo. |
| No ser objeto de decisiones automatizadas | No quedar sujeto a una decisión basada únicamente en valoraciones automatizadas, incluida elaboración de perfiles, cuando produzca efectos jurídicos o afecte significativamente al titular. |

**Enforcement frente al GDPR.** En Ecuador, la SPDP puede actuar de oficio o a petición del titular, hacer actuaciones previas, inspecciones, medidas correctivas y procedimientos administrativos sancionadores. La LOPDP sanciona a entidades privadas/empresas públicas con multas sobre volumen de negocio: 0.1% a 0.7% por infracciones leves y 0.7% a 1% por graves; en el sector público usa salarios básicos unificados. En la Unión Europea, el GDPR se aplica por autoridades de control nacionales coordinadas por mecanismos como cooperación/ventanilla única; las multas pueden llegar a EUR 20 millones o 4% de la facturación anual global, además de órdenes correctivas, limitaciones de tratamiento y suspensión de transferencias. La lógica común es proporcionalidad y tutela de derechos, pero el GDPR tiene un techo sancionatorio global más alto y una arquitectura transfronteriza madura, mientras que Ecuador concentra la supervisión en la SPDP nacional.

## 3. Hands-on Exploitation & Defense: picoCTF

Los write-ups están en `picoctf/writeups.md`.

| Reto | Técnica usada | Screenshot |
|---|---|---|
| Inspect HTML | Revisar código fuente/DevTools; el flag aparece en un comentario HTML o contenido enviado al cliente. | `evidencias/inspect_html_website.png` y `evidencias/picoctf_inspect_html.png` |
| Cookies | Modificar la cookie `name`; al probar el valor `18`, la aplicación muestra el flag. | `evidencias/cookies_website.png` y `evidencias/picoctf_cookies.png` |

Las evidencias muestran tanto la instancia web del reto como la validación/flag correspondiente en picoCTF.

## 4. WAF Deployment: DVWA

La configuración reproducible está en `dvwa-waf/`.

| Elemento | Detalle |
|---|---|
| DVWA directo | `http://localhost:8080` |
| DVWA detrás del WAF | `http://localhost:8081` |
| Regla defensiva | `if ($args ~* "(;|\|)") { return 403; }` en `dvwa-waf/waf/nginx.conf` |
| Ataque antes del WAF | En Command Injection con seguridad `Low`: `127.0.0.1;whoami`; validado con salida `www-data`. |
| Validación después del WAF | Mismo payload vía puerto `8081`; validado con `403 Forbidden` servido por Nginx. |

Comandos:

```bash
cd HW3_JuanDiegoChicaiza/dvwa-waf
docker compose up -d
```

Screenshots generados:

| Evidencia | Ruta sugerida |
|---|---|
| Ataque exitoso antes del WAF | `evidencias/dvwa_command_injection_before.png` |
| Bloqueo 403 después del WAF | `evidencias/dvwa_waf_block_after.png` |

## 5. Privacy Engineering Task: QuitoCash

### Aviso de Privacidad de QuitoCash

**Responsable del tratamiento.** QuitoCash S.A., Quito, Ecuador, tratará datos personales para operar una aplicación fintech que permite enviar dinero usando números telefónicos y ofrece predicciones de hábitos de gasto. Este aviso aplica a usuarios en Ecuador y, cuando corresponda, a usuarios ubicados en la Unión Europea bajo el GDPR.

**Datos tratados.** Recopilamos identificación básica, número telefónico, información de cuenta, datos transaccionales, destinatarios de pagos, datos de dispositivo y registros de seguridad. No recolectaremos datos que no sean necesarios para prestar el servicio financiero, prevenir fraude, cumplir obligaciones legales o entregar funciones opcionales aceptadas por el usuario.

**Finalidades y bases legales.** Para crear la cuenta, autenticar usuarios, ejecutar transferencias y atender soporte usamos ejecución contractual. Para verificación KYC/AML, reportes regulatorios, contabilidad y conservación legal usamos cumplimiento de obligación legal. Para prevención de fraude, seguridad, auditoría y mejora operativa usamos interés legítimo, siempre con evaluación de proporcionalidad. Para predicción de hábitos de gasto, perfilamiento opcional, marketing y recomendaciones personalizadas usamos consentimiento explícito, revocable en cualquier momento.

**IA y decisiones automatizadas.** La función de IA de QuitoCash predice categorías y tendencias de gasto para mostrar alertas, presupuestos y recomendaciones. No tomaremos decisiones con efectos jurídicos o significativamente similares basadas únicamente en tratamiento automatizado, como negar una cuenta, bloquear fondos o reducir funcionalidades esenciales, sin intervención humana significativa y sin ofrecer explicación, revisión humana y mecanismo de impugnación.

**Derechos del titular.** El usuario puede ejercer acceso, rectificación/actualización, eliminación, oposición, portabilidad, suspensión, anulación y derecho a no ser objeto de decisiones automatizadas. Para portabilidad, QuitoCash entregará los datos proporcionados y observados por el usuario en formato estructurado y legible por máquina, por ejemplo CSV/JSON, cuando legalmente proceda. Para oposición, el usuario puede oponerse a marketing directo, perfilamiento publicitario y tratamientos basados en interés legítimo escribiendo a privacidad@quitocash.example o desde Configuración > Privacidad.

**Conservación y seguridad.** Conservaremos datos solo durante el tiempo necesario para la finalidad declarada y los plazos legales financieros, tributarios y de prevención de lavado. Aplicaremos cifrado en tránsito y reposo, control de acceso, monitoreo, segregación de funciones y registro de auditoría.

**Transferencias y encargados.** Podemos usar proveedores de nube, analítica antifraude, mensajería y verificación de identidad bajo contratos de encargado, confidencialidad y garantías adecuadas. Las transferencias internacionales se realizarán con base legal, garantías contractuales y controles equivalentes a LOPDP/GDPR.

**Reclamos.** El usuario puede contactar a privacidad@quitocash.example. En Ecuador también puede acudir a la Superintendencia de Protección de Datos Personales; en la UE puede reclamar ante su autoridad de control competente.

### Minimización de datos

QuitoCash podría querer recolectar estos datos, pero debería evitarlos:

1. Lista completa de contactos del teléfono: para enviar dinero basta permitir selección voluntaria de un contacto o ingreso manual de número; no es necesario subir toda la agenda.
2. Geolocalización precisa continua: para antifraude suele bastar ubicación aproximada, país, IP o señales puntuales de riesgo, no rastreo permanente.
3. Acceso a SMS/correos o historial financiero externo no vinculado: la predicción de gasto puede funcionar con transacciones dentro de QuitoCash y categorías declaradas, sin leer comunicaciones privadas o cuentas no necesarias.

## Fuentes consultadas

- OWASP Top 10:2025: https://owasp.org/Top10/2025/
- OWASP Top 10:2025 A01 Broken Access Control: https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
- OWASP Top 10:2025 A04 Cryptographic Failures: https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/
- OWASP Top 10:2025 A05 Injection: https://owasp.org/Top10/2025/A05_2025-Injection/
- NVD CVE-2025-5121: https://nvd.nist.gov/vuln/detail/CVE-2025-5121
- NVD CVE-2025-59745: https://nvd.nist.gov/vuln/detail/CVE-2025-59745
- NVD CVE-2025-25257: https://nvd.nist.gov/vuln/detail/CVE-2025-25257
- LOPDP Ecuador, texto legal: https://www.gob.ec/sites/default/files/regulations/2025-01/01%20Ley%20Org%C3%A1nica%20de%20Protecci%C3%B3n%20de%20Datos%20Personales.pdf
- SPDP Ecuador: https://spdp.gob.ec/
- GDPR, artículos 58 y 83: https://gdpr-info.eu/art-58-gdpr/ y https://gdpr-info.eu/art-83-gdpr/
