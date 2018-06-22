import math

valores_comerciales = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

#R de 1k a 470k

esc_max = pow(10, -6)
paso = 10

nc1 = pow(10, -9)
nc2 = pow(10, -9)

error =  0.0045

def es_potencia_aproximada(num, base):
    if (base == 1 and num != 1):
        return False
    if (base == 1 and num == 1):
        return True
    if (base == 0 and num != 1):
        return False

    power = int(math.log(num, base) + 0.5)

    return abs(num - base ** power) <= error * num #permito un 5% de error

def es_un_valor_comercial(valor):
    if (valor <= 0):
        return False
    for i in range(len(valores_comerciales)):
        n = valor / valores_comerciales[i]
        if (es_potencia_aproximada(n, 10)):
            return True
    return False


def devolver_valores_filtro(Wo, Q, Ho):
    valores_posibles = []
    Wo_2 = Wo ** 2
    nc = nc1

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

                den_r2 = ( ( Wo_2 * c1 * c2 * r3 ) - ( 1 / r1 ) )

                if (den_r2 <= 0):
                    continue

                r2 = 1 / den_r2

                if (not es_un_valor_comercial(r2)):
                    continue

                valores_posibles.append((c1, c2, r1, r2, r3))

        nc *= 10

    return valores_posibles

def escribir_valores(valores, archivo, frecuencia):
    archivo.write("Frecuencia: {}\n".format(frecuencia))
    for circuito in valores_posibles:
        archivo.write("c1: {}, c2: {}, r1: {}, r2: {}, r3: {}\n"
            .format(circuito[0], circuito[1], circuito[2], circuito[3], circuito[4]))

def procesar_valores_transferencia(linea):
    linea_proc = [float(elem) for elem in linea.split()]
    return linea_proc[0], linea_proc[2], linea_proc[3], -linea_proc[4]

if __name__ == '__main__':
    archivo_salida = open("pasabanda_resultados_comerciales.txt", "w")
    i = -1
    with open("pasabanda_resultados.txt", "r") as archivo_entrada:
        for linea in archivo_entrada:
            i += 1
            if i == 0:
                continue
            frecuencia, Wo, Q, Ho = procesar_valores_transferencia(linea)
            valores_posibles = devolver_valores_filtro(Wo, Q, Ho)
            if (len(valores_posibles) > 0):
                escribir_valores(valores_posibles, archivo_salida, frecuencia)
    archivo_salida.close()
