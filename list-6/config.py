import pygame
import json
import os

# Lista ścieżek do plików z obrazami avatarów.
avatars = [
    "assets/avatars/avatar1.png",
    "assets/avatars/avatar2.png",
    "assets/avatars/avatar3.png",
    "assets/avatars/avatar4.png"
]

# Efekty specjalne przypisane do każdego avatara (index odpowiada awatarowi).
avatar_effects_list = [
    {"extra_lives": 3, "points_multiplier": 1, "points_on_draw": 0},  # avatar1
    {"extra_lives": 0, "points_multiplier": 2, "points_on_draw": 0},  # avatar2
    {"extra_lives": 0, "points_multiplier": 1, "points_on_draw": 2},  # avatar3
    {"extra_lives": 0, "points_multiplier": 2, "points_on_draw": 0},  # avatar4
]

# Aktualnie wybrane avatary: (gracz, komputer) — indeksy z listy avatars.
_selected_avatar_indices = (0, 1)

# Aktualne efekty dla awatara gracza (domyślnie efekt pierwszego avatara).
_current_avatar_effects = avatar_effects_list[_selected_avatar_indices[0]]

# Zarządzanie avatarami.
def set_selected_avatars(player_index, computer_index):
    global _selected_avatar_indices
    _selected_avatar_indices = (player_index, computer_index)
    set_avatar_effects_by_index(player_index)

def get_selected_avatars():
    player_index, computer_index = _selected_avatar_indices
    player_avatar = pygame.image.load(avatars[player_index])
    computer_avatar = pygame.image.load(avatars[computer_index])
    return player_avatar, computer_avatar

def set_avatar_effects_by_index(index):
    global _current_avatar_effects
    if 0 <= index < len(avatar_effects_list):
        _current_avatar_effects = avatar_effects_list[index]
    else:
        _current_avatar_effects = {}

def get_avatar_effects():
    return _current_avatar_effects

# Ścieżka do pliku z wynikami
SCORE_FILE = os.path.join(os.getcwd(), "scores.json")

def ensure_score_file_exists():
    """
    Tworzy pusty plik scores.json, jeśli jeszcze nie istnieje.
    """
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_scores():
    """
    Wczytuje listę wyników z pliku JSON. Obsługuje błędy uprawnień i błędny format.
    """
    ensure_score_file_exists()
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (PermissionError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania wyników: {e}")
        return []

def save_scores(scores):
    """
    Zapisuje listę wyników do pliku JSON.
    """
    try:
        with open(SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except PermissionError as e:
        print(f"Błąd zapisu wyników: {e}")

def add_score(player_name, score):
    """
    Dodaje lub aktualizuje wynik gracza.
    """
    scores = load_scores()
    found = False
    for entry in scores:
        if entry["name"] == player_name:
            if score > entry["score"]:
                entry["score"] = score
            found = True
            break
    if not found:
        scores.append({"name": player_name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    save_scores(scores)

def get_top_scores(limit=10):
    """
    Pobiera najlepsze wyniki (domyślnie top 10).
    """
    return load_scores()[:limit]




