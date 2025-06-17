import pygame
import sys
import menu
import rules_screen
import scores_screen
import about_screen
import game

def get_text_input(screen, background, prompt="Podaj swoje imię i kliknij Enter:"):
    """
    Wyświetla ekran do wpisywania tekstu przez użytkownika.
    
    Args:
        screen (pygame.Surface): powierzchnia, na której wyświetlany jest input.
        background (pygame.Surface): tło ekranu inputu.
        prompt (str): tekst wyświetlany jako podpowiedź dla użytkownika.
    
    Returns:
        str: wprowadzony przez użytkownika tekst (lub "Gracz", jeśli nic nie wpisano).
    """
    pygame.font.init()
    font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 36)
    input_text = ""
    clock = pygame.time.Clock()

    while True:
        screen.blit(background, (0, 0))

        prompt_surface = font.render(prompt, True, (0, 0, 0))
        input_surface = font.render(input_text + "_", True, (0, 0, 0))

        screen.blit(prompt_surface, (50, 200))
        screen.blit(input_surface, (50, 260))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text.strip() if input_text.strip() else "Gracz"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(event.unicode) == 1 and event.unicode.isprintable():
                        input_text += event.unicode

        clock.tick(30)

def main():
    """
    Główna pętla programu wyświetlająca menu główne,
    obsługująca nawigację klawiaturą i myszą oraz
    wywołująca odpowiednie funkcje w zależności od wyboru użytkownika.
    """
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Kółko i Krzyżyk")

    # Tło menu.
    try:
        background_menu = pygame.image.load("assets/images/background.png").convert()
        background_menu = pygame.transform.scale(background_menu, (600, 600))
    except Exception as e:
        print("Błąd ładowania tła menu:", e)
        background_menu = None

    # Tło do ekranu wpisywania imienia.
    try:
        background_input = pygame.image.load("assets/images/background2.png").convert()
        background_input = pygame.transform.scale(background_input, (600, 600))
    except Exception as e:
        print("Błąd ładowania tła input:", e)
        background_input = pygame.Surface((600, 600))
        background_input.fill((255, 255, 255))  

    selected_option = 0
    player_name = None  
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Wyświetl tło menu lub białe tło jeśli nie udało się załadować obrazka.
        if background_menu:
            screen.blit(background_menu, (0, 0))
        else:
            screen.fill((255, 255, 255)) 

        option_rects = menu.draw_menu(screen, selected_option, mouse_pos)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu.menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu.menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if selected_option == 0:
                        player_name = get_text_input(screen, background_input)
                    handle_option(selected_option, player_name, screen)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            player_name = get_text_input(screen, background_input)
                        handle_option(i, player_name, screen)

        clock.tick(30)

def handle_option(option, player_name, screen):
    """
    Obsługuje wykonanie wybranej opcji z menu.

    Args:
        option (int): indeks wybranej opcji menu.
        player_name (str): imię gracza (wprowadzone przez użytkownika).
        screen (pygame.Surface): powierzchnia do wyświetlania kolejnych ekranów.
    """
    if option == 0:
        game.start_game(screen, player_name)
    elif option == 1:
        rules_screen.show_rules(screen)
    elif option == 2:
        menu.choose_avatar()
    elif option == 3:
        scores_screen.show_scores(screen)
    elif option == 4:
        about_screen.show_about(screen)
    elif option == 5:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
