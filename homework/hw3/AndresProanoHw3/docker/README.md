# Base Docker para DVWA local

## Objetivo
Dejar una base sencilla para levantar DVWA en un entorno local de laboratorio usando Docker Compose.

## Alcance de este directorio
Este directorio concentra el despliegue reproducible del laboratorio:
- `docker-compose.dvwa_base.yml` para `DVWA + MariaDB`
- `docker-compose.dvwa_waf.yml` para agregar el proxy `ModSecurity + CRS`

## Archivo incluido
- `docker-compose.dvwa_base.yml`: stack minimo con DVWA y MariaDB para pruebas locales.
- `docker-compose.dvwa_waf.yml`: servicio WAF que protege DVWA en `localhost:8081`.

## Uso sugerido
1. Revisar el archivo `docker-compose.dvwa_base.yml`.
2. Levantar DVWA con `docker compose -f docker/docker-compose.dvwa_base.yml up -d`.
3. Abrir DVWA en `http://localhost:8080`.
4. Completar la configuracion inicial de la base de datos desde la interfaz si el contenedor lo solicita.
5. Iniciar sesion y cambiar el nivel de seguridad a `Low`.
6. Levantar el WAF con `docker compose -f docker/docker-compose.dvwa_base.yml -f docker/docker-compose.dvwa_waf.yml up -d`.
7. Validar el acceso protegido en `http://localhost:8081`.

## Ideas de prueba
- Verificar primero que DVWA cargue correctamente y que el modulo `Command Injection` este disponible.
- Tomar una captura de la configuracion o del panel inicial para documentar que el entorno era local.
- Confirmar que la prueba vulnerable y la prueba bloqueada se ejecutan sobre el mismo laboratorio.
- Registrar cualquier detalle de configuracion extra en `waf/notes.md`.

## Integracion con WAF
La integracion con WAF queda resuelta mediante `docker-compose.dvwa_waf.yml`, que:
- publica el WAF en `8081`
- mantiene DVWA directo en `8080`
- usa `BACKEND=http://dvwa:80`
- monta la regla custom desde `waf/modsecurity_rules/`

## Nota importante
Este entorno es solo para fines academicos y de laboratorio controlado. No debe exponerse a Internet ni usarse contra sistemas de terceros.
