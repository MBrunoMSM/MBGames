import pygame
import sys
import os

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo da Forca")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO_ESCURO = (139, 0, 0)
VERDE_ESCURO = (0, 100, 0)

fonte_inicial = pygame.font.Font(None, 40)
fonte_jogo = pygame.font.Font(None, 32)

pasta_imagens = "imagens"
forca_imagens = [pygame.image.load(os.path.join(pasta_imagens, f"forca_{i}.png")).convert_alpha() for i in range(8)]
logo_mbgames = pygame.transform.scale(pygame.image.load(os.path.join(pasta_imagens, "logo_mbgames.png")).convert_alpha(), (largura // 2, altura // 3))

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


        tela.blit(logo_mbgames, (largura // 4, altura // 8))

        texto_input = fonte_inicial.render("Digite a palavra em letras minúsculas e pressione enter:", True, PRETO)
        tela.blit(texto_input, (largura // 2 - texto_input.get_width() // 2, altura // 2 - texto_input.get_height() // 2))

        texto_palavra_digitada = fonte_inicial.render(palavra, True, PRETO)
        tela.blit(texto_palavra_digitada, (largura // 2 - texto_palavra_digitada.get_width() // 2, altura // 2 + 50))
        pygame.display.flip()

    return palavra

def desenhar_forca(tentativas_usadas):
    if 0 <= tentativas_usadas < 8:
        tela.blit(forca_imagens[tentativas_usadas], (largura // 4 - forca_imagens[tentativas_usadas].get_width() // 2, altura // 2 - forca_imagens[tentativas_usadas].get_height() // 2))

def tela_final(tentativas_usadas):
    tela.fill(BRANCO)
    if tentativas_usadas >= 7:
        mensagem = fonte_inicial.render("Ops! Você perdeu!", True, VERMELHO_ESCURO)
    else:
        mensagem = fonte_inicial.render("Parabéns, você ganhou!", True, VERDE_ESCURO)

    tela.blit(mensagem, (largura // 2 - mensagem.get_width() // 2, altura // 2))

    pygame.draw.rect(tela, (0, 128, 0), (largura // 2 - 100, altura // 2 + 50, 200, 50))  # Cor verde escura
    texto_botao = fonte_jogo.render("Jogar Novamente", True, BRANCO)
    tela.blit(texto_botao, (largura // 2 - texto_botao.get_width() // 2, altura // 2 + 75))

    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if largura // 2 - 100 <= mouse_x <= largura // 2 + 100 and altura // 2 + 50 <= mouse_y <= altura // 2 + 100:
                    return True

        pygame.time.Clock().tick(30)

def main():
    while True:
        palavra = pedir_palavra()
        palavra_oculta = ["_" for _ in palavra]
        tentativas_usadas = 0
        letras_usadas = []

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key >= 97 and evento.key <= 122:
                        letra = chr(evento.key).lower()

                        if letra in letras_usadas:
                            continue

                        letras_usadas.append(letra)
                        if letra in palavra:
                            for i in range(len(palavra)):
                                if palavra[i] == letra:
                                    palavra_oculta[i] = letra
                        else:
                            tentativas_usadas += 1

            tela.fill(BRANCO)

            desenhar_forca(tentativas_usadas)

            texto_palavra = fonte_jogo.render("Palavra: " + " ".join(palavra_oculta), True, PRETO)
            tela.blit(texto_palavra, (largura * 3 // 4 - texto_palavra.get_width() // 2, altura // 4 - texto_palavra.get_height() // 2))
            texto_tentativas = fonte_jogo.render("Tentativas usadas: " + str(tentativas_usadas), True, PRETO)
            tela.blit(texto_tentativas, (largura * 3 // 4 - texto_tentativas.get_width() // 2, altura // 2 + 10))
            texto_letras_usadas = fonte_jogo.render("Letras usadas: " + ", ".join(letras_usadas), True, PRETO)
            tela.blit(texto_letras_usadas, (largura * 3 // 4 - texto_letras_usadas.get_width() // 2, altura * 3 // 4 + 10))
            pygame.display.flip()

            if tentativas_usadas >= 7 or "_" not in palavra_oculta:
                pygame.time.wait(1000)
                if tela_final(tentativas_usadas):
                    break
                else:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
