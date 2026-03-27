
#ZADANIE 1

#H0: kostka jest symetryczna
#H1: kostka nie jest symetryczna

#a
obserwowane_wyniki <- c(171, 200, 168, 213, 226, 222)
n <- sum(obserwowane_wyniki)
oczekiwane_wyniki <- rep(1/6 * n, 6)

ocz_tab <- matrix(oczekiwane_wyniki, ncol = 6)
colnames(ocz_tab) <- c(1,2,3,4,5,6)
rownames(ocz_tab) <- "frekwencja : "
ocz_tab

#b
t <- sum ((oczekiwane_wyniki - obserwowane_wyniki)^2 / oczekiwane_wyniki)
t

#c
p_value <- 1 - pchisq(t, df = 5)
p_value

#d 
# ponieważ p_value jest mniejsze od poziomu istotności 5% mamy podstawy twierdzić, że kostka nie jest symetryczna

#e
chisq.test(obserwowane_wyniki, p = rep (1/6, 6))

#ZADANIE 2

#a
realizacje <- rexp(1000)

#b

#H0: próba pochodzi z  N(1,1)
#H1: próba nie pochodzi z N(1,1)

ks.test(realizacje, "pnorm")
# ponieważ p value < 0.05 mamy podstawy do odrzucenia H0

#H0: próba pochodzi z Exp(1)
#H1: próba nie pochodzi z Ecp(1)

ks.test(realizacje, "pexp")
# ponieważ p value > 0.05 nie mamy podstaw do udrzucenia H0

#c

realizacje <- rgamma(1000, shape = 100, scale = 1)

#d

#H0: próba pochodzi z  N(100,10)
#H1: próba nie pochodzi z N(1,1)

ks.test(x, "pnorm", mean = 100, sd = 10)
# ponieważ p value < 0.05 mamy podstawy do odrzucenia H0

#H0: próba pochodzi z  gamma(100,1)
#H1: próba nie pochodzi z gamma(100,1)

ks.test(x, "pgamma", shape = 100, scale = 1)
# ponieważ p value < 0.05 mamy podstawy do odrzucenia H0

#zad 3
mieszkania <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/lab7/mieszkania.csv", sep = ';')

#a
#H0: ceny za metr kwadratowy mieszkania mają rozkład normalny
#H1: ceny za metr kwadratowy mieszkania nie mają rozkładu normalnego

cena_za_m2 <- mieszkania $ Cena / mieszkania $ Metraz
shapiro.test(cena_za_m2)

#ponieważ p value < 0,05 mamy podstawy do odrzucenia hipotezy zerowej

#b

#H0: metraz mieszkan ma rozkład normalny
#H0: metraz mieszkan nie ma rozkładu normalnego

metraz <- mieszkania $ Metraz
shapiro.test(metraz)

#ponieważ p value < 0,05 mamy podstawy do odrzucenia hipotezy zerowej

#ZADANIE 4

#a
cena_mieszkania <- mieszkania$Cena
reg <- lm(cena_mieszkania ~ metraz)
summary(reg)

#b
plot(
  metraz, cena_mieszkania,
  main = "Wykres rozrzutu ceny za m2 względem metrazu",
  xlab = "cena mieszkania", ylab = "metraż",
  pch = 20
)

abline(reg, col = "red")

b0 <- 7510.254
b1 <- -23.704

cat("rownanie y = ", b1, " * metraż + ", b0 )

#c 
est_metraz <- b1 * metraz + b0 
reszty <- cena_mieszkania - est_metraz

shapiro.test(reszty)

#d

metraz_wartosc <- 80
cena_mieszkania_80 <- b1 * metraz_wartosc + b0
cena_mieszkania_80

#ZADANIE 5

bakteria <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/lab7/bakteria.csv", sep = ';', dec = ",")

#a
masa_bakterii <- bakteria$masa
czas <- bakteria$czas


plot(czas, masa_bakterii,
     main = "Wykres masy bakterii od czasu",
     xlab = "czas", ylab = "masa bakterii"
     ,pch = 20)

#b

reg <- lm(log(masa_bakterii) ~`czas)

