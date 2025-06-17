import pygame
import config

def avatar_selector():
    """
    Uruchamia ekran wyboru awatara dla gracza.

    Użytkownik może wybrać jedną z dostępnych postaci, zobaczyć opis ich bonusów (legenda),
    lub zrezygnować z wyboru. Wybrany awatar zostaje ustawiony w konfiguracji gry.

    Obsługuje:
    - wyświetlanie tła, avatarów, przycisków,
    - podświetlanie avatarów i przycisków przy najechaniu myszką,
    - wybór avatara i zatwierdzanie wyboru,
    - wyświetlanie legendy z opisem bonusów postaci,
    - dźwięk kliknięcia przy każdym kliknięciu myszy,
    - zamykanie okna wyboru.

    Pliki wymagane:
    - avatary: assets/avatars/avatar1.png, avatar3.png, avatar4.png
    - dźwięk kliknięcia: assets/sounds/click.wav
    - tło: assets/images/background2.png
    - czcionki: assets/fonts/EagleLake-Regular.ttf, assets/fonts/PirataOne-Regular.ttf
    """
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Wybierz awatara")

    # Wymiary przycisków.
    BUTTON_WIDTH = 160
    BUTTON_HEIGHT = 45

    # Załaduj tło i przeskaluj.
    background = pygame.image.load("assets/images/background2.png").convert()
    background = pygame.transform.scale(background, (600, 600))

    # Czcionki.
    font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 30)
    small_font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 28)
    label_font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 22)

    # Wczytaj avatary (tylko wybrane, indeksy zgodne z config.py).
    avatar_paths = [
        "assets/avatars/avatar1.png",
        "assets/avatars/avatar3.png",
        "assets/avatars/avatar4.png"
    ]
    avatar_global_indices = [0, 2, 3]  # odpowiadające indeksy w config.py

    avatars = [pygame.image.load(path) for path in avatar_paths]
    avatars = [pygame.transform.smoothscale(img, (150, 150)) for img in avatars]

    avatar_names = ["Jednorożec", "Dobry Smok", "Otto (niedźwiedź x pies)"]
    avatar_bonuses = [
        "Jednorożec: Dodatkowe 3 życia.",
        "Dobry Smok: Punkt za remis.",
        "Otto (niedźwiedź x pies): Punkty",
        "za wygraną liczą się podwójnie."
    ]

    positions = [(120, 180), (330, 180), (225, 365)]  # pozycje avatarów

    selected_index = None  # wybrany avatar lokalny indeks

    # Definicje prostokątów przycisków.
    button_rect = pygame.Rect(220, 530, BUTTON_WIDTH, BUTTON_HEIGHT)
    legend_rect = pygame.Rect(420, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    quit_button_rect = pygame.Rect(20, 530, BUTTON_WIDTH, BUTTON_HEIGHT)
    close_legend_rect = pygame.Rect((600 - BUTTON_WIDTH) // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)

    show_legend = False
    running = True

    # Załaduj dźwięk kliknięcia.
    DIR = "c:/Users/jzmro/OneDrive/Dokumenty/GitHub/Gra/list-6/"
    click_sound = pygame.mixer.Sound(DIR + "assets/sounds/click_fixed.wav")

    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        # Render tytułu.
        title = font.render("Wybierz swojego awatara", True, (0, 0, 0))
        screen.blit(title, (60, 70))

        if not show_legend:
            # Przycisk "Legenda".
            legend_color = (138, 43, 226) if legend_rect.collidepoint(mouse_pos) else (0, 0, 0)
            pygame.draw.rect(screen, legend_color, legend_rect, border_radius=8)
            legend_label = small_font.render("Legenda", True, (255, 255, 255))
            screen.blit(legend_label, legend_label.get_rect(center=legend_rect.center))

            # Rysowanie avatarów.
            rects = []
            for i, (avatar, pos) in enumerate(zip(avatars, positions)):
                rect = pygame.Rect(pos[0], pos[1], 150, 150)
                rects.append(rect)

                label = label_font.render(avatar_names[i], True, (0, 0, 0))
                screen.blit(label, label.get_rect(center=(pos[0] + 75, pos[1] - 20)))

                # Podświetlenie avatara.
                if rect.collidepoint(mouse_pos) or selected_index == i:
                    pygame.draw.rect(screen, (138, 43, 226), rect, 5)

                screen.blit(avatar, pos)

            # Przycisk "Wybierz".
            is_hovered = button_rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, (138, 43, 226) if is_hovered else (0, 0, 0), button_rect, border_radius=8)
            btn_label = small_font.render("Wybierz", True, (255, 255, 255))
            screen.blit(btn_label, btn_label.get_rect(center=button_rect.center))

            # Przycisk "Zamknij".
            hovered_quit = quit_button_rect.collidepoint(mouse_pos)
            quit_color = (138, 43, 226) if hovered_quit else (0, 0, 0)
            pygame.draw.rect(screen, quit_color, quit_button_rect, border_radius=8)
            quit_label = small_font.render("Zamknij", True, (255, 255, 255))
            screen.blit(quit_label, quit_label.get_rect(center=quit_button_rect.center))

        else:
            # Widok legendy.
            overlay = pygame.Surface((600, 600))
            overlay.set_alpha(220)
            overlay.fill((240, 240, 240))
            screen.blit(overlay, (0, 0))

            legend_title = font.render("Legenda Postaci", True, (0, 0, 0))
            screen.blit(legend_title, (150, 50))

            for i, bonus_text in enumerate(avatar_bonuses):
                bonus_label = label_font.render(bonus_text, True, (0, 0, 0))
                screen.blit(bonus_label, (50, 150 + i * 50))

            mouse_on_close = close_legend_rect.collidepoint(mouse_pos)
            close_color = (138, 43, 226) if mouse_on_close else (0, 0, 0)
            pygame.draw.rect(screen, close_color, close_legend_rect, border_radius=8)
            close_label = small_font.render("Zamknij", True, (255, 255, 255))
            screen.blit(close_label, close_label.get_rect(center=close_legend_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()

                if not show_legend:
                    if quit_button_rect.collidepoint(event.pos):
                        running = False

                    for i, rect in enumerate(rects):
                        if rect.collidepoint(event.pos):
                            selected_index = i

                    if button_rect.collidepoint(event.pos) and selected_index is not None:
                        player_index = avatar_global_indices[selected_index]
                        computer_index = 1
                        config.set_selected_avatars(player_index, computer_index)
                        running = False

                    if legend_rect.collidepoint(event.pos):
                        show_legend = True

                else:
                    if close_legend_rect.collidepoint(event.pos):
                        show_legend = False
