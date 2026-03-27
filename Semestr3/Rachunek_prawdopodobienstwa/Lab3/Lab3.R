#zadanie 1
# n=6 p=0.5
# rozkład dwumianowy dbinom (x,size,prob)

#	Rzucono monetą 6 razy. Niech X będzie liczbą reszek. Wyznaczyć
#P(X = 5)
#P(X ≥ 3)
#P(2 ≤ X ≤ 4)
#Narysować wykres rozkładu zmiennej X (funkcja: plot, type=”h”).


z11 <- dbinom(5,6,0.5)
z12 <- 1 -  pbinom(2,6,0.5) #bo P(x>=3) = 1 - P(x<=2)
z13 <- pbinom(4,6,0.5) - pbinom(1,6,0.5) #w dyskretnych: P(a≤X≤b)=p(X≤a)-p(x≤b-1)

x<- 0:6
z14 <-plot(x, dbinom(x, 6, 0.5), type = "h",
           col = "blue",
           lwd = 2,
           main = "Rozkład dwumianowy: n=6, p=0.5",
           xlab = "x (liczba reszek)",
           ylab = "P(X = x)" )

#	Pewien salon średnio sprzedaje trzy samochody tygodniowo.
#Niech X będzie liczbą samochodów sprzedanych w ciągu 2 tygodni. 
#Zakładając, iż liczba samochodów sprzedanych przez firmę w dowolnym przedziale
#czasu ma rozkład Poissona, wyznaczyć
#P(X = 5)
#P(X ≥ 4)
#P(3 ≤ X ≤ 5)
#Narysować wykres rozkładu zmiennej X dla 0≤x≤30.

z21 <- dpois(5,6)
z22 <- 1-ppois(3,6)
z23 <- ppois(5,6) - ppois(2,6)
x<- 0:30
z24 <-plot(x, dpois(x,6), type = "h",
           col = "blue",
           lwd = 2,
           main = "Rozkład Poissona: lambda=6",
           xlab = "x - liczba samochodów ",
           ylab = "P(X = x)" )

#3. Zmienna X ma rozkład jednostajny na przedziale [4; 12]. Wyznaczyć 
#i) P(X<7)
#ii) P(5<X<11)
#iii) P(X>10)
#iv) Wyznaczyć x taki, że P(X>x)=0.6

z31 <- punif(7,4,12)
z32 <- punif(11,4,12) - punif(5,4,12) # w dyskretnych P(a<x<b) = p(x<b) - p(x<a)
z33 <- 1 - punif(10,4,12)
z34 <- qunif(0.4,4,12) #bo P(X<x) = 1 - 0.6

#	Telefony przychodzą do pewnej centrali losowo z stałą
#intensywnością 4 na minutę. Niech T będzie czasem między dwoma telefonami.
#Wyznaczyć prawdopodobieństwo tego, iż czas między telefonami jest
#większy niż 30s. 
#mniejszy niż 20s.
#między 40 a 80s.
#Wyznaczyć czas t taki, że p’stwo, iż czas między telefonami jest większy niż t wynosi 0,2. 
#Narysować wykres gęstości zmiennej T na przedziale 0≤t≤3.
#[funkcja: plot, type=”l”, wynaczyć gęstość g(t) dla t∈{0,0.01,0.02,…,2.99,3}].


#sekundy należy zamienić na minuty ponieważ labmda = 4/min
z41 <- 1- pexp(0.5,4)
z42 <- pexp(1/3,4)
z43 <- pexp(4/3,4) - pexp(2/3,4) 
z44 <- qexp(0.8,4) #bo P(T<=t) = 1 - P(T>t) = 0.8
x<- seq(0, 3, by = 0.01)
z45 <- plot(x, dexp(x,4), type = "l",
            col = "blue",
            lwd = 2,
            main = "Rozkład wykladniczy: parametr = 4/min",
            xlab = "t - czas miedzt dwoma telefonami (min) ",
            ylab = "d(t)" )

#5.	Wzrost studentów X ma rozkład normalny z wartością oczekiwaną 170cm a 
#wariancja 144cm2. Niech X będzie wzrost losowo wybranego studenta. Wyznaczyć
#i)	P(X > 180)
#ii)	P(X < 165)
#iii)	P(155 < X < 190)
#iv)	Wzrost k, taki że 10% osób jest wyższe niż k.

#E(X) = 170 Var(X) = 144 -> o = 12 

z51 <- 1-pnorm(180, 170,12)
z52 <- pnorm(165, 170, 12)
z53 <- pnorm(190, 170,12) - pnorm(155, 170, 12)
z54 <- qnorm(0.9, 170, 12)

#	Rzucono kostką 180 razy. Niech X będzie liczbą jedynek. Wyznaczyć
#P(X = 27)
#P(X ≥ 32)
#P(X < 29)
#P(25 ≤ X ≤ 33)

z61 <- dbinom(27, 180, 1/6)
z62 <- 1 - pbinom(31, 180, 1/6)
z63 <- pbinom(28, 180, 1/6)
z64 <- pbinom(33, 180, 1/6) - pbinom(24, 180, 1/6)



