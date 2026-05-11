# Aviso de Privacidad - QuitoCash

> Documento academico breve, redactado para alinearse con la LOPDP del Ecuador y con el GDPR europeo.

## 1. Responsable del tratamiento
**QuitoCash S.A.**, con domicilio en Quito, Ecuador, es el responsable del tratamiento de los datos personales usados para operar la aplicacion. Contacto de privacidad: `privacy@quitocash.example`. Delegado de Proteccion de Datos: `dpo@quitocash.example`.

## 2. Datos que tratamos
- Datos de identificacion: nombres, cedula o pasaporte, fecha de nacimiento.
- Datos de contacto: numero telefonico y correo electronico.
- Datos de autenticacion y seguridad: hash de credenciales, tokens de sesion, huella del dispositivo y logs de acceso.
- Datos transaccionales: monto, contraparte, fecha, canal y direccion IP asociada a la operacion.
- Datos opcionales para la funcion de IA `Spending Insights`: patrones de gasto inferidos desde el historial transaccional, solo si el usuario activa esta funcion.

## 3. Finalidades y base legal

| Finalidad | Base legal |
|---|---|
| Apertura de cuenta, autenticacion y transferencias por numero telefonico | Ejecucion contractual |
| Cumplimiento de KYC, prevencion de lavado y requerimientos regulatorios | Obligacion legal |
| Seguridad de la plataforma, monitoreo antifraude y defensa ante abuso | Interes legitimo debidamente ponderado |
| Envio de promociones o comunicaciones no esenciales | Consentimiento |
| Funcion opcional de IA `Spending Insights` | Consentimiento expreso del titular; salvaguardas de decisiones automatizadas conforme LOPDP Art. 20 y GDPR Art. 22 |

## 4. Destinatarios y transferencias
QuitoCash podra comunicar datos a bancos corresponsales, procesadores de pago, proveedores cloud, proveedores de autenticacion y autoridades competentes cuando exista obligacion legal. Si existieran transferencias internacionales, estas se realizaran con las garantias legales aplicables, incluidas clausulas contractuales adecuadas cuando corresponda.

## 5. Conservacion
Los datos se conservaran durante la relacion contractual y, despues, solo por el tiempo necesario para obligaciones regulatorias, defensa de reclamaciones, prevencion de fraude y cumplimiento contable. Los datos tratados para marketing o para la funcion de IA opcional se eliminaran o desactivaran cuando el titular retire su consentimiento, salvo obligacion legal de retencion.

## 6. Portabilidad y oposicion
El titular puede solicitar una copia de sus datos en formato estructurado, comun y de lectura mecanica, o pedir su transmision a otro responsable cuando sea tecnicamente posible. Tambien puede oponerse al tratamiento para marketing, perfilamiento no esencial o tratamientos basados en interes legitimo, en cuyo caso QuitoCash dejara de tratar los datos salvo que acredite motivos legitimos imperiosos o necesidad para reclamaciones.

Las solicitudes pueden realizarse desde `Configuracion -> Privacidad` o escribiendo a `privacy@quitocash.example`. QuitoCash respondera dentro de los plazos legales aplicables en Ecuador y, si corresponde GDPR, dentro del plazo previsto por dicha normativa.

## 7. Decisiones automatizadas e IA
La funcion `Spending Insights` usa analisis automatizado del historial transaccional para clasificar categorias de gasto, detectar patrones y generar predicciones presupuestarias. Esta funcion sera opcional, estara desactivada por defecto y no se utilizara para aprobar o negar transferencias, creditos ni acceso a productos financieros.

Si el usuario activa esta funcion, podra:
- solicitar intervencion humana
- pedir una explicacion general de la logica aplicada
- expresar su punto de vista
- impugnar un resultado
- desactivar la funcion sin perder acceso al servicio principal

## 8. Seguridad y reclamos
QuitoCash aplicara cifrado en transito y en reposo, control de acceso por roles, segregacion de entornos, monitoreo de eventos y respuesta a incidentes. Para ejercer derechos o presentar reclamos, el titular puede contactar a QuitoCash; si la respuesta no es satisfactoria, puede acudir a la SPDP en Ecuador o a la autoridad de control competente en la UE cuando corresponda.

---

## 9. Data minimization - Datos que QuitoCash no deberia recolectar

| # | Dato a no recolectar | Justificacion |
|---|---|---|
| 1 | Lista completa de contactos del telefono | No es necesaria para transferir dinero a un numero puntual y expone datos de terceros que no son usuarios. |
| 2 | Geolocalizacion GPS continua en segundo plano | Es desproporcionada para una app de pagos entre personas y revela patrones sensibles de vida diaria. |
| 3 | Contenido de SMS, WhatsApp o redes sociales | Excede radicalmente la finalidad del servicio y existen mecanismos menos invasivos para OTP, notificaciones y antifraude. |

## Nota academica
Este aviso busca cumplir con los elementos exigidos por el deber: identidad del responsable, finalidades, categorias de datos, base legal, destinatarios, transferencias, conservacion, derechos, contacto, seguridad, reclamos, portabilidad, oposicion, decisiones automatizadas y minimizacion. En una implementacion real deberia acompaniarse de contratos con encargados, analisis de riesgos, evaluaciones de impacto y revision legal especializada.
