# Reporte de Resolución de Retos: picoCTF

Este documento detalla la metodología y los pasos seguidos para resolver una serie de desafíos de ciberseguridad y criptografía en la plataforma picoCTF.

### GuessMyCheese

Para resolver este reto, se desarrolló un script en Python diseñado para realizar un ataque de diccionario combinado con fuerza bruta de un byte para descifrar un hash SHA-256.

Una breve explicación del código:

- Importamos los módulos hashlib y os necesarios para usar el algoritmo de hashing e importar el archivo cheese_list.txt.

- Dentro de la lógica del código vamos a leer el archivo línea por línea eliminando los espacios en blanco, saltos de linea y convirtiendo todo a minúsculas.

- Posterior a leer el archivo vamos a utilizar un bucle de 0 a 255 (representando los valores que puede llegar a tener un byte) y tomamos el nombre del queso en el archivo convirtiéndolo a bytes y añadimos el byte de la sal final como sufijo. 

- Finalmente, aplicamos el algoritmo SHA-256 a la combinación de "queso+sal" y convertimos la cadena de texto hexadecimal legible. Al tener el resultado comparamos con el hash objetivo que estamos buscando.

Como resultado, obtenemos el nombre del queso original: 'Mascarpone' junto con el valor exacto de la sal en formato hexadecimal (1f) dando la combinación exacta que generó el hash.

En este caso, tuvimos como resultado, para 'e4f87db650036276b732987fe7cb95f3c4bad824ef5d5238bed25c925f595688':
- Nombre del queso: Mascarpone
- Sal: 1f

### HideToSee

Para poder resolver descargamos la imagen y la subimos al link: 
- https://www.aperisolve.com/c2fe86a71d25aa68d8149891506be629#google_vignette

donde descargamos el archivo Steghide, lo descomprimimos y obtenemos el resultado que es:

- krxlXGU{zgyzhs_xizxp_zx751vx6}

para procesar esto, lo que realizamos es un descifrado de atbash, este consiste en que la última letra del abecedario se transforma en la primera (a = z), la penúltima en la segunda (b = y) y así sucesivamente. Al realizar este proceso obtenemos la palabra: 

- picoCTF{atbash_crack_ac751ec6}

### Rotation

Para resolver esto, utilizamos la página CyberChef donde en su interior utilizamos ROT13. Lo que tenemos que decifrar es: 

- xqkwKBN{z0bib1wv_l3kzgxb3l_949in1i1}

donde, después de probar diferentes valores se obtuvo el valor final de 18, dando como resultado:

- picoCTF{r0tat1on_d3crypt3d_949af1a1}

### Sustitution

Para realizar el siguiente ejercicio, también se utilizó CyberChef donde se ingresó "Sustitution". 
Dentro de este apartado se fue haciendo prueba y error al inicio. Como se sabía el final de la palabra se empezó por reemplazar las letras de picoCTF. 

Posterior a este intento de fuerza bruta, se analizó la repetición de letras donde se encontró que la 'j' era la que más se repetía. Dentro del idioma de inglés se reemplazó esta por la 'e'.

Después, en la primera parte de la palabra se observa que existe una palabra 'tnese', por lo que reemplazamos la n por la h. Así mismo, después de un análisis tenemos otra palabra comvuter donde la v reemplazamos por la p. 

Siguiendo este algoritmo pudimos ir decifrando la palabra hasta obtener el Chipertext de:

- U B W R G T N B Q E C F O H K V I D S Y M P L A D X

Revelando el input, con la clave:

- picoCTF{N6R4M_4N41Y515_15_73D10U5_42EA1770}

### Vigenere

Dentro de CyberChef utilizamos la función de Vigenère Decode donde, al colocar la palabra clave 'CYLAB' pudimos obtener la clave:

- picoCTF{D0NT_US3_V1G3N3R3_C1PH3R_ae82272q}
