### Section 1: Research - Historical & Advanced Classical Ciphers

#### The Vigenère Cipher:
- Mechanism: Explain how the Vigenère Square (Tabula Recta) is used to encrypt a message using a keyword.

El Vigenère Square consiste en tener una cuadrícula de 26x26 que contiene el alfabeto escrito 26 veces en filas, 
cada fila está desplazada cíclicamente una posición a la izquierda comparado con la anterior. Para poder cifrar 
elegimos una palabra clave y esta se repite hasta que su longitud coincida con la del mensaje. Emparejamos el primer carácter del texto plano con el primero de la clave, buscamos la fila que comienzan con la letra de la clave y la columna que comienza con la letra del mensaje para que la intersección se considere el carácter cifrado. Algebraicamente, podemos definirlo como 
$C_i = (P_i + K_i) \pmod{26}$

- Analysis: How does this polyalphabetic approach defend against basic frequency analysis?

Se diferencia porque el sistema polialfabético utiliza múltiples alfabetos de crifado en secuencia. Esto significa que una letra como la "E" no se cifrará siempre como el mismo carácter, sino que va a ir variando dependiendo de su posición relativa a la palabra clave. Cuando distribuimos una misma letra del texto entre varios caracteres posibles eliminamos los picos estadísticos.

- Breaking the Cipher: Briefly describe the Kasiski examination and how it determines keyword length.

El Kasiski Examination consiste en encontrar secuencias repetidas de caracteres en el texto cifrado. Si tenemos un grupo común de letras (como conectores) van a aparecer varias veces en el texto original y coincidirá con la misma posición en la palabra clave repetida, produciendo bloques de texto cifrado idénticos. Cuando podemos determinar la distancia entre estas repeticiones y encontramos sus factores comunes se puede llegar a determinar la longitud probable de la palabra clave.

#### The Hill Cipher:
- Mathematical Basis: This cipher is based on linear algebra. Explain how a plaintext block is converted into a vector and multiplied by a key matrix.

En el cifrado Hill, como primer paso, las letras se convierten en valores numéricos. Después, podemos dividir el texto plano en bloques de tamaño n representados como vectores columna de n componentes. El proceso de cifrado se realiza multiplicando una matriz de clave K de tamaño n x n por el vector del texto plano P, para esto aplicamos aritmética modular: $C = KP \pmod{26}$

- Requirements: What specific mathematical requirements must the key matrix meet to ensure a message can be decrypted?

Para poder decifrar necesitamos que la matriz de clave sea invertible bajo el módulo utilizado. Para lograr esto, se necesita que el determinante de la matriz sea distinto de cero y coprimo con la base modular (26). En otras palabras, buscamos que el determinante no sea divisible por los factores primos de 26.

#### The Playfair Cipher:
- Mechanism: Explain the process of creating the $5 \times 5$ grid and the specific rules for encrypting a digraph (pair of letters).

Primero ingresamos una palabra clave, eliminando letras duplicadas y llenando el resto con las letras restantes del alfabeto combinando, normalmente, la "I" y la "J" en una sola celda. El mensaje se divide en pares donde, si un par tiene letras iguales insertamos una "X" entre ellas. 
Las reglas de cifrado son 
1) Si están en la misma fila, sustituimos por las letras a su derecha
2) Si están en la misma columna, por las letras debajo
3) Si forman un rectángulo, cada letra la sustituimos por la de su misma fila pero en la columna de la otra letra del par

- Historical Context: Research its use by British forces in WWI and WWII. Why was it considered "field-ready" compared to more complex systems?

Se consideraba "field-ready" porque no requeria equipo especial, solo lápiz y papel, y era lo suficientemente rápido para proteger información táctica cuya relevancia caducaba en pocas horas, como las coordenadas de un ataque de artillería.

#### The Enigma Machine:
- Rotor Logic: Explain the concept of the rotors and how they caused the substitution alphabet to change with every single keystroke.

Los rotores son discos con cableado interno que conectan 26 contactos en un lado con 26 en el otro en un patrón desordenado. Lo fundamental es que el rotor de la derecha gira una posición con cada tecla presionada, esto altera físicamente el circuito eléctrico y cambia el alfabeto de sustitución para la siguiente letra. Este movimiento mecánico crea un periodo polialfabético largo antes de que la secuencia se repita.

- The Reflector: What was the purpose of the reflector in the Enigma's circuitry, and why did it mean a letter could never be encrypted as itself?

El reflector es un disco estacionario al final de los rotores que redirige la señal eléctrica de vuelta a través de ellos por un camino diferente. Este le daba reciprocidad a la máquina donde la misma configuración servía para cifrar y descifrar. Sin embargo, el reflector conectaba los contactos en pares obligando a que la corriente no regrese por el mismo cable de entrada, haciendo imposible que una letra se cifrara como ella misma. 

- The Plugboard: How did the plugboard (Steckerbrett) exponentially increase the number of possible configurations?

Este se ubicaba al frente de la máquina permitiendo intercambiar pares de letras mediante cables antes de entrar a los rotores. Los rotores ofrecían unas 17,576 posiciones iniciales, el uso de 10 cables en el panel de parcheo añadia aproximadamente 150,738,274,937,250 de combinaciones adicionales. Esto elevaba el espacio de claves total a niveles astronómicos dificultando el croptoanálisis manual