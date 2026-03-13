tablero = [
    ["♜","♞","♝","♛","♚","♝","♞","♜"],
    ["♟","♟","♟","♟","♟","♟","♟","♟"],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "," "],
    ["♙","♙","♙","♙","♙","♙","♙","♙"],
    ["♖","♘","♗","♕","♔","♗","♘","♖"]
]

def mostrar_tablero(tablero):
    print("  a b c d e f g h")
    for i, fila in enumerate(tablero):
        print(8-i, end=" ")
        for celda in fila:
            print(celda, end=" ")
        print(8-i)
    print("  a b c d e f g h")

def mover_pieza(tablero, origen, destino):
    columna_origen = ord(origen[0].lower()) - ord('a')
    fila_origen = 8 - int(origen[1])
    columna_destino = ord(destino[0].lower()) - ord('a')
    fila_destino = 8 - int(destino[1])
    
    pieza = tablero[fila_origen][columna_origen]
    if pieza == " ":
        print("No hay pieza en la casilla de origen.")
        return False
    tablero[fila_destino][columna_destino] = pieza
    tablero[fila_origen][columna_origen] = " "
    return True

while True:
    mostrar_tablero(tablero)
    origen = input("Ingresa la casilla de origen: ")
    destino = input("Ingresa la casilla de destino: ")
    mover_pieza(tablero, origen, destino)