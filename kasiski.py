#! /usr/bin/python3


def esDivisible(numero, lista):
    '''
            Return True:
                    si el numero no deja resto
                    con todos los números de la lista
    '''
    divisible = True
    for i in lista:
        if not i % numero == 0:
            divisible = False
            break
    return divisible


def mcd(numeros):
    '''
            Calcula el maximo común divisor
            * Numeros: es una lista de enteros
    '''
    mcd = 1
    numeros.sort()  # ordena la lista de menor a mayor
    # recorre hasta el numero mayor de la lista (el último)
    for i in range(2, numeros[-1] + 1):
        if esDivisible(i, numeros):
            mcd = i
    return mcd


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


def main():

    archivo_entrada = open("entrada_kasiski.txt", "r")

    texto_entrada = archivo_entrada.read()

    len_texto = len(texto_entrada)

    # Almacena de forma temporal a ubicación dos grupos repetidos de letras e
    # a súa distancia entre elas
    subcadenas_encontradas = {}

    # Lonxitude dos grupos de letras repetidas
    tam_subcadena = 3

    # Mentras o tamaño de cadena sexa máis pequeno que a lonxitude do texto
    # (Para buscar grupos de letras con todas as lonxitudes posibles)
    while tam_subcadena < len_texto:
        for i in range(len_texto):
            if i + tam_subcadena > len_texto:
                    # Avanza caracter a caracter (i) ata que chega ao final
                break

            # Conxunto de caracteres que recorremos
            subcadena_aux = texto_entrada[i:(i + tam_subcadena)]

            # Se se repite a subcadena polo menos duas veces
            if texto_entrada.count(subcadena_aux) >= 2:

                # Chapuza para poder borrar dentro do bucle
                subcadenas_encontradas_iterable = dict(subcadenas_encontradas)
                for key in subcadenas_encontradas_iterable.keys():
                    # Subcadena de maior tamaño repetida
                    # Borramos a máis pequena
                    if (key in subcadena_aux) and (key != subcadena_aux):
                        del subcadenas_encontradas[key]
                        break

                # Gardamos de forma provisional a subcadena máis a posición donde
                # acaba, (usamos -1 porque a cadena empeza en 0)
                if subcadenas_encontradas.get(subcadena_aux, None) == None:
                    subcadenas_encontradas[subcadena_aux] = [texto_entrada.find(
                        subcadena_aux, i) + (tam_subcadena - 1)]
                else:
                    lista_inicial = subcadenas_encontradas.get(subcadena_aux)
                    lista_inicial.append(texto_entrada.find(
                        subcadena_aux, i) + (tam_subcadena - 1))
                    subcadenas_encontradas[subcadena_aux] = lista_inicial

        tam_subcadena += 1

    # print(subcadenas_encontradas)
    # print()

    # Lista de distancias calculada a partir do diccionario temporal
    lista_distancias = []

    for key in subcadenas_encontradas.keys():
        for index, item in enumerate(reversed(subcadenas_encontradas[key])):
            if len(subcadenas_encontradas[key]) > (index + 1):
                lista_distancias.append(subcadenas_encontradas[key][
                    index + 1] - subcadenas_encontradas[key][index])

    # print(lista_distancias)
    # print()

    # Descartamos mcd = 1 para evitar trigramas casuales que nos impidan
    # adivinar la longitud de la clave
    longitud = lista_distancias[0]
    for i in range(len(lista_distancias)):
        if(i + 1 <= len(lista_distancias)):
            aux1 = mcd([lista_distancias[i], longitud])
            if (aux1 != 1):
                longitud = aux1

    print("La posible longitud de la clave es: " + str(longitud))
    print()

    # Inicializamos a lista con tantos elementos como longitud ten a clave
    lista_subcadenas = []
    for a in range(longitud):
        lista_subcadenas.append("")

    # Creamos as diferentes cadenas de distintos alfabetos
    count = 0
    for j in texto_entrada:
        lista_subcadenas[count] = lista_subcadenas[count] + j
        count += 1
        if count >= longitud:
            count = 0

    for a in range(longitud):
        print("Cadena " + str(a) + ": " + lista_subcadenas[a])
        print()

    dict_repeticiones = {}
    lista_cadenas_descifradas = []

    print("Aplicando algoritmo AEOS...")
    print("La posible clave es: ", end="")
    for b in range(longitud):
        for i in lista_subcadenas[b]:
            if i in dict_repeticiones.keys():
                dict_repeticiones[i] = dict_repeticiones.get(i) + 1
            else:
                dict_repeticiones[i] = 1
        lista_ordenada = sortTuple(list(dict_repeticiones.items()))

        
        cadena_descifrada = descifrar_cadena(
            lista_subcadenas[b], dict_repeticiones)
        lista_cadenas_descifradas.append(cadena_descifrada)

        dict_repeticiones = {}

    print("\n")

    # Calculamos a lonxitude maxima que poden ter as cadenas
    maxima = 0
    for cad in lista_cadenas_descifradas:
        if (len(cad)) > maxima:
            maxima = len(cad)

    # Desciframos por fin :)
    cadena_descifrada_FINAL = ""
    for indice in range(maxima):
        for cad in lista_cadenas_descifradas:
            if (indice < maxima) and (indice < len(cad)):
                cadena_descifrada_FINAL = cadena_descifrada_FINAL + cad[indice]

    print("TEXTO DESCIFRADO: ")
    print(cadena_descifrada_FINAL)
    print()

if __name__ == '__main__':
    main()
