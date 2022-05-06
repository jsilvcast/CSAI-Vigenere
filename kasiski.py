#! /usr/bin/python3
import argparse
import itertools
import time
import numpy as np


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

# Function to sort the list of tuples by its second item
def sortTuple(tup):

    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] <= tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


def descifrar_cadena(cadena, dict_repeticiones):
    alfabeto_normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alfabeto_desplazado = ""
    cadena_descifrada = ""

    letras_comunes = ["E", "A", "O", "S"]
    lista_ordenada_frecuencias = []

    #print("Dict rep: ")
    #print(dict_repeticiones)

    for a in alfabeto_normal:
        aux = dict_repeticiones.get(a)
        if (aux == None):
            aux = 0
        lista_ordenada_frecuencias.append(aux)

    limite = 0
    for n in lista_ordenada_frecuencias:
        limite = limite + n

    limite = int(limite * 0.03)

    #print (limite)
    #print (lista_ordenada_frecuencias)

    dict_temporal_seleccion = {}

    for a in range(len(lista_ordenada_frecuencias)):
        valor_total = 0
        if lista_ordenada_frecuencias[a] >= limite:
            valor_total = valor_total + lista_ordenada_frecuencias[a]
            if lista_ordenada_frecuencias[(a+4)%26] >= limite:
                valor_total = valor_total + lista_ordenada_frecuencias[(a+4)%26]
                if lista_ordenada_frecuencias[(a+4+10)%26] >= limite:
                    valor_total = valor_total + lista_ordenada_frecuencias[(a+4)%26]
                    if lista_ordenada_frecuencias[(a+4+10+4)%26] >= limite:
                        valor_total = valor_total + lista_ordenada_frecuencias[(a+4)%26]
                        dict_temporal_seleccion[alfabeto_normal[a]] = valor_total
    
    list_aux = list(dict_temporal_seleccion.items())
    letra_clave = ""
    max_valor = 0
    for b in list_aux:
    	if b[1] > max_valor:
    		max_valor = b[1]
    		letra_clave = b[0]

    print(letra_clave, end="")

    # Crea un alfabeto desplazado con la letra que cifra
    for i in range(26):
        cod_ascii = (ord(letra_clave) + i)
        if(cod_ascii > 90):
            cod_ascii = cod_ascii - 26
        alfabeto_desplazado = alfabeto_desplazado + chr(cod_ascii)

    cadena = cadena.strip()
    for a in cadena:
        cadena_descifrada = cadena_descifrada + \
            alfabeto_normal[alfabeto_desplazado.index(a)]

    
    return cadena_descifrada


def main(file_name):

    file_input = open(file_name, "r")

    input_text = file_input.read()
    input_text = input_text.upper()

    text_len = len(input_text)

    substring_found = {}

    # Substring length
    substring_len = 3

    # Iterate over all possible substrings until checkIfEnterInElse or text_len
    for i in range(text_len - substring_len + 1):
        checkIfEnterInElse = False
        for j in range(substring_len, text_len - substring_len + 1):
            subcadena = input_text[j:j+substring_len]
            if substring_found.get(subcadena) == None:
                substring_found[subcadena] = []
                substring_found[subcadena].append(j + (substring_len - 1))
            else:
                checkIfEnterInElse = True
                substring_found[subcadena].append(j + (substring_len - 1))

        if checkIfEnterInElse == False:
            break
        substring_len += 1

    # Create a dict with freqs
    subcadenas_frecuencias = {}
    for a in substring_found:
        subcadenas_frecuencias[a] = len(substring_found[a])

    lista_subcadenas_frecuencias = list(subcadenas_frecuencias.items())
    # Use numpy to fast comparison
    np_lista_subcadenas_frecuencias = np.array(lista_subcadenas_frecuencias)

    # remove from np_lista_subcadenas_frecuencias elements with frequency > 1
    np_lista_subcadenas_frecuencias = np_lista_subcadenas_frecuencias[np_lista_subcadenas_frecuencias[:, 1] == '1']

    # remove from substring_found elements in np_lista_subcadenas_frecuencias
    for a in np_lista_subcadenas_frecuencias[:, 0]:
        del substring_found[a]

    # Lista de distancias calculada a partir do diccionario temporal
    lista_distancias = []

    for positions in substring_found.values():
        for i in range(len(positions)-1):
            lista_distancias.append(positions[i+1]-positions[i])

    # Descartamos mcd = 1 para evitar trigramas casuales que nos impidan
    # adivinar la longitud de la clave
    longitud = lista_distancias[0]
    for i in lista_distancias[1:]:
        aux = gcd(longitud, i)
        if aux != 1:
            longitud = aux

    print("La posible longitud de la clave es: " + str(longitud))
    print()

    # Inicializamos a lista con tantos elementos como longitud ten a clave
    lista_subcadenas = [input_text[i::longitud] for i in range(longitud)]

    for a in range(longitud):
        print("Cadena " + str(a) + ": " + lista_subcadenas[a])
        print()

    dict_repeticiones = {}
    lista_cadenas_descifradas = []

    print("Aplicando algoritmo AEOS...")
    print("La posible clave es: ", end="")
    for cadena in lista_subcadenas:
        for char in cadena:
            if char in dict_repeticiones:
                dict_repeticiones[char] += 1
            else:
                dict_repeticiones[char] = 1

        
        cadena_descifrada = descifrar_cadena(
            cadena, dict_repeticiones)
        lista_cadenas_descifradas.append(cadena_descifrada)

        dict_repeticiones = {}

    print("\n")

    # Desciframos por fin :)
    cadena_descifrada_FINAL = ""

    cad_iter = itertools.cycle([iter(x) for x in lista_cadenas_descifradas])

    count = len(lista_cadenas_descifradas)
    while True:
        try:
            cadena_descifrada_FINAL += next(next(cad_iter))
        except StopIteration:
            count -= 1
            if count == 0:
                break


    print("TEXTO DESCIFRADO: ")
    print(cadena_descifrada_FINAL)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descifra un texto cifrado con el algoritmo de Cezar')
    parser.add_argument('-f', '--file', type=str,help='Fichero de texto cifrado')
    args = parser.parse_args()

    start = time.time()
    main(args.file)
    print("--- %s seconds ---" % (time.time() - start))
