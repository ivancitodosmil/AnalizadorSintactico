import json

# Cargar la tabla SLR desde el archivo JSON
with open("SLR_TABLES.json", "r", encoding="utf-8") as f:
    tablas = json.load(f)

tabla_accion = {int(k): v for k, v in tablas["action"].items()}
tabla_ir_a = {int(k): v for k, v in tablas["goto"].items()}

# Reglas de la gramática
reglas = {
    1: ("I'", ["I"]),
    2: ("I", ["inicio", "(", ")", "{", "B", "}"]),
    3: ("B", ["US"]),
    4: ("B", ["US", "B"]),
    5: ("US", ["DV"]),
    6: ("DV", ["V"]),
    7: ("DV", ["V", "DV"]),
    8: ("V", ["TV", "LV"]),
    9: ("TV", ["int"]),
    10: ("TV", ["double"]),
    11: ("LV", ["id"]),
    12: ("LV", ["id", ",", "LV"]),
    13: ("US", ["W"]),
    14: ("W", ["while", "(", "COND", ")", "{", "B", "}"]),
    15: ("US", ["IF"]),
    16: ("IF", ["if", "(", "COND", ")", "{", "B", "}", "else", "{", "B", "}"]),
    17: ("US", ["ASIGN"]),
    18: ("ASIGN", ["id", "=", "E"]),
    19: ("E", ["E", "+", "T"]),
    20: ("E", ["E", "-", "T"]),
    21: ("E", ["T"]),
    22: ("T", ["T", "*", "F"]),
    23: ("T", ["T", "/", "F"]),
    24: ("T", ["F"]),
    25: ("F", ["(", "E", ")"]),
    26: ("F", ["id"]),
    27: ("F", ["num"]),
    28: ("COND", ["id", "OPREL", "id"]),
    29: ("OPREL", [">"]),
    30: ("OPREL", ["<"]),
}


def analizador_desde_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for i, linea in enumerate(lineas, 1):
        entrada = linea.strip().split()
        if not entrada:
            continue  

        entrada.append("$")  # Aquí añado el Símbolo de fin de entrada

        pila = [0]
        puntero = 0
        derivacion = []

        print(f"\n📄 Analizando línea {i}: {' '.join(entrada[:-1])}")
        print(f"{'PILA':<60}│{'ENTRADA':<70}│{'ACCIÓN'}")
        print("─" * 140)

        while True:
            if puntero >= len(entrada):
                print("\n" + "❌ ERROR: Se alcanzó el final de la entrada sin encontrar '$'.".center(140))
                break

            estado = pila[-1]
            simbolo = entrada[puntero]
            accion = tabla_accion.get(estado, {}).get(simbolo, "")

            pila_str = " ".join(map(str, pila))
            entrada_str = " ".join(entrada[puntero:])
            print(f"{pila_str:<60}│{entrada_str:<70}│{accion}")

            if accion == "":
                print("\n" + f"❌ ERROR DE SINTAXIS en línea {i}".center(140))
                break

            if accion.startswith("s"):
                nuevo_estado = int(accion[1:])
                pila.append(simbolo)
                pila.append(nuevo_estado)
                puntero += 1
            elif accion.startswith("r"):
                num_regla = int(accion[1:])
                izquierda, derecha = reglas[num_regla]
                if derecha != ["ε"]:
                    for _ in range(len(derecha) * 2):
                        pila.pop()
                estado_actual = pila[-1]
                pila.append(izquierda)
                goto_estado = tabla_ir_a[estado_actual][izquierda]
                pila.append(goto_estado)
                derivacion.append(f"{izquierda} → {' '.join(derecha)}")
            elif accion == "acc":
                print("\n" + f"✅ LÍNEA {i} ACEPTADA".center(140))
                print("\n🌲 Árbol de derivación:")
                for prod in reversed(derivacion):
                    print(prod)
                break


# Ejecutar
analizador_desde_archivo("entrada.txt")
