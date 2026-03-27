
#Wyznaczyć przedział ufności dla średniego wzrostu wszystkich studentów (obu płci) na poziomie ufności 90%.

waga <- read.csv("C:/Users/Dudek/OneDrive/Pulpit/Repozytoria/Rachunek_prawdopodobienstwa_lab/Lab5/waga1.csv", sep = ';')

alpha <- 0.1
n <- length(waga$Wzrost)
mean_height <- mean(waga$Wzrost)
s_height <- sd(waga$Wzrost)

s_e_mean_height <- s_height / sqrt (n)
t <- qnorm(1-alpha/2)

przedzial <- Pair ( mean_height - s_e_mean_height*t, mean_height + s_e_mean_height*t  )

