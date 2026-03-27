#2.	a) i) Zasymulować 600 rzutów kostką (odpowiednio przekształcić realizacje z rozkładu jednostajnego na [0,1]). 
#ii)	Wyznaczyć średni wynik oraz wariancję z próby [porównać z wartością oczekiwaną 3,5 oraz wariancją 35/12]. 
#iii)	Wyznaczyć rozkład częstości dla tych wyników, polecenie - table [porównać z dyskretnym rozkładem jednostajnym]. 
#iv)	Przekształcić tablicę w ramkę danych za pomocą polecenia „as.data.frame”. Wyświetlić tę ramkę oraz wyznaczyć wariancję tych częstości.
#b)	Zasymulować 600 rzutów kostką za pomocą procedury wyboru elementu ze zbioru z zwracaniem (polecenie „sample”). 

#a
x <- ceiling(6 * runif(600))

m <- mean(x)
v <- var(x)

freq <- table(x)

frame <- as.data.frame(freq)
v_freq <- var(frame$Freq)


#b
x <- sample(1:6, 600, replace = TRUE)