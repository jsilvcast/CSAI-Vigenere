#! /usr/bin/python3
import argparse
import cProfile
import itertools
import time

import numpy as np
from multiprocessing import Process, Event, Manager

from freqs import frequency_array_27, frequency_array_26
import hashlib

def chr_to_number_27(char):
    number = ord(char) - 65
    if number >= 14:
        number += 1
    if number == 145:
        return 14
    return number

def chr_to_number_26(char):
    number = ord(char) - 65
    return number

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

def sorted_enumerate(seq):
    list = [0] * len(seq)
    k = 0
    for (_, i) in reversed(sorted((v, i) for (i, v) in enumerate(seq))):
        list[k] = i
        k += 1
    return list

def descifrar_cadena2(repeticiones, dictionary):
    repeticiones_desp = np.zeros((dictionary,dictionary), dtype=np.uint16)
    # repeticiones_desp_26 = np.zeros((26,26), dtype=np.uint16)
    # repeticiones_desp_26_27 = np.zeros((27,26), dtype=np.uint16)
    # repeticiones_26 = repeticiones_27[:-1]
    repeticiones_desp[0] = repeticiones
    # repeticiones_desp_26[0] = repeticiones_26
    # repeticiones_desp_26_27[0] = repeticiones_26
    for i in range(1, dictionary):
        repeticiones_desp[i] = np.roll(repeticiones, -i)
        # repeticiones_desp_26_27[i] = roll_repeticiones_desp_27[:-1]
        # if i < 26:
        #     repeticiones_desp_26[i] = np.roll(repeticiones_26, -i)

    if dictionary == 26:
        x = np.dot(repeticiones_desp, frequency_array_26)
    else:
        x = np.dot(repeticiones_desp, frequency_array_27)
    # x_26 = np.dot(repeticiones_desp_26, frequency_array_26)
    # x_26_27 = np.dot(repeticiones_desp_26_27, frequency_array_26)
    # print(np.argmax(np.max(x_27, axis=0), axis=0))
    return sorted_enumerate(x[:,0])[:5], sorted_enumerate(x[:,1])[:5], sorted_enumerate(x[:,2])[:5]


alfabeto_27 = b"ABCDEFGHIJKLMN\xb1OPQRSTUVWXYZ"
alfabeto_26 = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def transform(lista_cadenas, comb, length, dictionary, lista_cadenas2):
    for index in range(length):
        np.subtract(lista_cadenas[index], comb[index], out=lista_cadenas2[index])
        np.mod(lista_cadenas2[index], dictionary, out=lista_cadenas2[index])

def decode(lista_cadenas2, text_len, maxima, alfabeto):
    cadena_descifrada_FINAL = bytearray(text_len)
    j = 0
    for indice in range(maxima):
        for cad in lista_cadenas2:
            try:
                cadena_descifrada_FINAL[j] = alfabeto[cad[indice]]
                j += 1
            except:
                break
    return cadena_descifrada_FINAL

def check_product(lista_cadenas, lista_caracteres, length, maxima, text_len,
                  # foundit, quit,
                  dictionary, alfabeto, hash):

    lista_cadenas2 = [np.zeros(lista_cadenas[i].shape, dtype=np.int32) for i in range(length)]
    for comb in itertools.product(*lista_caracteres):
        transform(lista_cadenas, comb, length, dictionary, lista_cadenas2)

        cadena_descifrada_FINAL = decode(lista_cadenas2, text_len, maxima, alfabeto)
        # print(cadena_descifrada_FINAL)
        # print(hashlib.sha256(cadena_descifrada_FINAL).hexdigest())
        if hashlib.sha256(cadena_descifrada_FINAL).hexdigest() == hash:
            print(comb)
            print(cadena_descifrada_FINAL.decode())
            # foundit.set()
            # quit.set()
            return True
    # quit.set()

def kasiski_length(input_text, text_len, substring_len):
    # Iterate over all possible substrings until checkIfEnterInElse or text_len
    substring_found = {}
    for i in range(text_len - substring_len + 1):
        checkIfEnterInElse = False
        for j in range(substring_len, text_len - substring_len + 1):
            subcadena = input_text[j:j + substring_len]
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

    if len(substring_found) < 2:
        return 1

    for positions in substring_found.values():
        for i in range(len(positions) - 1):
            lista_distancias.append(positions[i + 1] - positions[i])

    # Descartamos mcd = 1 para evitar trigramas casuales que nos impidan
    # adivinar la longitud de la clave
    longitud_minima = lista_distancias[0]
    for i in lista_distancias[1:]:
        aux = gcd(longitud_minima, i)
        longitud_minima = aux
        if longitud_minima == 1:
            return longitud_minima

    return longitud_minima

def main(file_name, hash, dictionary):
    file_input = open(file_name, mode="r", encoding="utf-8")

    input_text = file_input.read().upper()
    text_len = len(input_text)

    # Substring length
    substring_lens = [3, 7, 11, 13]
    i = 0
    substring_len = substring_lens[0]
    longitud_minima = 1

    if dictionary == 26:
        alfabeto = alfabeto_26
        chr_to_number = chr_to_number_26
    else:
        alfabeto = alfabeto_27
        chr_to_number = chr_to_number_27

    while longitud_minima <= 1:
        print("Trying substring length:", substring_len)
        longitud_minima = kasiski_length(input_text, text_len, substring_len)
        i += 1
        substring_len = substring_lens[i]

    for longitud in range(longitud_minima, 20):
        print("Posible longitud de la clave: " + str(longitud))

        # Inicializamos a lista con tantos elementos como longitud ten a clave
        lista_subcadenas = [np.array(list(map(chr_to_number, input_text[i::longitud])), dtype=np.int32) for i in range(longitud)]

        repeticiones = np.zeros(dictionary, dtype=np.uint16)

        lista_caracteres_en = []
        lista_caracteres_es = []
        lista_caracteres_fr = []
        for cadena in lista_subcadenas:
            for ordinal in cadena:
                repeticiones[ordinal] += 1

            caracteres_en, caracteres_es, caracteres_fr = descifrar_cadena2(repeticiones, dictionary)
            lista_caracteres_en.append(caracteres_en)
            lista_caracteres_es.append(caracteres_es)
            lista_caracteres_fr.append(caracteres_fr)


        # f = functools.partial(check_product, result_key=result_key)
        # with Pool(3) as p:
        #     for return_value in p.map(f, [lista_caracteres_en, lista_caracteres_es, lista_caracteres_fr]):
        #         if return_value:
        #             return
        maxima = 0
        for cad in lista_subcadenas:
            if (len(cad)) > maxima:
                maxima = len(cad)
        length = len(lista_caracteres_en)

        reduced_lista_caracteres = [[] for x in range(longitud)]
        for number_of_caracteres in range(3, dictionary, 3):
            for i in range(len(lista_caracteres_es)):
                reduced_lista_caracteres[i] = lista_caracteres_es[i][:number_of_caracteres]
            if check_product(lista_subcadenas, reduced_lista_caracteres,
                            length, maxima, text_len,
                            # foundit, quit,
                            dictionary, alfabeto, hash):
                print("Español")
                return

            for i in range(len(lista_caracteres_es)):
                reduced_lista_caracteres[i] = lista_caracteres_en[i][:number_of_caracteres]

            if check_product(lista_subcadenas, reduced_lista_caracteres,
                            length, maxima, text_len,
                            # foundit, quit,
                            dictionary, alfabeto, hash):
                print("Inglés")
                return

            for i in range(len(lista_caracteres_es)):
                reduced_lista_caracteres[i] = lista_caracteres_fr[i][:number_of_caracteres]

            if check_product(lista_subcadenas, reduced_lista_caracteres,
                            length, maxima, text_len,
                            # foundit, quit,
                            dictionary, alfabeto, hash):
                print("Francés")
                return
        # return
        # foundit = Event()
        # quit = Event()
        # return
        # p_en = Process(target=check_product, args=(lista_subcadenas, lista_caracteres_en, length, maxima, text_len,
        #                                            foundit, quit, dictionary, alfabeto, hash))
        # p_es = Process(target=check_product, args=(lista_subcadenas, lista_caracteres_es, length, maxima, text_len,
        #                                            foundit, quit, dictionary, alfabeto, hash))
        # p_fr = Process(target=check_product, args=(lista_subcadenas, lista_caracteres_fr, length, maxima, text_len,
        #                                            foundit, quit, dictionary, alfabeto, hash))
        # p_en.start()
        # p_es.start()
        # p_fr.start()
        #
        # quit.wait()
        # if foundit.is_set():
        #     p_en.terminate()
        #     p_es.terminate()
        #     p_fr.terminate()
        #     return
        #
        # p_en.join()
        # p_es.join()
        # p_fr.join()
        # if foundit.is_set():
        #     return


        # if check_product(lista_caracteres_es, result_key=result_key):
        #     return
        #
        # if check_product(lista_caracteres_en, result_key=result_key):
        #     return
        #
        # if check_product(lista_caracteres_fr, result_key=result_key):
        #     return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descifra un texto cifrado con el algoritmo de Cezar')
    parser.add_argument('-f', '--file', type=str,help='Fichero de texto cifrado')
    parser.add_argument('-c', '--check', type=str, help='Hash to check')
    parser.add_argument('-d', '--dictionary', type=int, help='Dictionary')
    args = parser.parse_args()

    start = time.time()
    main(args.file, args.check, args.dictionary)
    # cProfile.run("main(args.file, args.check)")
    print("--- %s seconds ---" % (time.time() - start))
