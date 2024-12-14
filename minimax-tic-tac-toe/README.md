# Implementacja i Analiza Algorytmu Minimax z Optymalizacją Alfa-Beta dla gry _Kółko i Krzyżyk_

To repozytorium zawiera implementację algorytmu minimax na grze kółko i krzyżyk.

## Opis Działania Algorytmu

Algorytm minimax jest rekurencyjnym algorytmem przeszukiwania drzewa gry, który ocenia ruchy dostępne w danej grze z perspektywy maksymalizującego i minimalizującego gracza. W kontekście gry kółko i krzyżyk, maksymalizującym graczem jest AI, a minimalizującym użytkownik.

Optymalizacja alfa-beta dodatkowo przycina gałęzie drzewa, które nie muszą być eksplorowane, ponieważ nie wpłyną na ostateczną decyzję. Alfa reprezentuje minimalną ocenę, którą maksymalizujący gracz jest zapewniony, natomiast beta reprezentuje maksymalną ocenę, którą minimalizujący gracz jest zapewniony. Zapewnia to szybsze przeszukiwanie drzewa możliwych rozwiązań, jednocześnie zmniejszając ilość potrzebnych obliczeń.

## Rozpoczęcie Rozgrywki

W przypadku rozpoczęcia rozgrywki przez komputer wybiera on jeden z narożników, co jest optymalnym rozpoczynającym ruchem. Każdy kolejny ruch komputera jest generowany przez algorytm minimax.

## Przykład Działania Algorytmu

1. Dla każdego możliwego ruchu, algorytm rekurencyjnie ocenia możliwe wyniki gry, zakładając optymalne ruchy przeciwnika.
2. Zastosowanie optymalizacji alfa-beta pozwala na pominięcie niektórych gałęzi drzewa, które nie wpłyną na ostateczną decyzję, skracając czas potrzebny na podjęcie decyzji.
3. Algorytm kontynuuje, aż znajdzie ruch, który maksymalizuje szanse na wygraną AI, biorąc pod uwagę możliwe ruchy przeciwnika.

## Analiza Wydajności

Do analizy wydajności algorytmu przeprowadziłem serię eksperymentów, mierząc czas potrzebny na podjęcie decyzji przez AI w różnych stanach gry, zarówno z implementacją optymalizacji alfa-beta, jak i bez niej. Wziąłem pod uwagę 2 gry, pierwszą rozpoczynałem od lewego górnego rogu, natomiast drugą od prawego dolnego.

Poniższe wykresy przedstawiają długość wykonania algorytmu minimax (po lewej) i alpha-beta (po prawej), na podstawie aktualnego stanu planszy (im większa wartość stanu tym późniejszy etap gry). \
**Pierwsza gra**\
![Wykres minimax 1](/plots/minimax.png) ![Wykres alpha-beta 1](/plots/alpha_beta.png)\
**Druga gra**\
![Wykres minimax 2](/plots/minimax2.png) ![Wykres aphta-beta 2](/plots/alpha_beta2.png)

Analizując przebieg pierwszej gry można zauważyć, że algorytm minimax bez optymalizacji alpha-beta poradził sobię szybciej w każdym możliwym stanie. Natomiast podczas drugiej gry są momenty w których wygrywa ten z implementacją alpha-beta. Warto zastanowić się dlaczego tak się dzieje. W pierwszej grze nie podczas przeszukiwania możliwych stanów, algorytm natkął się na te nadające się do odrzucenia dopiero po przeanalizowaniu gorszych rozwiązań co doprowadziło do nieodrzucenia gorszej ścieżki, tym samym zwiększając ilość wykonanych operacji. Jednak w drugiej grze w niektórych stanach bardziej optymalne rozwiązania zostały znalezione pierwsze powodując odrzucenie gorszych.

Warto też zwrócić uwagę na zwiększenie czasu działania, dla każdego stanu w drugiej grze, w przypadku algorytmu minimax bez optymalizacji alpha-beta. W przypadku algorytmu z optymalizacją można zauważyć poprawę czasową w drugiej grze w niektórych stanach. Oznacza to, że algorytm z optymalizacją alpha-beta pozwala znacząco zredukować czas obliczeń w korzystnym przypadku kolejności rozpatrywanych stanów. 

## Podsumowanie i Wnioski

Implementacja algorytmu minimax z optymalizacją alfa-beta w grze kółko i krzyżyk pokazała, że jest to skuteczna metoda do sterowania ruchami AI. Optymalizacja alfa-beta znacząco poprawia wydajność algorytmu, redukując czas potrzebny na analizę ruchów, co jest kluczowe w grach o większej złożoności.

Wnioski z implementacji i testów są następujące:
- Algorytm minimax efektywnie ocenia najlepsze ruchy w grze kółko i krzyżyk, ale jego wydajność znacznie spada wraz ze wzrostem liczby możliwych ruchów.
- Optymalizacja alfa-beta jest niezbędna do utrzymania rozsądnego czasu odpowiedzi AI, szczególnie w początkowych etapach gry, gdzie możliwych ruchów jest najwięcej.
- Implementacja algorytmu wymaga dokładnego przemyślenia logiki gry i możliwych scenariuszy, aby zapewnić optymalne i szybkie działanie AI.

W rezultacie, zastosowanie algorytmu minimax z optymalizacją alfa-beta w grach strategicznych, takich jak kółko i krzyżyk, może znacząco poprawić jakość i szybkość decyzji podejmowanych przez sztuczną inteligencję, co czyni tę metodę atrakcyjną dla twórców gier i systemów decyzyjnych.