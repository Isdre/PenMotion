# PenMotion

PenMotion to projekt napisany w języku Python, który działa jako interpreter rysunków wykonanych przez przesunięcia długopisu. Poniżej znajdziesz informacje na temat konfiguracji, dostępnych funkcji i sposobu użycia.

## Konfiguracja

1. Sklonuj repozytorium PenMotion.
2. Przejdź do folderu z projektem.
3. Wygeneruj parser za pomocą komendy:
```bash
antlr4 -Dlanguage=Python3 .\PenMotion.g4 -visitor -o PenMotion/definitions/antlr

```


## Użycie
Aby wykonać kod PenMotion w pliku, użyj poniższej komendy:
```bash
python penmotion.py [nazwa_pliku]
```
## Dostępne funkcje

- Opuszczenie i podniesienie długopisu.
- Ustawienie rozmiaru strony i długopisu.
- Ustawienie koloru długopisu.
- Przesunięcie o wektor (x, y).
- Przesunięcie na pozycję (x, y).
- Powtarzanie instrukcji (repeat).
- Wyczyszczenie ekranu.
- Funkcje bez i z argumentami.
- komentarze

## Przykładowe kody

W folderze `test_codes` znajdziesz przykładowe kody do wypróbowania.

Zapraszam do eksperymentowania z PenMotion i tworzenia własnych rysunków! 😊
