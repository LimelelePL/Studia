# Znane problemy i ograniczenia

## has_proper_name — false positives / false negatives

| Przypadek | Przykład | Wynik | Problem |
|-----------|----------|-------|---------|
| Pauza dialogowa | `powiedział — Chodź` | False positive | `—` non-alpha → `Chodź` wykryte jako nazwa własna |
| Polskie cudzysłowy | `„Gazeta Wyborcza"` | False positive | `„` non-alpha → `Gazeta` wykryte jako nazwa własna |
| Prefiks + nazwa własna | `anty-NATO` | False negative | Traktowane jako jedno słowo zaczynające się małą literą |

## read_sentece — niepoprawne dzielenie zdań

Funkcja traktuje każde `.` `!` `?` jako koniec zdania, co psuje:

| Przypadek | Przykład | Efekt |
|-----------|----------|-------|
| Skróty z kropką | `m.in.`, `tj.`, `np.`, `dr.` | Zdanie splitowane w środku skrótu |
| Inicjały | `J.R.R. Tolkien` | Każda kropka kończy zdanie |

## Inne znane ograniczenia

- `skip_word` z myślnikiem/apostrofem: `"anty-NATO"` traktowane jako jedno słowo (małe `a`)
- Liczby z myślnikiem `19-letni`: cyfra zatrzymuje `skip_word`, `letni` traktowane jako osobne słowo (małą literą — zachowanie poprawne)
- `Windows-95`: myślnik przed cyfrą zatrzymuje `skip_word` → `Windows` jedno słowo ✓
