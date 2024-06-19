from Interfaces.menuinterface import ButtonInterface
import pygame, sys
import game

class Button(ButtonInterface):
	def __init__(self, image : pygame.image, pos : list, text_input : str, font : pygame.font, base_color : str, hovering_color : str) -> None:
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen : pygame.display) -> None:
          # Desenha o botao na tela
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def check_for_input(self, position : list) -> bool:
          # Checa se o botao foi apertado com o clique
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def change_color(self, position : list) -> None:
          # Muda a cor do botao quando o mouse passa por cima
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
            

# Algumas variaveis globais sao inicializadas aqui
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
background = pygame.image.load("assets/Background.png")

def get_font(size) -> pygame.font:
    """
    Importa a fonte utilizada no menu
    """
    return pygame.font.Font("assets/font.ttf", size)

def play() -> None:
    """
    Roda a funcao principal Game.run()
    """
    my_game = game.Game()
    my_game.game_run()
    
def options() -> None:
    """
    Cria o menu de opcoes, e imprime a frase "esse e o menu de opcoes" ate que o botao voltar seja apertado
    """
    while True:
        options_pos = pygame.mouse.get_pos()

        screen.fill("white")

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        options_rect = options_text.get_rect(center=(640, 260))
        screen.blit(options_text, options_rect)

        options_back = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        options_back.change_color(options_pos)
        options_back.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.check_for_input(options_pos):
                    main_menu()

        pygame.display.update()

def main_menu():
    """ 
    Garante o funcionamento do main_menu, uma especie de main que define se o game vai rodar, para isso ele cria diversos botoes interativos que sao clicaveis
    
    """
    while True:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="Green", hovering_color="White")
        options_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="Green", hovering_color="White")
        quit_button = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="Green", hovering_color="White")

        screen.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()