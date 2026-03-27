#5.	Wyznaczyć przedział ufności dla średniego wzrostu studentek na poziomie ufności 98%.
waga <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/Lab5/waga1.csv", sep = ';')

n <-  nrow(waga[waga $ plec == 1 ,])
mean_height = mean (waga[waga $ plec ==1 ,] $Wzrost)
s_height <- sd (waga[waga $ plec ==1 ,] $Wzrost)

s_e_mean_height <- s_height / sqrt(n)
alpha = 0.02
z <- qnorm(1 - alpha/2)
przedzial <- Pair( mean_height - z * s_e_mean_height,  mean_height + z * s_e_mean_height )
