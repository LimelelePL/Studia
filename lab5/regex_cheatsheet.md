Python Regex Cheatsheet

1. Metaznaki (Meta Characters)
. – Dowolny znak (z wyjątkiem nowej linii).
^ – Początek ciągu znaków (np. ^Hello).
$ – Koniec ciągu znaków (np. world$).
* – Zero lub więcej wystąpień.
+ – Jedno lub więcej wystąpień.
? – Zero lub jedno wystąpienie (oznacza, że znak jest opcjonalny).
{n} – Dokładnie n wystąpień.
{min, max} – Zakres wystąpień (od min do max).
| – Alternatywa (operator "lub", np. mr|mrs).
() – Grupowanie znaków.
\ – Znak ucieczki (używany do wyszukiwania znaków specjalnych, np. \. szuka kropki).

# 2. Specjalne Sekwencje (Special Sequences)
\d – Dowolna cyfra (0-9).
\D – Dowolny znak niebędący cyfrą.
\s – Dowolny "biały znak" (spacja, tabulacja, nowa linia).
\S – Dowolny znak niebędący białym znakiem.
\w – Dowolny znak alfanumeryczny (litery, cyfry, podkreślnik _).
\W – Dowolny znak niebędący znakiem alfanumerycznym.
\b – Granica słowa (początek lub koniec słowa).

3. Zbiory (Sets)
[abc] – Dowolny z wymienionych znaków (a, b lub c).
[a-z] – Dowolna mała litera z zakresu a-z.
[A-Z] – Dowolna wielka litera z zakresu A-Z.
[0-9] – Dowolna cyfra (odpowiednik \d).
[^abc] – Dowolny znak, który nie jest a, b ani c.

4. Najważniejsze metody modułu re
# Kompilacja wzorca (zalecane dla czytelności i wydajności)
pattern = re.compile(r'ABC')
# finditer() - zwraca iterator z obiektami match (najlepsza do pętli)
matches = pattern.finditer(test_string)
# findall() - zwraca listę dopasowanych stringów
strings = pattern.findall(test_string)
# search() - szuka pierwszego dopasowania w całym tekście
match = pattern.search(test_string)
# match() - sprawdza dopasowanie tylko na samym początku tekstu
match = pattern.match(test_string)
# sub() - zamienia dopasowania na inny tekst
new_string = pattern.sub('planet', test_string)

5. Flagi kompilacji (Compilation Flags)
re.I lub re.IGNORECASE – ignorowanie wielkości liter.
re.M lub re.MULTILINE – tryb wielowierszowy (zmienia zachowanie ^ i $).
re.S lub re.DOTALL – sprawia, że kropka . dopasowuje też nową linię.