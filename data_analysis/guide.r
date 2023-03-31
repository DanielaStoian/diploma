library(lubridate)
library(forecast)
library(rpart)
library(gbm)
library(plyr)
library(tsutils)

tl <- function(x, ...) {
  x <- as.ts(x)
  tspx <- tsp(x)
  n <- length(x)
  tt <- 1:n
  fit <- supsmu(tt, x)
  out <- ts(cbind(trend = fit$y, remainder = x - fit$y))
  tsp(out) <- tsp(x)
 
  out <- structure(list(time.series = out), class = "stl")
  return(out)
}
lpb <- function(x, nsim=100) {
  n <- length(x)
  meanx <- mean(x)
  y <- x - meanx
  gamma <- wacf(y, lag.max = n)$acf[, , 1]
  s <- length(gamma)
  Gamma <- matrix(1, s, s)
  d <- row(Gamma) - col(Gamma)
  for (i in 1:(s - 1))
    Gamma[d == i | d == (-i)] <- gamma[i + 1]
  L <- t(chol(Gamma))
  W <- solve(L) %*% matrix(y, ncol = 1)
  out <- ts(L %*% matrix(sample(W, n * nsim, replace = TRUE), nrow = n, ncol = nsim) + meanx)
  tsp(out) <- tsp(x)
  return(out)
}
MBB <- function(x, window_size) {
  bx <- array(0, (floor(length(x) / window_size) + 2) * window_size)
  for (i in 1:(floor(length(x) / window_size) + 2)) {
    c <- sample(1:(length(x) - window_size + 1), 1)
    bx[((i - 1) * window_size + 1):(i * window_size)] <- x[c:(c + window_size - 1)]
  }
  start_from <- sample(0:(window_size - 1), 1) + 1
  bx[start_from:(start_from + length(x) - 1)]
}
bld.mbb.bootstrap <- function(x, num, block_size=NULL, mu) {
 
  if(length(x) <= 1L)
    return(rep(list(x), num))
 
  freq <- frequency(x)
  if(length(x) <= 2*freq)
    freq <- 1L
 
  if (is.null(block_size)) {
    block_size <- ifelse(freq > 1, 2 * freq, min(8, floor(length(x) / 2)))
  }
 
  xs <- list()
  xs[[1]] <- x # the first series is the original one
 
  if (num > 1) {
    # Box-Cox transformation
    if (min(x) > 1e-6) {
      lambda <- BoxCox.lambda(x, lower = 0, upper = 1)
    } else {
      lambda <- 1
    }
    x.bc <- BoxCox(x, lambda)
    lambda <- attr(x.bc, "lambda")
    if (freq > 1) {
      # STL decomposition
      x.stl <- stl(ts(x.bc, frequency = freq), "per")$time.series
      seasonal <- x.stl[, 1]*mu
      trend <- x.stl[, 2]
      remainder <- x.stl[, 3]
    } else {
      # Loess
      trend <- 1:length(x)
      suppressWarnings(
        x.loess <- loess(ts(x.bc, frequency = 1) ~ trend, span = 6 / length(x), degree = 1)
      )
      seasonal <- rep(0, length(x))
      trend <- x.loess$fitted
      remainder <- x.loess$residuals
    }
  }
 
  # Bootstrap some series, using MBB
  for (i in 2:num) {
    xs[[i]] <- ts(InvBoxCox(trend + seasonal + MBB(remainder, block_size), lambda))
    tsp(xs[[i]]) <- tsp(x)
  }
 
  xs
}

setwd("C:\\Users\\vangelis spil\\Desktop\\ev allocation\\new")

cluster <- "A"
multi <- 3

for (cluster in c("A","B","C","D")){
  for (multi in c(3,5,10)){
   
    datain <- read.csv(paste0("cluster_",cluster,".csv"))
    datain$X <- NULL
    datain$Date <- as.Date(datain$Date)
    datain$Start_hour <- as.factor(datain$Start_hour)
    datain$wd <- as.factor(weekdays(datain$Date))
    datain$month <- as.factor(month(datain$Date))
    k <- ts(datain$Demand, frequency = 168)
   
    stat_multi <- 1 ; mustart <- 1
    num_boots <- 4
    while (stat_multi<multi) {
      new_series <- k - k
      set.seed(123)
      boots <- bld.mbb.bootstrap(k, num=num_boots, mu=mustart)
      for (i in 1:num_boots){
        new_series <- new_series + boots[[i]]
      }
      new_series[new_series<0] <- 0
      new_series <- round(new_series/num_boots,0)
      datain$Demand2 <- new_series
      stat_multi <- round(sum(datain$Demand2)/sum(datain$Demand),0)
      mustart <- mustart + 1
    }
    print(stat_multi)
   
    par(mfrow=c(1,2))
    k <- ts(datain$Demand, frequency = 168)
    seasplot(k, outplot = 4, trend = F, ylim=c(0,max(k)), main= cluster)
    seasplot(new_series, outplot = 4, ylim=c(0,max(new_series,k)), trend = F, main= "Simulated")
   
    i=1
    plot(k[i:(i+167)], type="l", ylim = c(0,7))
    lines(new_series[i:(i+167)], col="red")
    i <- i+168
   
    stats <- ddply(datain[,c("Start_hour","Demand","Demand2")], .(Start_hour), colwise(mean))
    plot(stats$Demand2, col="red", type="l")
    lines(stats$Demand)
   
    stats <- ddply(datain[,c("wd","Start_hour","Demand","Demand2")], .(wd,Start_hour), colwise(mean))
    plot(stats$Demand2, col="red", type="l")
    lines(stats$Demand)
   
    # plot(density(datain$Demand2, bw=0.1), col=2, ylim=c(0,4), main = "")
    # lines(density(datain$Demand, bw=0.1))
   
    write.csv(datain, paste0("multi",multi,"/cluster_",cluster,"_",multi,".csv"))
   
  }
}