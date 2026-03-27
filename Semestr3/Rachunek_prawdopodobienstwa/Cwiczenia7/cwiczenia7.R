
cum_prob <- function (prob) {

  len <- length(prob)
  res <- array (0, dim = len)
  res [1] = prob[1]
  
  for (i in 2:len) {
    res[i] <- res[i-1] + prob[i]
  }
  
  return(res)
}


#zadanie 1
#wartosci i prawdopodobienstwa musza byc uporządkowane malejąco
values <- c(2,1,3,5)
probabilities <- c(0.4, 0.2, 0.3, 0.1)
n <- 5


draw_realizationU <- function (cum_prob, values, u, n) {
  realization <- array(0, n) # n to liczba losowań
  for (i in 1:n){
    j<-1
    #szukamy przedziału do którego wpadła zmienna u
    #optymalne bo najbardziej prawdopodobne zdarzenia trafiaja na poczatek 
    while(u[i] > cum_prob[j]){
      j<- j+1
    }
    realization[i] <- values[j]
  }
  return(realization)
}

#obliczamy wektor prawdopodobienstw skumulowanych
cum_prob <- cum_prob(probabilities)
# generujemy 5 realizacji
u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152)
realizations <- draw_realizationU(cum_prob, values, u, n)

#zadanie 2
# rozkład gemometryczny modeluje ile porażek nastąpi przed pierwszym sukcesem bernoullego
#a)
p <- 0.5
n <- 2
draw_realizationG <- function(p, u, n) {
  res <- numeric(n)
  index <- 1
  
  for (i in 1:n) {
    trails <- 0
    
    while (index <= length(u)) {
      
      if (u[index] < p) { #aby byl sukces wylosowany przedzial musi byc mniejszy od p
        res[i] <- trails            # zapisujemy liczbę porażek
        index <- index + 1          
        break                       # wychodzimy z geom dla tego i
      }
      
      trails <- trails + 1          # porażka zwiększamy licznik
      index <- index + 1
      
    }
  }
  
  return(res)
}


u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152)
realizations <- draw_realizationG(p, u, n)

#b)

p <- 0.5
u <- c(0.641932, 0.019873, 0.171584, 0.263589, 0.663152)
n <- 5

draw_realizationGP <- function(p, u, n) {
  res <- numeric(n)
  
  for (i in 1:n) {
    k <- 1
    cum <- p  # P(X = 1)
    
    while (u[i] > cum) { #czy  wylosowana wartość u_i znajduje się w bieżącym skumulowanym przedziale
      k <- k + 1 # przechodzimy do nastepnej wartosci zmiennej losowej k - kolejnej próby
      cum <- cum + (1 - p)^(k - 1) * p
    }
    
    res[i] <- k
  }
  
  return(res)
}

realizations <- draw_realizationGP(p, u, n)

#zad 3 
#a)
#dystrybuanta F(X) = x^2/4 F^-1(p) = 2sqrt(p) dla 0<=p<=1 (p to prawdopodobienstwo)

#dystrybuanta
f <- function(x) {
  return(x^2/4)
}

#odwrotnosc dystrybuanty
g <- function(x) {
  return(2*sqrt(x))
}

draw_realization3a <- function(u,n) {
  res = array(0,n)
  for (i in 1:n) {
    res[i] = g(u[i])
  }
  return(res)
}
u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152)
realizations3a <- draw_realization3a(u,5)

#b)

draw_realization3b <- function(u,n) {
  a<- 0 
  b<- 2
  res = array(0,n)
  ui <- 1
  
  
  for (i in 1:n) {
    while (TRUE) { #0.5x
      x <- runif(1,a,b)
      #u <- runif(1)
      if(u[ui]< ( 0.5*x )){
        res[i] = x
        break
      } else {
        ui <- ui + 1
      }
    }
  }
  return(res)
}
u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152,  0.985853,  0.641737,  0.476182,  0.991198,  0.288609)
realizations3b <- draw_realization3b(u,3)

#c
a<- 0 
b<- 2
p <- 1/((b-a)*1)
result <- 1/p

#zad 4
#a

f <- function (x) {
  return(cos(x))
}

draw_realization4a <- function(u,n) {
  a<- 0 
  b<- pi/2
  res = array(0,n)
  ui <- 1
  
  for (i in 1:n) {
    while (TRUE) { #bo max(cosx) = cos 0 = 1
      x <- runif(1,a,b)
      if(u[ui]< ( f(x))){ 
        res[i] = x
        break
      }
      ui <- ui + 1
    }
  }
  return(res)
}

u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152,  0.985853,  0.641737,  0.476182,  0.991198,  0.288609)
realizations4a <- draw_realization4a(u,3)

#liczba propozycji calka to pi
p <- pi/((b-a)*1)
result <- 1/p

#b

draw_realization4b <- function(u,n) {

 res <- array(0,n)
 ui <- 1
 
for (i in 1:n) {
  x <- draw_realization4a(u, 1)
  if (u[ui]<0.5) {
    x<--x
  }
  res[i] <- x
  ui <- ui + 1
}
 return(res)
}


u <- c(0.641932, 0.019873, 0.171584,  0.263589, 0.663152,  0.985853,  0.641737,  0.476182,  0.991198,  0.288609)
realizations4b <- draw_realization4b(u,3)

# Kod w języku R do wygenerowania wykresu rozrzutu:
X <- c(0, 0, 1, 1)
Y <- c(0, 1, 1, 2)

plot(X, Y, 
     main="Rozrzut dla Regresji Y względem X", 
     xlab="X (Orły w pierwszym rzucie)", 
     ylab="Y (Całkowita liczba orłów)",
     xlim=c(-0.5, 1.5), 
     ylim=c(-0.5, 2.5),
     pch=16, # Kształt punktu (solid circle)
     cex=2)  # Rozmiar punktu
grid()





 

