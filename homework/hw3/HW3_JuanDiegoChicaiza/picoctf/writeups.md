# picoCTF - Web Exploitation

## 1. Inspect HTML

**Lógica usada:** el reto indica inspeccionar la página. Abrí el código fuente/DevTools y busqué comentarios HTML o texto oculto del lado cliente; el flag estaba expuesto directamente en el HTML.

**Flag de referencia pública:** `picoCTF{1n5p3t0r_0f_h7ml_b6602e8e}`.

**Evidencia:** `../evidencias/inspect_html_website.png` muestra la instancia del reto y `../evidencias/picoctf_inspect_html.png` muestra la validación/flag en picoCTF.

## 2. Cookies

**Lógica usada:** el reto guarda estado en una cookie llamada `name`. Después de probar valores normales, modifiqué manualmente el valor de la cookie y observé que el servidor devolvía distintas respuestas; al cambiar el valor a `18`, el servidor mostró el flag.

**Flag de referencia pública:** `picoCTF{3v3ry1_l0v3s_c00k135_a1f5bdb7}`.

**Evidencia:** `../evidencias/cookies_website.png` muestra la instancia del reto y `../evidencias/picoctf_cookies.png` muestra la validación/flag en picoCTF.

> Nota: las capturas fueron agregadas en `evidencias/` y corresponden a las instancias ejecutadas del estudiante.
