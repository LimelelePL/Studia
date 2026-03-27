#i)	Wygenerować 100 realizacji z rozkładu Bin(10; 0,3)

n<-10
p<-0.3
rep <- 100
res <- numeric(rep)

for (i in 1:rep) {
  #generujemy 10 liczb losowych 
  u <- runif(n)
  
  #symulujemy 10 prób bernoullego 
  #sukces jest gdy p>u (1) wpp porażka (0)
  #wynikiem jest ilosc sukcesów
  res[i] <- length(which(p>u))
}


#ii)	Wygenerować 50 realizacji z rozkładu Geom(0,4)

p<-0.4
rep <- 50
res <- numeric(rep)

for (i in 1:rep) {
  #ilosc prób
  tries <- 0
  succes <- FALSE
 
  #zliczamy ilosc prób do wystąpienia pierwszego sukcesu
  while(!succes) {
    u <- runif(1)
    
    # wystąpił sukces 
    if (p>u) {
      res[i]<-tries+1
      succes <- TRUE;
    }
    
    tries <- tries + 1
  }
}


