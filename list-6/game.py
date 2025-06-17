import pygame
import random
import config

pygame.init()
pygame.mixer.init()
player_move_sound = pygame.mixer.Sound("assets/sounds/click_fixed.wav")
computer_move_sound = pygame.mixer.Sound("assets/sounds/mutant_frog-2.wav")

SCREEN_SIZE = 600
GRID_SIZE = 130
BOARD_SIZE = GRID_SIZE * 3  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LINE_COLOR = (10, 10, 10)

# Wczytanie i skalowanie tła.
background = pygame.image.load("assets/images/background2.png").convert()
background = pygame.transform.scale(background, (SCREEN_SIZE, SCREEN_SIZE))

def load_font(size):
    """Ładuje font o podanym rozmiarze."""
    return pygame.font.Font("assets/fonts/PirataOne-Regular.ttf", size)

font = load_font(30)
small_font = pygame.font.Font("assets/fonts/EagleLake-Regular.ttf", 18)
message_font = pygame.font.Font("assets/fonts/NewRocker-Regular.ttf", 26)

player_lives = 3
player_score = 0
avatar_effects = {}

# Reprezentacja planszy - 3x3 siatka, na początku pusta (None).
grid = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"  # Gracz zawsze X, komputer O.
game_over = False

round_end_time = None
waiting_for_computer = False
computer_move_time = None

# Komunikaty wyświetlane po zakończeniu rundy.
player_win_msgs = ["To tylko kwestia czasu!", "Byłem blisko!", "Zaraz ci pokażę!"]
computer_win_msgs = ["Tylko na tyle Cię stać?", "Nigdy mnie nie pokonasz.", "Hahahaha!"]

def load_avatars():
    """
    Wczytuje i skaluje awatary gracza i komputera.
    
    Returns:
        (player_img, computer_img): dwie powierzchnie pygame z awatarami.
    """
    player_avatar, computer_avatar = config.get_selected_avatars()
    player_img = pygame.transform.smoothscale(player_avatar, (80, 80))
    computer_img = pygame.transform.smoothscale(computer_avatar, (80, 80))
    return player_img, computer_img

player_img, computer_img = load_avatars()

def draw_board(screen):
    """
    Rysuje planszę, linie, znaki graczy oraz informacje o punktach i życiu.
    
    Args:
        screen (pygame.Surface): powierzchnia, na której rysujemy.
    """
    screen.blit(background, (0, 0))
    # Linie planszy.
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * GRID_SIZE), (BOARD_SIZE, i * GRID_SIZE), 5)
        pygame.draw.line(screen, LINE_COLOR, (i * GRID_SIZE, 0), (i * GRID_SIZE, BOARD_SIZE), 5)

    # Rysowanie znaków X i O.
    for row in range(3):
        for col in range(3):
            mark = grid[row][col]
            if mark:
                x = col * GRID_SIZE + (GRID_SIZE - 80) // 2
                y = row * GRID_SIZE + (GRID_SIZE - 80) // 2
                if mark == "X":
                    screen.blit(player_img, (x, y))
                else:
                    screen.blit(computer_img, (x, y))

    # Informacje o życiu i punktach po prawej stronie planszy.
    lives_text = small_font.render(f"Życia: {player_lives}", True, RED)
    score_text = small_font.render(f"Punkty: {player_score}", True, BLACK)
    screen.blit(lives_text, (BOARD_SIZE + 10, 50))
    screen.blit(score_text, (BOARD_SIZE + 10, 100))

def check_winner():
    """
    Sprawdza, czy jest zwycięzca na planszy.
    
    Returns:
        str lub None: "X" lub "O" jeśli jest zwycięzca, None jeśli brak.
    """
    # Sprawdzenie wierszy.
    for row in grid:
        if row[0] and row[0] == row[1] == row[2]:
            return row[0]
    # Sprawdzenie kolumn.
    for col in range(3):
        if grid[0][col] and grid[0][col] == grid[1][col] == grid[2][col]:
            return grid[0][col]
    # Sprawdzenie przekątnych.
    if grid[0][0] and grid[0][0] == grid[1][1] == grid[2][2]:
        return grid[0][0]
    if grid[0][2] and grid[0][2] == grid[1][1] == grid[2][0]:
        return grid[0][2]
    return None

def is_draw():
    """Sprawdza, czy nastąpił remis (brak pustych pól)."""
    return all(cell is not None for row in grid for cell in row)

def reset_board(starting_player):
    """
    Resetuje planszę i ustawia aktualnego gracza.

    Args:
        starting_player (str): "X" lub "O" kto zaczyna nową rundę.
    """
    global grid, current_player, game_over, waiting_for_computer, computer_move_time, round_end_time
    grid = [[None for _ in range(3)] for _ in range(3)]
    current_player = starting_player
    game_over = False
    round_end_time = None

    if current_player == "O":
        waiting_for_computer = True
        computer_move_time = pygame.time.get_ticks() + 1500  
    else:
        waiting_for_computer = False
        computer_move_time = None

def get_computer_move():
    """
    Prosta AI: komputer stara się zająć środek, potem rogi, potem dowolne puste pole.
    
    Returns:
        tuple(int, int) lub None: współrzędne ruchu lub None jeśli brak ruchu.
    """
    if grid[1][1] is None:
        return (1, 1)
    corners = [(0,0), (0,2), (2,0), (2,2)]
    free_corners = [pos for pos in corners if grid[pos[0]][pos[1]] is None]
    if free_corners:
        return random.choice(free_corners)
    empty_cells = [(r, c) for r in range(3) for c in range(3) if grid[r][c] is None]
    if empty_cells:
        return random.choice(empty_cells)
    return None

def render_multiline(text, font, color, max_width):
    """
    Renderuje wielowierszowy tekst dzieląc go na linie dopasowane do max_width.
    
    Args:
        text (str): tekst do podziału
        font (pygame.font.Font): font do pomiaru szerokości
        color (tuple): kolor tekstu (nieużywany tutaj, ale może być przydatny)
        max_width (int): maksymalna szerokość linii
    
    Returns:
        list[str]: lista linii tekstu
    """
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

def start_game(screen, player_name):
    """
    Główna pętla gry - obsługuje rozgrywkę, rysuje ekran, obsługuje ruchy gracza i komputera,
    aktualizuje punkty i życie.

    Args:
        screen (pygame.Surface): powierzchnia do rysowania gry
        player_name (str): imię gracza do zapisu wyników
    """
    global current_player, game_over, player_img, computer_img
    global player_lives, player_score, round_end_time
    global waiting_for_computer, computer_move_time
    global avatar_effects

    # Atrybuty statyczne funkcji do pamiętania stanu pomiędzy wywołaniami.
    if not hasattr(start_game, "next_start"):
        start_game.next_start = "X"
    if not hasattr(start_game, "lives_deducted"):
        start_game.lives_deducted = False

    avatar_effects = config.get_avatar_effects() or {}

    if not hasattr(start_game, "avatar_lives_added"):
        extra_lives = avatar_effects.get("extra_lives", 0)
        player_lives += extra_lives
        start_game.avatar_lives_added = True

    player_img, computer_img = load_avatars()
    reset_board(start_game.next_start)

    end_message = None
    clock = pygame.time.Clock()

    while True:
        draw_board(screen)

        if game_over:
            winner = check_winner()
            if winner == "X":
                if not start_game.lives_deducted:
                    multiplier = avatar_effects.get("points_multiplier", 1)
                    points_to_add = 1 * multiplier
                    player_score += points_to_add
                    config.add_score(player_name, player_score)
                    start_game.lives_deducted = True
                if end_message is None:
                    end_message = random.choice(player_win_msgs)
            elif winner == "O":
                if not start_game.lives_deducted and player_lives > 0:
                    player_lives -= 1
                    start_game.lives_deducted = True
                    if player_lives <= 0:
                        config.add_score(player_name, player_score)
                if end_message is None:
                    end_message = random.choice(computer_win_msgs)
            else:
                # Remis.
                if not start_game.lives_deducted:
                    points_on_draw = avatar_effects.get("points_on_draw", 0)
                    player_score += points_on_draw
                    if points_on_draw > 0:
                        config.add_score(player_name, player_score)
                    start_game.lives_deducted = True
                if end_message is None:
                    end_message = "Remis!"

            # Wyświetlanie komunikatu na ekranie.
            if end_message:
                if end_message in player_win_msgs + computer_win_msgs:
                    right_x = BOARD_SIZE + 10
                    right_y = BOARD_SIZE - 100
                    lines = render_multiline(end_message, message_font, BLACK, 180)
                    for i, line in enumerate(lines):
                        label = message_font.render(line.strip(), True, BLACK)
                        screen.blit(label, (right_x, right_y + i * message_font.get_linesize()))
                else:
                    label = message_font.render(end_message, True, BLACK)
                    screen.blit(label, (10, BOARD_SIZE + 20))

                label2 = small_font.render("Naciśnij R, by zrestartować grę.", True, BLACK)
                screen.blit(label2, (10, BOARD_SIZE + 60))

            if player_lives <= 0:
                end_label = small_font.render("Koniec gry - brak żyć!", True, RED)
                screen.blit(end_label, (50, 550))

            # Pokazanie miejsca gracza w rankingu.
            top_scores = config.get_top_scores()
            for idx, entry in enumerate(top_scores):
                if entry["name"] == player_name:
                    place = idx + 1
                    rank_label = small_font.render(f"Twoje miejsce w rankingu: {place}", True, (0, 128, 0))
                    screen.blit(rank_label, (10, BOARD_SIZE + 100))
                    break

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Restart gry po naciśnięciu R.
                if event.key == pygame.K_r:
                    extra_lives = avatar_effects.get("extra_lives", 0)
                    player_lives = 3 + extra_lives
                    player_score = 0
                    start_game.lives_deducted = False
                    reset_board(start_game.next_start)
                    end_message = None
                    game_over = False
                    round_end_time = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and current_player == "X" and player_lives > 0:
                    x, y = event.pos
                    if x < BOARD_SIZE and y < BOARD_SIZE:
                        row = y // GRID_SIZE
                        col = x // GRID_SIZE
                        if grid[row][col] is None:
                            grid[row][col] = current_player
                            player_move_sound.play()
                            winner = check_winner()
                            if winner or is_draw():
                                game_over = True
                                round_end_time = pygame.time.get_ticks() + 3500
                            else:
                                current_player = "O"
                                waiting_for_computer = True
                                computer_move_time = pygame.time.get_ticks() + 1500

        # Ruch komputera po upływie czasu.
        if waiting_for_computer and not game_over:
            now = pygame.time.get_ticks()
            if now >= computer_move_time:
                move = get_computer_move()
                if move:
                    r, c = move
                    grid[r][c] = "O"
                    computer_move_sound.play() 
                winner = check_winner()
                if winner or is_draw():
                    game_over = True
                    round_end_time = pygame.time.get_ticks() + 3500
                else:
                    current_player = "X"
                waiting_for_computer = False

        # Automatyczne rozpoczęcie kolejnej rundy, jeśli gra nie skończona.
        if game_over and round_end_time and pygame.time.get_ticks() >= round_end_time:
            if player_lives > 0:
                # Zmiana gracza rozpoczynającego rundę.
                start_game.next_start = "O" if start_game.next_start == "X" else "X"
                reset_board(start_game.next_start)
                start_game.lives_deducted = False
                end_message = None
                game_over = False
                round_end_time = None
                waiting_for_computer = current_player == "O"
                if waiting_for_computer:
                    computer_move_time = pygame.time.get_ticks() + 1500
                else:
                    computer_move_time = None
            else:
                round_end_time = None 

        clock.tick(30)
