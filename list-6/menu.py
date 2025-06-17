import pygame
import avatar_selector 
 
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Menu Główne")

# Menu.
DIR = "c:/Users/jzmro/OneDrive/Dokumenty/GitHub/Gra/list-6/"
font = pygame.font.Font(DIR + "assets/fonts/PirataOne-Regular.ttf", 24)
menu_options = ["Nowa Gra", "Zasady", "Wybierz avatara", "Wyniki", "O Grze", "Wyjdź"]


def draw_menu(screen, selected_option, mouse_pos):
    """
    Rysuje menu główne na ekranie, podświetlając opcję
    wybraną kursorem lub zaznaczoną klawiaturą.

    Args:
        screen (pygame.Surface): powierzchnia do rysowania menu.
        selected_option (int): indeks aktualnie wybranej opcji.
        mouse_pos (tuple): aktualna pozycja myszy.

    Returns:
        list[pygame.Rect]: lista prostokątów.
    """
    option_rects = []
    for i, option in enumerate(menu_options):
        label = font.render(option, True, (0, 0, 0))
        rect = label.get_rect(center=(300, 230 + i * 30))
        option_rects.append(rect)

        # Kolor zależy od stanu (najechanie myszką, zaznaczenie klawiaturą).
        if rect.collidepoint(mouse_pos):
            color = (138, 43, 226)  # Fiolet.
        elif i == selected_option:
            color = (255, 0, 0)  # Czerwony.
        else:
            color = (0, 0, 0)  # Czarny.

        # Cień dla lepszej czytelności tekstu.
        shadow = font.render(option, True, (255, 255, 255))
        screen.blit(shadow, (rect.x + 2, rect.y + 2))
        label = font.render(option, True, color)
        screen.blit(label, rect)

    return option_rects

def choose_avatar():
    """Wywołuje funkcję wyboru avatara z modułu avatar_selector."""
    avatar_selector.avatar_selector()

def main():
    """
    Główna pętla programu obsługująca menu główne.
    Wykrywa kliknięcia myszy i naciskanie klawiszy,
    odtwarza dźwięk kliknięcia oraz wywołuje odpowiednie akcje.
    """
    pygame.init()

    # Dźwięk kliknięcia.
    DIR = "c:/Users/jzmro/OneDrive/Dokumenty/GitHub/Gra/list-6/"
    click_sound = pygame.mixer.Sound(DIR + "assets/sounds/click_fixed.wav")
    print("Głośność dźwięku kliknięcia:", click_sound.get_volume())

    selected_option = 0
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((255, 255, 255)) 
        option_rects = draw_menu(screen, selected_option, mouse_pos)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        click_sound.play()  # Dźwięk kliknięcia.
                        selected_option = i
                        if menu_options[selected_option] == "Wybierz avatara":
                            choose_avatar()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    click_sound.play()

    pygame.quit()

if __name__ == "__main__":
    main()
