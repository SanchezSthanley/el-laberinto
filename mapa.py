import random

TILE = 20

def generar_mapas(ancho_px, alto_px):
    columnas = ancho_px // TILE
    filas = alto_px // TILE

    # Inicializar laberinto lleno de paredes (1)
    laberinto = [[1 for _ in range(columnas)] for _ in range(filas)]

    # DFS para generar caminos
    def dfs(x, y):
        laberinto[y][x] = 0
        direcciones = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 < nx < columnas-1 and 0 < ny < filas-1:
                if laberinto[ny][nx] == 1:
                    laberinto[y + dy//2][x + dx//2] = 0
                    dfs(nx, ny)

    dfs(1,1)

    # Hacer entrada y salida
    laberinto[1][0] = 0
    laberinto[filas-2][columnas-1] = 0

    return laberinto, filas, columnas