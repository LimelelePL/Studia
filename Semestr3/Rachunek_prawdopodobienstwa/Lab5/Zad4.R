#
#4.	Przetestować hipotezę, że średni wzrost studentek wynosi 160cm za pomocą 
#polecenia t.test

waga <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/Lab5/waga1.csv", sep = ';')

mean_height <- 160
#H0: mean_height = 160
#H1: mean_height != 160

dane <- waga [waga$plec == 1,] $ Wzrost
t.test(dane, mu = mean_height, conf.level = 0.95)

#ponieważ p >0.05 mamy dowody na to, że H0 jest prawdziwa


