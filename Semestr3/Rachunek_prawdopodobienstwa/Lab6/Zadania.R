#---------------------------zadanie 1-----------------------------------------------

#AAAAAAAAAAAA

#H0: skończenie studiów nie zależy od płci : p1 = p2
#H1: skończenie studiów zależy od płci : p1 != p2

# liczebnosc kazdej z prób
n_k = 520
n_m = 480

#proporcja łączona kobiet i mezczyzn, ktorzy ukończyła studia
p_hat = (220 + 165) / (n_k + n_m)
p_k = 220/520
p_m = 165/480

#błąd standardowy
SE_pooled = sqrt(p_hat * (1 - p_hat) * (1/n_k + 1/n_m))

#statystyka testowa
t = ( p_k - p_m) / SE_pooled

#poziom istotności
a = 0.05;

#wartość p value
p_value = 2*(1 - pnorm(abs(t)))
p_value

#Na poziomie istotności 5% nie ma podstaw do odrzucenia hipotezy zerowej.

#za pomocą prop.test
prop.test(c(220,165), c(n_k, n_m), correct = FALSE)

#BBBBBBBBBBBBBB

tablica = matrix(c(300, 220, 315, 165), nrow = 2, byrow = TRUE)

rownames(tablica) = c("Kobiety", "Mężczyźni")
colnames(tablica) = c("0", "1 ")

tablica

#CCCCCCCCCCCCCC

chisq.test(tablica)
fisher.test(tablica)

#DDDDDDDDDDDDD

#sredni wzrost kobiet i mezcyzn i wariancje
h_k = 166
h_m = 174
var_k = 100
var_m = 121

#H0 : średni wzrost nie zależy od płci : h_m - h_k = 0
#H1 : średni wzrost zależy od płci :  h_m - h_k != 0

#błąd standardow
SE_height = sqrt(var_k/n_k + var_m/n_m)

#statystyka testowa
z = (h_m - h_k) / SE_height

#p value
p_value = 2 * (1-pnorm(abs(z)))
p_value

#ponirważ p value << 0,05 mamy mocne dowody na to ze hipoteza zerowa jest nieprawdziwa

#------------------------------------zadanie 2--------------------------------------
waga <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/Lab6/waga1.csv", sep = ';')

kobiety = waga $ plec == 1
mezczyzni = waga $ plec == 0

n_k = sum(kobiety)
n_m = sum(mezczyzni)
n = n_k + n_m

waga_kobiet_przed = waga$Waga_przed[kobiety]
waga_kobiet_po = waga$Waga_po[kobiety]
waga_mezyzn_przed =waga $ Waga_przed [mezczyzni]
waga_mezczyzn_po = waga $ Waga_po [mezczyzni]

waga_przed = waga$Waga_przed
waga_po = waga $ Waga_po

# H0 : studencji srednio przytyli w trakcie studiów o 2kg :  waga przed - waga po = 2kg
# H1 : studencji nie przytyli srednio w trakcie studiów o 2kg: waga przed - waga po != 2kg

t.test(waga_po-waga_przed ,mu = 2)

#ponieważ p-value < 0.05 odrzucamy hipoteze zerowa

#------------------------------- zadanie 3 ---------------------------------------------

#H0: proporcja kobiet wazacych wiecej niz 70 kg po studiach nie rozni sie od proporcji mezczyzn wazacych wiecej niz 70kg: p_m = p_k
#H1: proporcja kobiet wazaych wiecej niz 70kg po studiach rozni sie od proporcji mezcyzn wazacych wiecej niz 70kg: p_m != p_k

n_k_m70 = sum(waga_kobiet_po > 70)
n_k_l70 = n_k - n_k_m70
n_m_m70 = sum(waga_mezczyzn_po > 70)
n_m_l70 = n_m - n_m_m70

# 1 wazy wiecej ni 70kg, 0 nie wazy wiecej niz 70kg
tablica = matrix(c(n_k_l70,n_k_m70 ,n_m_l70 ,n_m_m70), nrow = 2, byrow = TRUE)

rownames(tablica) = c("Kobiety", "Mężczyźni")
colnames(tablica) = c("0", "1 ")

chisq.test(tablica)

#Na poziomie istotności 5% odrzucamy hipotezę zerową i stwierdzamy, że proporcja osób ważących 
#więcej niż 70 kg po studiach różni się istotnie statystycznie między kobietami i mężczyznami.

#----------------------------------zadanie 4---------------------------------------------
#H0: mezczyzni sa srednio wyzsci o 5cm niz kobiety : h_m - h_k = 5
#H1: mezczyzni nie sa srednio wyzsci o 5cm od kobiet : h_m h_k != 5

h_m = waga $ Wzrost [mezczyzni]
h_k = waga $ Wzrost [kobiety]

t.test(h_m,h_k, paired = FALSE, mu =  5)

#Na poziomie istotnosci 5% odrzucamy hipoteze zerową i swierdzamy, że 
# mężczyźni nie są srednio wyzsci o 5cm od kobiet

#--------------------------------------zadanie 5----------------------------------------
# H0: proporcja studentów tych co nie przybrali na wadze do tych co przybrali na wadze to 80% : p = 0.8
# H1: proporcja wagi studentów przed studiami i po studiach rozni sie od zera : p!= 0.8

#obliczmy przyrost wagi
przyrost = waga$Waga_po - waga$Waga_przed

przytyl = sum(przyrost > 0)
n = length(przyrost)

prop.test(przytyl,n, p = 0.8)

#na poziomie istotnosci 5% nie odrzucamy hipotezy zerowej i stwierdzamy, że
# statystycznie 80 procent studentow przybalo po studiach

#-------------------------------------zadanie 6------------------------------------
# H0: średni przyrost masy ciała studiujących mężczyzn wynosi 4 kg
# H1: średni przyrost masy ciała studiujących mężczyzn jest różny od 4 kg


t.test(waga$Waga_po[mezczyzni] - waga $ Waga_przed [mezczyzni], mu = 4)

#Na poziomie istotności 5% odrzucamy hipotezę zerową i stwierdzamy, że średni przyrost 
#masy ciała studiujących mężczyzn różni się istotnie statystycznie od 4 kg.


