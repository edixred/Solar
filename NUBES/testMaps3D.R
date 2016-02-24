# 3D Plot of Half of a Torus
library(plot3D)
library(misc3d)
library(mvtnorm);
library(MASS);
set.seed(5)
sigma <-matrix(c(4,2,2,3), ncol=2)
x<-rmvnorm(n=500, mean=c(1,2), sigma=sigma,
           method="chol")
z<-kde2d(x[,1],x[,2],n=200);
par(mar=rep(0,4))
persp(z,theta=60,phi=5,col=heat.colors(199,alpha=1),
      shade=0.4,border=NA,box=FALSE)
#----------
persp3D(z = volcano, zlim = c(-60, 200), phi = 20,
        colkey = list(length = 0.2, width = 0.4, shift = 0.15,
                      cex.axis = 0.8, cex.clab = 0.85), lighting = TRUE, lphi = 90,
        clab = c("","height","m"), bty = "f", plot = FALSE)
# create gradient in x-direction
Vx <- volcano[-1, ] - volcano[-nrow(volcano), ]
# add as image with own color key, at bottom
image3D(z = -60, colvar = Vx/10, add = TRUE,
        colkey = list(length = 0.2, width = 0.4, shift = -0.15,
                      cex.axis = 0.8, cex.clab = 0.85),
        clab = c("","gradient","m/m"), plot = FALSE)
# add contour
contour3D(z = -60+0.01, colvar = Vx/10, add = TRUE,
          col = "black", plot = TRUE)




