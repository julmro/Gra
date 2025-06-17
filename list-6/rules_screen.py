import pygame

click_sound = pygame.mixer.Sound("assets/sounds/click_fixed.wav") 

def show_rules(screen):
    """
    Wyświetla ekran z zasadami gry na podanym ekranie Pygame.

    Args:
        screen (pygame.Surface): Powierzchnia, na której rysowane są zasady.

    Funkcja wyświetla tekst z zasadami gry, dopasowuje tło oraz
    rysuje przycisk "Zamknij", który pozwala wyjść z ekranu po kliknięciu.
    
    Działa w pętli aż do momentu zamknięcia okna lub kliknięcia przycisku.
    """
    # Czcionki do różnych rozmiarów tekstu.
    font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 18)
    big_font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 28)

    # Wczytanie i dopasowanie tła do rozmiaru ekranu.
    background = pygame.image.load("assets/images/background2.png").convert()
    background = pygame.transform.scale(background, screen.get_size())

    screen.blit(background, (0, 0))

    # Zasady gry.
    lines = [
        "ZASADY GRY:",
        "",
        "1. Grasz przeciwko Czerwonemu Smokowi. ",
        "2. Kliknij na pole, aby umieścić swój awatar.",
        "3. Czerwony Smok wykonuje ruch automatycznie.",
        "4. Wygrywa ten, kto ułoży 3 swoje awatary w rzędzie.",
        "5. Remis: gdy plansza się zapełni.",
        "6. Za wygraną zdobywasz punkt.",
        "7. Za przegraną tracisz jedno życie.",
    ]

    # Rysowanie każdej linii tekstu zasad na ekranie.
    for i, line in enumerate(lines):
        text = font.render(line, True, (0, 0, 0))
        screen.blit(text, (20, 50 + i * 40))

    # Ustawienia przycisku "Zamknij".
    button_width, button_height = 160, 45
    button_x = 30  
    screen_width, screen_height = screen.get_size()
    button_y = screen_height - button_height - 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()

        # Rysowanie tła i zasad.
        screen.blit(background, (0, 0))
        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (20, 50 + i * 40))

        # Sprawdzenie, czy kursor znajduje się nad przyciskiem.
        is_hovered = button_rect.collidepoint(mouse_pos)
        # Zmiana koloru przycisku, gdy jest na nim kursor.
        button_color = (180, 0, 255) if is_hovered else (0, 0, 0)

        # Rysowanie prostokąta przycisku z zaokrąglonymi rogami
        pygame.draw.rect(screen, button_color, button_rect, border_radius=6)
        button_text = big_font.render("Zamknij", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        # Aktualizacja wyświetlanego obrazu.
        pygame.display.flip()

        # Obsługa zdarzeń: zamknięcie okna lub kliknięcie przycisku kończy pętlę.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                click_sound.play()
                waiting = False





