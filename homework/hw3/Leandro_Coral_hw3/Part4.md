# WAF Deployment (DVWA) - Laboratorio Completado

El entorno de laboratorio ha sido desplegado exitosamente utilizando Docker, siguiendo tu plan de implementación. Aquí tienes los detalles y las instrucciones para tomar tus capturas de pantalla para el deber:

## Fase 1: Preparación del Entorno Local (DVWA)
El contenedor de DVWA está corriendo de forma aislada. Ya se ha inicializado la base de datos y la seguridad ha sido configurada en nivel "Low".

*   **URL Directa (Sin WAF):** `http://localhost:8080`
*   **Credenciales:** `admin` / `password`
*   **Para tu captura:** Ingresa a esta URL, ve a *DVWA Security*, verifica que esté en "Low" y toma la captura.

## Fase 2: Ejecución del Ataque (Command Injection)
*   **Para tu captura:** Dentro de `http://localhost:8080/vulnerabilities/exec/`, ingresa el payload `127.0.0.1; whoami` y haz clic en Submit. 
*   Verás cómo se concatena el comando y se muestra el usuario (probablemente `www-data`). Toma una captura de esa pantalla.

## Fase 3: Implementación Defensiva (ModSecurity WAF)
Se levantó un proxy reverso con Nginx y ModSecurity (`owasp/modsecurity-crs`). Se ha configurado una regla personalizada (`custom_rules.conf`) para bloquear el punto y coma `;` y la tubería `|`. 
Esta regla fue montada en el contenedor para que se evalúe y bloquee la petición.

**Regla Creada:**
```apache
SecRule ARGS "([;|])" \
    "id:1000,\
    phase:2,\
    deny,\
    status:403,\
    log,\
    msg:'Command Injection attempt blocked (Semicolon or Pipe detected)'"
```
*   **Para tu captura:** Puedes tomar una captura del archivo `custom_rules.conf` que dejé en tu carpeta `hw3`, o del código de arriba.

## Fase 4: Validación de la Defensa
El proxy WAF está protegiendo a DVWA a través del puerto 8000.

*   **URL Protegida (Con WAF):** `http://localhost:8000`
*   **Para tu captura:** Ingresa a `http://localhost:8000/vulnerabilities/exec/` (inicia sesión con `admin/password`), intenta ingresar el mismo payload `127.0.0.1; whoami` y haz clic en Submit. 
*   El servidor WAF interceptará la petición antes de que llegue a DVWA y mostrará una página de error **403 Forbidden**. Toma captura de esto.

### Evidencia del Log de ModSecurity (Opcional/Extra)
Realicé una prueba enviando el payload directamente y el WAF lo bloqueó. El log generado por ModSecurity confirma que la regla `1000` bloqueó el ataque exitosamente:

```json
{
  "message": "Command Injection attempt blocked (Semicolon or Pipe detected)",
  "details": {
    "match": "Matched \"Operator `Rx' with parameter `([;|])' against variable `ARGS:ip' (Value: `127.0.0.1; whoami' )",
    "reference": "o9,1o9,1v165,17",
    "ruleId": "1000",
    "file": "/etc/modsecurity.d/owasp-crs/rules/REQUEST-900-CUSTOM.conf",
    "lineNumber": "1"
  }
}
```
*(Puedes encontrar el log completo exportado en tu carpeta de proyecto en `modsecurity_audit.log`).*
