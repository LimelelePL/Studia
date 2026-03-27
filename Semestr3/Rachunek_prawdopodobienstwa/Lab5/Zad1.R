#1.	Średni wskaźnik inteligencji (IQ) dla próby 100 studentów wynosi 109. 
#Wariancja z próby wynosi 225. Spośród tych studentów, 30 ma IQ wyższy niż 115..

var <- 225
s <- sqrt(225)
n <- 100

#a)	Przetestować hipotezę, że 35% wszystkich studentów ma IQ wyższy niż 115
#i) za pomocą testu Z, ii) za pomocą polecenia prop.test

# HIPOTEZY
# H0: p0 = 0.35
# H1: p0 != 0.35

# proporcja z próby
p_hat <- 30 / 100

#maksymalnw dopuszczalne prawdopodobienstwo otrzymania błedu
alpha_max <- 0.05

#wartosc proporcji zalozona w h0
p0 <- 0.35 

#bład standdardowy przy zalozeniu ze h0 jest prawdziwa
s_e_p <- sqrt ((p0*(1-0))/n )

# relaizacja statystyki testowej
z <- abs((p_hat - p0) / s_e_p) 

#prawdopodobienstwo otrzymania takiego wyniku jak otrzymany lub bardziej skrajnego
#zakladajac ze h0 jest prawdziwa
p_value <- 2 * (1 - pnorm(z)) 

#czy hipoteza falszywa
p_value < alpha_max

prop.test(x = 30, n = 100, p = 0.35, correct = FALSE, conf.level = 0.95)

# wniosek p>=alpha, nie odrzucamy h0 -
# Nie ma wystarczających dowodów,
# aby odrzucić hipotezę, że 35% wszystkich studentów ma IQ wyższe niż 115.


#b)	Wyznaczyć przedział ufności dla proporcji wszystkich studentów mającej 
#IQ wyższy niż 115 na poziomie ufności 99% za pomocą
#i) przybliżenia do rozkładu normalnego
#ii) prop.test

# proporcja z próby
p_hat <- 30 / 100

#poziom nieufności - jak duze ryzyko bledu akceptujemy
alpha <- 0.01 

#realizacja z rozkładu normalnego
z <- qnorm(1 - alpha/2)

#bład standardowy
sep_hat <- sqrt(p_hat*(1-p_hat)/n) 

przedzial <- Pair(p_hat- t * sep_hat, p_hat + t*sep_hat)

prop.test(x = 30, n = 100, correct = FALSE, conf.level = 0.99)

#c)	Wyznaczyć przedział ufności dla średniego IQ wszystkich studentów na poziomie 
#ufności 90% w oparciu o wzór na przedział ufności dla dużej próby
#(czyli w oparciu o wartość krytyczną dla rozkładu normalnego).

#poziom nieufnosci
alpha <- 0.1

#srednie iq studentow
meanIQ <- 109

#kwantyl z rozkładu normalnego
z <- qnorm (1-alpha/2)

#błąd standardoy
s_e_meanIQ <- s / sqrt(n)

przedzial = Pair (meanIQ -z * s_e_meanIQ, meanIQ + z * s_e_meanIQ)

#d)	Wyznaczyć przedział ufności dla średniego IQ wszystkich studentów na poziomie
#ufności 90% w oparciu o wartość krytyczną dla rozkładu Studenta. 

alpha <- 0.1

meanIQ <- 109

#n-1 stopni swobody
t <- qt(1-0.1/2, n-1)

s_e_meanIQ <- s / sqrt(n)

przedzial <- Pair(meanIQ - z * s_e_meanIQ, meanIQ + z * s_e_meanIQ)

#e)	Przetestować hipotezę, że średni IQ studentów wynosi 115. 
#Wyznaczyć odpowiednią wartość p za pomocą i) testu Z, ii) testu T (studenta).

# H0: u0 = 115
# H1: u0 != 115

#maksymalny prawdopodobienstwo otrzymania bledu
alpha_max <- 0.05

#realizacja statystyki testowej
z <- abs ( sqrt(n) * (meanIQ - 115) / s  )

p_value <- 2 * (1 - pnorm(z))

#czy h0 falszywe
p_value < alpha_max

#wniosek ponieważ p_value<<0.05 mamy mocne dowody by odrzucic H0 i przyjąć H1

#test studenta
p_value <- 2 * (1-pt(z, df = n-1))
p_value < alpha_max


















