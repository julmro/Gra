import pygame
import config

click_sound = pygame.mixer.Sound("assets/sounds/click_fixed.wav") 

def show_scores(screen):
    """
    Wyświetla ekran z najlepszymi wynikami na podanym ekranie Pygame.

    Args:
        screen (pygame.Surface): Powierzchnia, na której rysowane jest menu wyników.

    Funkcja tworzy pętlę zdarzeń, w której wyświetla:
    - tło ekranu,
    - tytuł,
    - listę najlepszych wyników pobranych z config.get_top_scores(),
    - przycisk "Zamknij", który zamyka ekran wyników po kliknięciu.

    Obsługuje zdarzenia myszy oraz zamknięcia okna.

    Pętla działa aż do momentu zamknięcia okna lub kliknięcia przycisku "Zamknij".
    """
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 40)
    small_font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 20)
    tiny_font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 15)
    dif_font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 28)

    # Wczytanie i dopasowanie tła do rozmiaru ekranu.
    background = pygame.image.load("assets/images/background2.png").convert()
    background = pygame.transform.scale(background, screen.get_size())

    button_width, button_height = 160, 45
    button_x = 30  
    screen_width, screen_height = screen.get_size()
    button_y = screen_height - button_height - 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        # Tytuł.
        title = font.render("Najlepsze wyniki:", True, (0, 0, 0))
        screen.blit(title, (150, 30))

        # Pobranie najlepszych wyników z konfiguracji.
        scores = config.get_top_scores()

        # Wyświetlenie wyników lub komunikatu, jeśli lista jest pusta.
        if not scores:
            label = small_font.render("Brak wyników do wyświetlenia", True, (50, 50, 50))
            screen.blit(label, (150, 100))
        else:
            for i, entry in enumerate(scores):
                text = f"{i+1}. {entry['name']} - {entry['score']} pkt"
                label = small_font.render(text, True, (50, 50, 50))
                screen.blit(label, (150, 100 + i * 40))

        # Sprawdzenie, czy mysz znajduje się nad przyciskiem.
        is_hovered = button_rect.collidepoint(mouse_pos)
        button_color = (180, 0, 255) if is_hovered else (0, 0, 0)

        # Rysowanie przycisku "Zamknij".
        pygame.draw.rect(screen, button_color, button_rect, border_radius=6)
        button_text = dif_font.render("Zamknij", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        pygame.display.flip()

        # Obsługa zdarzeń.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                click_sound.play()
                running = False

        clock.tick(60)


