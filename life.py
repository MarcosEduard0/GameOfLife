import pygame  # pip install pygame
import random
import time

largura, altura = input("Digite o tamanho da tela LxA: ").split('x')
largura, altura = int(largura), int(altura)
gridL, gridA = int(largura/10), int(altura/10)
print(gridL, gridA)

# empty plane
plano = [[0 for _ in range(gridA)] for _ in range(gridL)]
temp = [[0 for _ in range(gridA)] for _ in range(gridL)]


pygame.init()
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Game of Life')


def desenha(matrix):
    # preenche a tela com azul
    screen.fill([0, 0, 128])

    # percorre o plano desenhando as celulas
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell:
                # se a celula estiver viva desenhe um quadrado branco
                pygame.draw.rect(
                    screen, (255, 255, 255), (10*c, 10*r, 10, 10)
                )


def processa(matrix):

    for y in range(gridA):
        for x in range(gridL):
            vivos = vizinhos_vivos(x, y, matrix)
            # Regra 1 - Any live cell with fewer than two live neighbours dies, as if caused by under-population.
            if matrix[x][y] == 1 and vivos < 2:
                temp[x][y] = 0
            # Regra 2 - Any live cell with two or three live neighbours lives on to the next generation.
            if matrix[x][y] == 1 and (vivos == 2 or vivos == 3):
                temp[x][y] = 1
            # Regra 3 - Any live cell with more than three live neighbours dies, as if by overcrowding.
            if matrix[x][y] == 1 and vivos > 3:
                temp[x][y] = 0
            # Regra 4 - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            if matrix[x][y] == 0 and vivos == 3:
                temp[x][y] = 1
    for y in range(gridA):
        for x in range(gridL):
            matrix[x][y] = temp[x][y]

    return matrix


def vizinhos_vivos(a, b, vizinho):
    vivos = 0

    # if vizinho[a-1][b+1] == 1:
    #     vivos = vivos + 1
    # if vizinho[a][b+1] == 1:
    #     vivos = vivos + 1
    # if vizinho[a+1][b+1] == 1:
    #     vivos = vivos + 1
    # if vizinho[a-1][b] == 1:
    #     vivos = vivos + 1
    # if vizinho[a+1][b] == 1:
    #     vivos = vivos + 1
    # if vizinho[a-1][b-1] == 1:
    #     vivos = vivos + 1
    # if vizinho[a][b-1] == 1:
    #     vivos = vivos + 1
    # if vizinho[a+1][b-1] == 1:
    #     vivos = vivos + 1
    if vizinho[a-1][(b+1) % gridA] == 1:
        vivos += 1
    if vizinho[a][(b+1) % gridA] == 1:
        vivos += 1
    if vizinho[(a+1) % gridL][(b+1) % gridA] == 1:
        vivos += 1
    if vizinho[a-1][b] == 1:
        vivos += 1
    if vizinho[(a+1) % gridL][b] == 1:
        vivos += 1
    if vizinho[a-1][b-1] == 1:
        vivos += 1
    if vizinho[a][b-1] == 1:
        vivos += 1
    if vizinho[(a+1) % gridL][b-1] == 1:
        vivos += 1
    return vivos


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y+h), [x + w, y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


def start():
    global plano
    plano = [[random.choice([0, 1]) for _ in range(gridA)]
             for _ in range(gridL)]
    # desenha a geração inicial
    desenha(plano)
    pygame.display.update()
    # espera alguns segundos para que possamos ver a geração inicial antes de começar
    time.sleep(1.5)

    gameLife()


def gameLife():
    global plano
    run = True
    while run:
        # Verificação de evento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sai do programa clicando no X da janela
                run = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # sai do programa apertando ESC
                run = False

        # processa a nova geração
        plano = processa(plano)

        # desenha a nova geração na tela
        desenha(plano)

        pygame.display.update()
        # esperar antes de ir para proxima geração
        time.sleep(0.05)


def escolher():
    global plano
    desenha(plano)
    # loop para o usuario desenhar como quer o joho
    button(screen, (0, 0), "ENTER para iniciar")
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sai do programa clicando no X da janela
                run = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # sai do programa apertando ESC
                run = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return gameLife()
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                x, y = pygame.mouse.get_pos()
                plano[int(y/10)][int(x/10)] = 1
                desenha(plano)

        pygame.display.update()


def menu():
    b1 = button(screen, (50, 300), "Escolher")
    b2 = button(screen, (300, 300), "Aleatorio")
    run = True
    while run:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    return escolher()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    return start()
        pygame.display.update()

    pygame.quit()


menu()
