# Homework 2: Securing the AutoDrive Firmware Pipeline

## Elaborado por

- Pablo Alvarado / 00344965
- Andres Proano / 00327809

Entrega para el caso AutoDrive, centrada en generacion manual de RSA, hashes criptograficos, certificados digitales, firmas digitales y diseno de un protocolo seguro de actualizacion de firmware.

## Contenido

- Notebook principal con desarrollo teorico y pequenas comprobaciones en Python.
- Explicacion paso a paso de las Partes 1 a 5 del enunciado.
- Conclusion final y referencias tecnicas.

## Archivo principal

- `Homework_2_Securing_AutoDrive_Firmware_Pipeline.ipynb`

## Estructura de la entrega

1. Introduccion general al caso AutoDrive.
2. RSA manual con `p = 11` y `q = 13`, incluyendo verificacion de cifrado y descifrado.
3. Uso de SHA-256 para integridad, avalanche effect y resistencia a colisiones.
4. Explicacion de certificados X.509, CSR y Root CA de confianza.
5. Flujo correcto de firma digital y no repudio.
6. Protocolo hibrido de actualizacion segura con tabla de requerimientos y diagrama ASCII.

## Ejecucion

El notebook usa librerias estandar de Python (`math`, `hashlib`, `json`, `os`) y la libreria `cryptography` para las demostraciones practicas de certificados, firmas y cifrado hibrido. Basta con abrir el archivo `.ipynb` en Jupyter Notebook o Visual Studio Code y ejecutar las celdas de codigo.

