#3.	Wygenerować 1000 liczb z następnego rozkładu dyskretnego 
#(należy zminimalizować oczekiwany czas działania).

#k	    0	     1	   2 	 3
#P(X=k)	0,15	0,25	0,5	0,1

#minimalizacja czasu działania polega na posortowaniu
#prawdopodobieństw malejąco oraz ustawnieniu odpowiadających im wartości
#na odpowiednich indeksach
probabilities <- c(0.5, 0.25, 0.15, 0.1)
values <- c(2, 1, 0, 3)

#obliczam wektor prawdopodobienstw skumulowanych
cumulated_prob <- cumsum(probabilities)

n <- 1000

u <- runif(n)
result <- numeric(n)

for (i in 1:n) {
  j <- 1
  # szukamy odpowiedniego przedziału 
  while (u[i] > cumulated_prob[j]) {
    j <- j + 1
  }
  
  result[i] <- values[j]
}

