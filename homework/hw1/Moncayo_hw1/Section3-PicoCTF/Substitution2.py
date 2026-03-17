from collections import Counter

def desencriptar(encrypted_text,diccionario_sustitucion):
    semi_decrypted_text=""
    for caracter in encrypted_text:
        if caracter in diccionario_sustitucion:
            semi_decrypted_text += diccionario_sustitucion[caracter]
        elif caracter.isalpha():
            semi_decrypted_text += "_"
        else:
            semi_decrypted_text += caracter

    return semi_decrypted_text

encrypted_text="isnfnnpctitnznfmxhisnfwnxxntimjxctsnascdstushhxuhgqbinftnubfciruhgqnicichktckuxbackdurjnfqmifchimkabturjnfusmxxnkdnisntnuhgqnicichktehubtqfcgmfcxrhktrtingtmagckctifmichkebkamgnkimxtwscusmfnznfrbtnebxmkagmfonimjxntocxxtshwnznfwnjnxcnznisnqfhqnfqbfqhtnhemscdstushhxuhgqbinftnubfciruhgqnicichkctkhihkxrihinmuszmxbmjxntocxxtjbimxthihdnitibankitckinfntinackmkanpucinamjhbiuhgqbinftucnkunanenktcznuhgqnicichktmfnheinkxmjhfchbtmeemcftmkauhgnahwkihfbkkckdusnuoxctitmkanpnubickduhkecdtufcqitheenktnhkisnhisnfsmkactsnmzcxrehubtnahknpqxhfmichkmkacgqfhzctmichkmkaheinksmtnxngnkitheqxmrwnjnxcnznmuhgqnicichkihbusckdhkisnheenktcznnxngnkitheuhgqbinftnubfcirctisnfnehfnmjniinfznscuxnehfinusnzmkdnxctgihtibankitckmgnfcumkscdstushhxtebfisnfwnjnxcnznismimkbkanftimkackdheheenktczninuskcvbntctnttnkicmxehfghbkickdmkneenuicznanenktnmkaismiisnihhxtmkauhkecdbfmichkehubtnkuhbkinfnackanenktcznuhgqnicichktahntkhixnmatibankitihokhwisncfnkngrmtneenuicznxrmtinmusckdisngihmuicznxrisckoxconmkmiimuonfqcuhuiectmkheenktcznxrhfcnkinascdstushhxuhgqbinftnubfciruhgqnicichkismitnnotihdnknfminckinfntickuhgqbinftucnkunmghkdscdstushhxnftinmusckdisngnkhbdsmjhbiuhgqbinftnubfcirihqcvbnisncfubfchtcirghiczmickdisngihnpqxhfnhkisncfhwkmkankmjxckdisngihjniinfanenkaisncfgmusckntisnexmdctqcuhUIE{K6F4G_4K41R515_15_73A10B5_702E03EU}"

encrypted_text=encrypted_text.lower()

freq = Counter(encrypted_text)

diccionario_sustitucion={'q':'p','c':'i','u':'c','h':'o','i':'t','e':'f'}
#cubro 7 caracters porque siempre se inicia con picoctf

print("Desencripcion tras reemplazo con caracteres fijos")

print(desencriptar(encrypted_text,diccionario_sustitucion))

#Como primer approach para desencriptar poco mas del texto aplicamos mapeo por frecuencia

import string

english_freq_order = list("etaoinshrdlcumwfgypbvkjxqz")
contador=0

for letter,count in freq.most_common():
    if(letter.islower()):
        if(letter not in diccionario_sustitucion.keys()):
            diccionario_sustitucion[letter]=english_freq_order[contador]
        contador=contador+1

print("Desencripcion tras sustitucion con mapeo por frecuencia (primer approach)")

print(desencriptar(encrypted_text,diccionario_sustitucion))

#Con este approach se hace mas claro el texto encriptado ya que se empiezan a ver palabras como "there", "computer" o "competition" con esas palabras corrijo el diccionario

diccionario_sustitucion['s']='h'
diccionario_sustitucion['n']='e'
diccionario_sustitucion['f']='r'
diccionario_sustitucion['b']='u'
diccionario_sustitucion['g']='m'
diccionario_sustitucion['r']='y'
diccionario_sustitucion['d']='g'
diccionario_sustitucion['j']='b'
diccionario_sustitucion['m']='a'
diccionario_sustitucion['o']='k'
diccionario_sustitucion['t']='s'

print("Desencripcion tras ajuste manual de diccionario con base en resultado de desencripcion generado con mapeo por frecuencia")

print(desencriptar(encrypted_text,diccionario_sustitucion))

print("Desencripcion tras prueba con combinaciones de llaves y valores aun no identificados correctamente para el diccionario de traduccion")

from itertools import permutations

remaining_keys = ['a','k','l','p','v','w','x','y','z']
remaining_values = ['d','j','l','n','q','v','w','x','z']

def desencriptar2(text, key):
    return ''.join(key.get(c, c) for c in text)

def is_valid(text):
    # Considera válido si contiene palabras clave importantes que ya se reconocen a simple vista en el texto a esta funcion le fuimos agregando frases que ya se iban descubriendo para poder llegar a la solucion final en la cual todo el texto se haya desencriptado
    text = text.lower()
    keywords = ["there","computersecurity","competition","highschoolers","bettervehicle","flag","severalother","wellestablished","challenge","includingcyberpatriot","valuableskills","offensiveelements","laboriousaffairs","excitedabout","executingconfigscripts"]
    return all(word in text for word in keywords)

# Genera todas las permutaciones posibles para los caracteres restantes
for perm in permutations(remaining_values):
    trial_key = diccionario_sustitucion.copy()
    for k, v in zip(remaining_keys, perm):
        trial_key[k] = v
    decrypted = desencriptar2(encrypted_text, trial_key)
    if is_valid(decrypted):
        print("Texto final desencriptado tras permutaciones con texto semidesencriptado con mapeo por frecuencia")
        print(decrypted)

#Posteriormente se revisan cuales son los textos desencriptados para ver cual es totalmente legible y ese sería la respuesta final

#Como segundo approach buscamos en vez del mapeo por frecuencia emplear lo que seria Hill Climbing para continuar desencriptando el texto

#Hago hill climbing para mejorar el diccionario
#Empleo en la funcion de score palabras que reconozco a simple vista que ya se han ido formando
def score(text):

    # bigramas comunes
    bigrams = [
        "th","he","in","er","an","re","on","at","en","nd","is","it","ti",
        "es","or","nt","ed","al","to","se","ha","ou","ng","ar","as","st","io"
    ]
    
    # trigramas comunes
    trigrams = [
        "the","and","ing","her","ere","ent","tha","nth","was","for","hat","his",
        "ion","tio","ati","ver","all","men","com","est","ion","ion","ity"
    ]
    
    # palabras completas que ya se dejan ver en el texto desencriptado hasta el momento
    keywords = [
        "there","exist","several","other","well","established","highschool",
        "computer","security","competition","including","cyber",
        "challenge","these","focus","primarily","systems","administration",
        "fundamentals","which","very","useful","marketable","skills","however",
        "believe","proper","purpose","only","teach"]
    
    score = 0
    score += sum(text.count(b) for b in bigrams)
    score += 2 * sum(text.count(t) for t in trigrams)
    score += 5 * sum(text.count(w) for w in keywords) 
    #Pondero las coincidencias
    
    return score

import random

alphabet = list(string.ascii_lowercase)
best_key = diccionario_sustitucion.copy()
best_score = score(desencriptar2(encrypted_text, best_key))

for _ in range(100000): 
    letras_fijas = [best_key[k] for k in ['q','c','u','h','i','e']]
    alphabet_values_no_fixed = [v for v in alphabet if v not in letras_fijas]
    # Escogemos 2 letras para ir haciendo swaps y luego ver que tan cercano al ingles se parece el texto
    a, b = random.sample(alphabet_values_no_fixed, 2)
    keys_a = [k for k, v in best_key.items() if v == a]
    keys_b = [k for k, v in best_key.items() if v == b]
    new_key = best_key.copy()
    for k in keys_a:
        new_key[k] = b
    for k in keys_b:
        new_key[k] = a
    
    s = score(desencriptar2(encrypted_text, new_key))
    
    if s > best_score:
        best_score = s
        best_key = new_key

print("Desencripcion tras Hill Climbing (segundo approach)")

print(desencriptar2(encrypted_text, best_key))

#Con este approach se hace mas claro el texto encriptado ya que se empiezan a ver palabras como "there", "computer" o "competition" con esas palabras corrijo el diccionario
#En general veo a este approach mejor que el de mapeo por frecuencia y me permite reconocer mas letras para el diccionario las cuales defino a continuacion

best_key['j']='b'
best_key['m']='a'
best_key['o']='k'
best_key['b']='u'
best_key['r']='y'
best_key['d']='g'
best_key['t']='s'
best_key['g']='m'
best_key['s']='h'
best_key['n']='e'
best_key['f']='r'
best_key['a']='d'
best_key['x']='l'
best_key['k']='n'

#Habiendo descubierto mas letras se hace mas rapido el permutar con las remaining keys y values para desencriptar el texto por lo que aplico el mismo proceso que antes de combinaciones hasta desencriptar totalmente

remaining_keys = ['l','p','v','w','y','z']
remaining_values = ['j','q','v','w','x','z']

# Genera todas las permutaciones posibles para los caracteres restantes
for perm in permutations(remaining_values):
    trial_key = best_key.copy()
    for k, v in zip(remaining_keys, perm):
        trial_key[k] = v
    texto_desencriptado_perm = desencriptar2(encrypted_text, trial_key)
    if is_valid(texto_desencriptado_perm):
        print("Texto final desencriptado tras permutaciones con texto semidesencriptado con Hill Climbing")
        print(texto_desencriptado_perm)

#Posteriormente se revisan cuales son los textos desencriptados para ver cual es totalmente legible y ese sería la respuesta final