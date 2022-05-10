#! /usr/bin/python3
import cProfile
import sys
import time

import numpy as np

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

def descifrar_cadena_final(repeticiones, frequency_array):
    frequency_array = frequency_array / 100
    repeticiones = repeticiones / repeticiones.sum()
    x_power = np.power(np.subtract(repeticiones, frequency_array), 2)
    xx1 = np.divide(x_power, frequency_array, where=frequency_array!=0)
    return np.sum(xx1, where=xx1!=np.inf, axis=0)


def descifrar_cadena(repeticiones_desp, frequency_array):
    x_power = np.power(np.subtract(repeticiones_desp, frequency_array), 2)
    xx1 = np.divide(x_power, frequency_array, where=frequency_array!=0)
    xx2 = np.sum(xx1, where=xx1!=np.inf, axis=1)
    index_min = np.argmin(xx2)

    return index_min, xx2[index_min]

def multi_solve(lista_subcadenas, frequency_array):
    key = []
    value = 0
    for cadena in lista_subcadenas:
        # repeticiones = np.zeros(dictionary, dtype=np.uint32)
        # for ordinal in cadena:
        #     repeticiones[ordinal] += 1

        index_min, value_min = descifrar_cadena(cadena, frequency_array)
        key.append(index_min)
        value += value_min
    return key, value

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

enFrequency_array_26 = np.array([8.34,1.54,2.73,4.14,12.6,2.03,1.92,6.11,6.71,0.23,0.87,4.24,2.53,6.8,7.7,1.66,0.09,5.68,6.11,9.37,2.85,1.06,2.34,0.2,2.04,0.06])
enFrequency_array_27 = np.array([8.34,1.54,2.73,4.14,12.6,2.03,1.92,6.11,6.71,0.23,0.87,4.24,2.53,6.8,0,7.7,1.66,0.09,5.68,6.11,9.37,2.85,1.06,2.34,0.2,2.04,0.06])

esFrequency_array_26 = np.array([12.027,2.215,4.019,5.010,12.614,0.692,1.768,0.703,6.972,0.493,0.011,4.967,3.157,6.712,9.51,2.510,0.877,6.871,7.977,4.632,3.107,1.138,0.017,0.215,1.008,0.467])
esFrequency_array_27 = np.array([12.027,2.215,4.019,5.010,12.614,0.692,1.768,0.703,6.972,0.493,0.011,4.967,3.157,6.712,0.311,9.51,2.510,0.877,6.871,7.977,4.632,3.107,1.138,0.017,0.215,1.008,0.467])

frFrequency_array_26 = np.array([8.7,0.93,3.16,3.55,17.82,0.96,0.97,1.08,6.98,0.71,0.16,5.68,3.23,6.42,5.34,3.03,0.89,6.43,7.91,7.11,6.1,1.83,0.04,0.42,0.19,0.21])
frFrequency_array_27 = np.array([8.7,0.93,3.16,3.55,17.82,0.96,0.97,1.08,6.98,0.71,0.16,5.68,3.23,6.42,0,5.34,3.03,0.89,6.43,7.91,7.11,6.1,1.83,0.04,0.42,0.19,0.21])

frequency_list_26 = [esFrequency_array_26, enFrequency_array_26, frFrequency_array_26]
frequency_list_27 = [esFrequency_array_27, enFrequency_array_27, frFrequency_array_27]

alfabeto_26 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alfabeto_27 = "ABCDEFGHIJKLMN\xb1OPQRSTUVWXYZ"

def main(file_name):
    file_input = open(file_name, mode="r", encoding="utf-8")

    input_text = file_input.read().upper()
    text_len = len(input_text)

    # Substring length
    substring_lens = [3, 7, 11, 13]
    i = 0
    substring_len = substring_lens[0]
    longitud_minima = 1

    with_n = input_text.find("Ñ") > 0

    while longitud_minima <= 1:
        print("Trying substring length:", substring_len)
        longitud_minima = kasiski_length(input_text, text_len, substring_len)
        i += 1
        substring_len = substring_lens[i]

    # longitud_minima = 2
    while True:
        print("Posible longitud de la clave: " + str(longitud_minima))

        # Inicializamos a lista con tantos elementos como longitud ten a clave


        lista_subcadenas_27 = [np.array(list(map(chr_to_number_27, input_text[i::longitud_minima])), dtype=np.int32)
                               for i in range(longitud_minima)]
        for cadena_index in range(len(lista_subcadenas_27)):
            repeticiones = np.zeros(27, dtype=np.uint32)
            cadena = lista_subcadenas_27[cadena_index]
            for ordinal in cadena:
                repeticiones[ordinal] += 1
            repeticiones_desp = np.zeros((27, 27), dtype=np.compat.long)
            repeticiones_desp[0] = repeticiones
            for i in range(1, 27):
                repeticiones_desp[i] = np.roll(repeticiones, -i)
            lista_subcadenas_27[cadena_index] = repeticiones_desp

        if with_n:
            combinations = [(lista_subcadenas_27, esFrequency_array_27),
                            (lista_subcadenas_27, enFrequency_array_27),
                            (lista_subcadenas_27, frFrequency_array_27)]

        else:
            lista_subcadenas_26 = [np.array(list(map(chr_to_number_26, input_text[i::longitud_minima])), dtype=np.int32)
                                   for i in range(longitud_minima)]
            for cadena_index in range(len(lista_subcadenas_27)):
                repeticiones = np.zeros(26, dtype=np.uint32)
                cadena = lista_subcadenas_26[cadena_index]
                for ordinal in cadena:
                    repeticiones[ordinal] += 1
                repeticiones_desp = np.zeros((26, 26), dtype=np.compat.long)
                repeticiones_desp[0] = repeticiones
                for i in range(1, 26):
                    repeticiones_desp[i] = np.roll(repeticiones, -i)
                lista_subcadenas_26[cadena_index] = repeticiones_desp

            combinations = [(lista_subcadenas_26, esFrequency_array_26),
                            (lista_subcadenas_26, enFrequency_array_26),
                            (lista_subcadenas_26, frFrequency_array_26),
                            (lista_subcadenas_27, esFrequency_array_27),
                            (lista_subcadenas_27, enFrequency_array_27),
                            (lista_subcadenas_27, frFrequency_array_27)]


        results = [multi_solve(*comb) for comb in combinations]

        key = results[0][0]
        value = results[0][1]
        index = 0
        for result_index in range(len(results)):
            if value > results[result_index][1]:
                key = results[result_index][0]
                value = results[result_index][1]
                index = result_index

            # print(results[result_index][0], results[result_index][1])
        if with_n:
            repeticiones = lista_subcadenas_27[0][key[0]]
            for key_dep_index in range(1, longitud_minima):
                 repeticiones = repeticiones + lista_subcadenas_27[key_dep_index][key[key_dep_index]]

            score = descifrar_cadena_final(repeticiones, frequency_list_27[index % 3])

            if score < 0.1:
                clave_final = ""
                for x in key:
                    clave_final += alfabeto_27[x]
                print(clave_final)
                return
        else:
            if index < 3:
                repeticiones = lista_subcadenas_26[0][key[0]]
                for key_dep_index in range(1, longitud_minima):
                    repeticiones = repeticiones + lista_subcadenas_26[key_dep_index][key[key_dep_index]]
                score = descifrar_cadena_final(repeticiones, frequency_list_26[index % 3])

                if score < 0.1:
                    clave_final = ""
                    for x in key:
                        clave_final += alfabeto_26[x]
                    print(clave_final)
                    return

            else:
                repeticiones = lista_subcadenas_27[0][key[0]]
                for key_dep_index in range(1, longitud_minima):
                    repeticiones = repeticiones + lista_subcadenas_27[key_dep_index][key[key_dep_index]]
                score = descifrar_cadena_final(repeticiones, frequency_list_27[index % 3])

                if score < 0.1:
                    clave_final = ""
                    for x in key:
                        clave_final += alfabeto_27[x]
                    print(clave_final)
                    return


        longitud_minima += 1

if __name__ == '__main__':
    start = time.time()
    main(sys.argv[1])
    # cProfile.run("main(sys.argv[1])")
    print("--- %s seconds ---" % (time.time() - start))
