import math

valores_comerciales = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

#R de 1k a 470k

esc_max = pow(10, -6)
paso = 10

nc1 = pow(10, -9)
nc2 = pow(10, -9)

error =  0.05

def es_potencia_aproximada(num, base):
    if (base == 1 and num != 1):
        return False
    if (base == 1 and num == 1):
        return True
    if (base == 0 and num != 1):
        return False

    power = int(math.log(num, base) + 0.5)

    return abs(num - base ** power) <= error * number #permito un 5% de error

def es_un_valor_comercial(valor):
    for i in range(len(valores_comerciales)):
        n = valor / valores_comerciales[i]
        if (es_potencia_aproximada(n, 10)):
            return Trueimport math


def devolver_valores_filtro(Wo, Q, Ho):
    valores_posibles = []

    Wo_2 = Wo ** Wo

    while (nc < esc_max):
        for ic1 in range(len(valores_comerciales)):
            for ic2 in range(len(valores_comerciales)):

                c1 = nc * (valores_comerciales[ic1])
                c2 = nc * (valores_comerciales[ic2])

                r1 = -Q / (c1 * Wo * Ho)

                if (not es_un_valor_comercial(r1)):
                    continue

                r3 = (( c1 + c2 ) / ( c1 * c2)) * ( Q / Wo )

                if (not es_un_valor_comercial(r3)):
                    continue

                r2 = 1 / ( ( Wo_2 * c1 * c2 * r3 ) - ( 1 / r1 ) )

                if (not es_un_valor_comercial(r2)):
                    continue

                valores_posibles.append(c1, c2, r1, r2, r3)

        nc *= 10

    return valores_posibles

def escribir_valores(valores, archivo, frecuencia):
    archivo.write("Frecuencia: {}".format(frecuencia))
    for circuito in valores_posibles:
        archivo.write("c1: {}, c2: {}, r1: {}, r2: {}, r3: {}"
            .format(circuito[0], circuito[1], circuito[2], circuito[3], circuito[4]))

def procesar_valores_transferencia(linea):
    linea_proc = [float(elem) for elem in linea.split()]
    return linea_proc[0], linea_proc[2], linea_proc[3], linea_proc[4]

if __name__ == '__main__':
    archivo_salida = open("salida.txt", "w")
    i = 0
    with open("entrada.txt", "r") as archivo_entrada:
        for linea in archivo_entrada:
            if i == 0:
                continue
            frecuencia, Wo, Q, Ho = procesar_valores_transferencia(linea)
            valores_posibles = devolver_valores_filtro(Wo, Q, Ho)
            escribir_valores(valores, archivo_salida, frecuencia)
            i += 0
    archivo_salida.close()
