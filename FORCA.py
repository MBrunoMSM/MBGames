import pygame
import sys
import random

pygame.init()

# Configurações da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Forca")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.Font(None, 48)

def pedir_palavra():
    input_ativo = True
    palavra = ""

    while input_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    input_ativo = False
                elif evento.key == pygame.K_BACKSPACE:
                    palavra = palavra[:-1]
                else:
                    palavra += evento.unicode

        tela.fill(BRANCO)
        texto_input = fonte.render("Digite a palavra e pressione Enter: " + palavra, True, PRETO)
        tela.blit(texto_input, (largura // 2 - texto_input.get_width() // 2, altura // 2 - texto_input.get_height() // 2))
        pygame.display.flip()

    return palavra

def main():
    palavra = pedir_palavra()
    palavra_oculta = ["_" for _ in palavra]
    tentativas = 7
    letras_usadas = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key >= 97 and evento.key <= 122:  # A-Z keys
                    letra = chr(evento.key).lower()

                    if letra in letras_usadas:
                        continue

                    letras_usadas.append(letra)
                    if letra in palavra:
                        for i in range(len(palavra)):
                            if palavra[i] == letra:
                                palavra_oculta[i] = letra
                    else:
                        tentativas -= 1

        tela.fill(BRANCO)

        texto_palavra = fonte.render("Palavra: " + " ".join(palavra_oculta), True, PRETO)
        tela.blit(texto_palavra, (largura // 2 - texto_palavra.get_width() // 2, altura // 4))

        texto_tentativas = fonte.render("Tentativas: " + str(tentativas), True, PRETO)
        tela.blit(texto_tentativas, (largura // 2 - texto_tentativas.get_width() // 2, altura // 2))

        texto_letras_usadas = fonte.render("Letras usadas: " + ", ".join(letras_usadas), True, PRETO)
        tela.blit(texto_letras_usadas, (largura // 2 - texto_letras_usadas.get_width() // 2, altura * 3 // 4))

        pygame.display.flip()

        if tentativas <= 0 or "_" not in palavra_oculta:
            break

    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
