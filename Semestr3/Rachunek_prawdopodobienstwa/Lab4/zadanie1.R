#1.	Korzystając z generatora liczb pseudolosowych z odpowiedniego rozkładu w R, wylosować
#a)	5 000 realizacji z rozkładu jednostajnego na przedziale [0,1]
#b)	3 000 realizacji z rozkładu normalnego o średniej 100 oraz odchyleniu standardowym 15.
#c)	[Nowe struktury danych – obiekt] W obu przypadkach wyznaczyć estymator gęstości rozkładu za pomocą 
#i) histogramu (polecenie „hist”), ii) estymatora jądrowego (polecenie „density” – tworzy odpowiedni obiekt). 

#Dla każdego z powyższych podpunktów proszę wygenerować wykres, np. histogram.

#a
a <- runif(5000)
hist(a, main = "Histogram U(1,0)", xlab = "liczba", ylab = "Licznosc")
d1 <- density(a)
plot(d1, main = "Estymator jądrowy gęstości dla U(0,1)", xlab = "wartość", ylab = "gestosc" )


#b
b <- rnorm(3000, 100, 15)
hist(b, main = "Histogram dla nrom(100,15)", xlab = "liczba", ylab = "Licznosc")
d2<- density(b)
plot(d2, main = "Estymator jądrowy gęstościa dla norm(100,15)", xlab = "wartość", ylab = "gestosc")