#g(x) = 0.5x 0<=x<=2

#a)	i) Napisać algorytm, który losuje realizację z tego rozkładu za pomocą metody odwracania dystrybuanty.
#ii) Wygenerować 200 realizacji z tego rozkładu za pomocą tego algorytmu.

# dystrybuanta F(x) = 0.25x^2 
# odwrotna funckja do F(x)  to f(p) = 2sqrt(p) dla 0<=p<=1

f <- function(p){
  return(2*sqrt(p))
}

genRealization <- function (func) { 
  # gdzie func to funkcja odwrotna dystrybuanty
  u <- runif(1)
  return( func(u) )
}

rep <- 200
res <- numeric(rep)

for (i in 1 : rep) {
  res[i] <-  genRealization(f)
}


#b)
#i) Napisać własny (tym razem nie wykorzystujemy gotowej funkcji) algorytm, 
#który losuje realizację z tego rozkładu za pomocą metody przyjęcia i odrzucenia.
#ii) Wygenerować 200 realizacji z tego rozkładu za pomocą tego algorytmu.


#ponieważ funkcja g określona jest na przedziale, korzystam z 
# uproszczonej metody przyjecia i odrzucenia

g <- function(x) {
  return(0.5*x)
}

genOneRealization <- function(g) {
  a<-0
  b<-2
  maxG <- 0.5*2
  
  while (TRUE) {
    x <- runif(1, a, b)
    u <- runif(1)
    
    if(u < g(x)/maxG) {
      return(x)
    }
  }
}


rep <- 200
res <- numeric(rep)

for (i in 1:rep) {
 res[i] <- genOneRealization(g)
}

