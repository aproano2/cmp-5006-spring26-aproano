# DVWA + WAF local

Este entorno levanta DVWA directo en `http://localhost:8080` y la misma aplicación detrás de un reverse proxy con regla WAF en `http://localhost:8081`.

```bash
docker compose up -d
```

1. Abrir `http://localhost:8080/setup.php` y crear/resetear la base de datos.
2. Iniciar sesión con `admin` / `password`.
3. Ir a `DVWA Security` y seleccionar `Low`.
4. Ataque sin WAF:
   - URL base: `http://localhost:8080/vulnerabilities/exec/`
   - Payload en el campo IP: `127.0.0.1;whoami`
   - Resultado esperado: la salida incluye el usuario del proceso web, típicamente `www-data`.
5. Validación con WAF:
   - Repetir el mismo payload vía `http://localhost:8081/vulnerabilities/exec/`
   - Resultado esperado: `403 Forbidden`.

La regla defensiva está en `waf/nginx.conf` y bloquea `;` o `|` en `$args` antes de reenviar la petición a DVWA.
