#2.	Przetestować hipotezę, że średni wzrost wszystkich studentów wynosi
#170cm za pomocą polecenia t.test

waga <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/Lab5/waga1.csv", sep = ';')
head (waga,5)

mean_height = 170

#H0: mean_height = 170
#H1: mean_height != 170

dane <- waga$Wzrost
alpha_max <- 0.05

t.test(dane,mu = mean_height ,conf.level = 0.95 )

# ponieważ p << 0.5 mamy mocne dowody aby odrzucic hipoteze H0
