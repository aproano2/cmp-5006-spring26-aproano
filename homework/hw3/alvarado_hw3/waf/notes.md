# Notas de ModSecurity

## Stack evidenciado
- Proxy WAF: `owasp/modsecurity-crs:nginx`
- Backend protegido: DVWA en `localhost:8080`
- Acceso filtrado: `localhost:8081`
- Motor observado en log: `ModSecurity v3.0.14`
- Conector observado en log: `ModSecurity-nginx v1.0.4`
- CRS observado en log: `OWASP_CRS/3.3.9`

## Regla custom del laboratorio
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

## Carga de la regla
La imagen oficial carga reglas locales desde `/etc/modsecurity.d/local-rules/`. En este repositorio el montaje queda resuelto mediante `docker/docker-compose.dvwa_waf.yml`.

## Arranque recomendado
El metodo recomendado es usar los archivos versionados del repositorio:

```powershell
docker compose -f docker/docker-compose.dvwa_base.yml -f docker/docker-compose.dvwa_waf.yml up -d
```

Comprobaciones:
```powershell
docker ps -a
curl.exe -i http://localhost:8081/
docker logs dvwa_waf --tail 100
docker logs dvwa_waf 2>&1 | Select-String "1001001"
```

## Evidencia funcional

| Prueba | Resultado esperado | Evidencia |
|---|---|---|
| `127.0.0.1; whoami` en DVWA directo | `www-data` | `evidence/dvwa_attack/dvwa_command_injection_before_waf.png` |
| Mismo patron a traves del WAF | `403 Forbidden` | `evidence/waf_blocking/dvwa_blocked_after_waf_403.png` |
| Revision de logs | Match sobre `ARGS:ip` con `id "1001001"` | `evidence/waf_blocking/modsecurity_log_block.png` |

## Hallazgo del log
La evidencia de log muestra que la peticion fue denegada en `phase 2`, con coincidencia del operador regex sobre `ARGS:ip` y con el mensaje `Bloqueo de posible separador de command injection (; o |) en ARGS`.

## Limitacion reconocida
La regla es deliberadamente estrecha para cumplir el enunciado. No bloquea `&&`, `||`, backticks ni `$()`, por lo que solo demuestra defensa puntual y no remediacion completa.
