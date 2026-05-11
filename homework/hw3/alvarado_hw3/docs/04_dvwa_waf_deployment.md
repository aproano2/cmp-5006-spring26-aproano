# Despliegue de DVWA con WAF (Command Injection)

## Proposito
Demostrar en un laboratorio local un ataque exitoso de Command Injection contra DVWA en nivel `Low` y su bloqueo posterior con ModSecurity usando una regla que rechaza `;` y `|` en argumentos HTTP.

## Alcance seguro del laboratorio
- Objetivo autorizado: DVWA desplegado en localhost.
- Modalidad: contenedores Docker en equipo local.
- Nivel de seguridad de DVWA: `Low`.
- Restriccion etica: no se probaron estas tecnicas contra sistemas publicos ni infraestructura de terceros.

## Entorno evidenciado
- Aplicacion vulnerable: DVWA
- Despliegue base: `docker/docker-compose.dvwa_base.yml`
- Despliegue WAF: `docker/docker-compose.dvwa_waf.yml`
- WAF: `owasp/modsecurity-crs:nginx`
- Regla custom: `waf/modsecurity_rules/block_command_separators.conf`
- Puerto de DVWA: `8080`
- Puerto del WAF: `8081`

## Fase 1 - Ataque exitoso sin WAF

### Procedimiento
1. Levantar DVWA con Docker.
2. Iniciar sesion en DVWA.
3. Fijar seguridad en `Low`.
4. Abrir `Vulnerabilities -> Command Injection`.
5. Probar el payload:
   ```
   127.0.0.1; whoami
   ```

### Resultado observado
La salida del modulo muestra la ejecucion del `ping` y, al final, el usuario del proceso web: `www-data`. Eso confirma que DVWA esta concatenando entrada del usuario con comandos del sistema operativo y ejecutandolos.

### Evidencia
- `evidence/dvwa_attack/dvwa_command_injection_before_waf.png`

### Observacion sobre la captura
La captura previa muestra el resultado de `whoami` (`www-data`) y el contexto del modulo vulnerable, lo cual prueba ejecucion de comandos. El payload exacto queda documentado en este archivo y puede reproducirse con la validacion local incluida en el `README.md`.

## Fase 2 - Defensa con ModSecurity

### Topologia
`navegador -> Nginx + ModSecurity -> DVWA`

### Regla aplicada
Archivo: `waf/modsecurity_rules/block_command_separators.conf`

```conf
SecRule ARGS "@rx [;|]" \
    "id:1001001,\
    phase:2,\
    deny,\
    status:403,\
    log,\
    msg:'Bloqueo de posible separador de command injection (; o |) en ARGS'"
```

### Logica de la regla
- `ARGS` inspecciona parametros HTTP de entrada.
- `@rx [;|]` coincide con `;` o `|`.
- `deny,status:403` bloquea la solicitud antes de llegar al backend.
- `log` registra la coincidencia para trazabilidad.

## Fase 3 - Validacion del bloqueo

### Procedimiento
1. Acceder a DVWA a traves del WAF.
2. Repetir el patron de ataque con el mismo payload.
3. Verificar que la respuesta sea bloqueada.

### Resultado observado
El WAF devuelve `403 Forbidden` y no permite que el backend procese la solicitud. El log de ModSecurity registra el evento con `id "1001001"` y con coincidencia sobre `ARGS:ip`.

### Evidencias
- `evidence/waf_blocking/dvwa_blocked_after_waf_403.png`
- `evidence/waf_blocking/modsecurity_log_block.png`

### Lo que se ve en el log
La captura del log muestra, al menos, estos elementos relevantes:
- `Access denied with code 403`
- `Matched "Operator Rx" with parameter [;|]`
- variable `ARGS:ip`
- valor con `127.0.0.1; whoami`
- `id "1001001"`

### Riesgo de interpretacion
La captura del `403 Forbidden` por si sola no demuestra que la peticion haya pasado por ModSecurity; podria ser un `403` de otra capa. La evidencia queda defendible solo cuando se lee junto con `evidence/waf_blocking/modsecurity_log_block.png`, donde si aparece el `id "1001001"` y la URI `vulnerabilities/exec/`.

## Limitacion tecnica documentada
Esta regla bloquea `;` y `|`, pero no cubre otros separadores o tecnicas como `&&`, `||`, backticks, nuevas lineas o `$()`. Por eso debe interpretarse como un control compensatorio de laboratorio y no como sustituto de validacion segura, allowlists y eliminacion del uso de shell en la aplicacion.

## Valor academico del literal
- Se muestra el ataque antes de la defensa.
- Se muestra la defensa aplicada.
- Se muestra la regla especifica solicitada por el enunciado.
- Se documenta el `403 Forbidden`.
- Se conserva evidencia del log del WAF.
- El laboratorio puede volver a levantarse desde los compose versionados del repositorio.

## Checklist de evidencias del literal 4
- [x] `evidence/dvwa_attack/dvwa_command_injection_before_waf.png`
- [x] `evidence/waf_blocking/dvwa_blocked_after_waf_403.png`
- [x] `evidence/waf_blocking/modsecurity_log_block.png`
- [x] Regla documentada en `waf/modsecurity_rules/block_command_separators.conf`
- [x] Contexto del stack resumido en `waf/notes.md`
- [x] Archivo reproducible para levantar el WAF desde el propio repositorio
