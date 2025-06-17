import pygame

click_sound = pygame.mixer.Sound("assets/sounds/click_fixed.wav") 

def show_about(screen):
    font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 20)
    diff_font = pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", 28)

    background = pygame.image.load("assets/images/background2.png").convert()
    background = pygame.transform.scale(background, screen.get_size())

    # Dane.
    lines = [
        "O AUTORZE:",
        "",
        "Gra stworzona przez:",
        "Julia Mrozińska",
        "Rok: 2025",
        "",
        "Gra oparta na klasycznym",
        "kółko i krzyżyk z awatarami.",
        "Wykorzystano bibliotekę Pygame.",
    ]

    # Przycisk "Zamknij".
    button_width, button_height = 160, 45
    button_x = 30
    screen_width, screen_height = screen.get_size()
    button_y = screen_height - button_height - 30
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    small_font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 20)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        for i, line in enumerate(lines):
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (40, 50 + i * 40))

        is_hovered = button_rect.collidepoint(mouse_pos)
        button_color = (180, 0, 255) if is_hovered else (0, 0, 0)

        pygame.draw.rect(screen, button_color, button_rect, border_radius=6)
        button_text = diff_font.render("Zamknij", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                click_sound.play()
                running = False

