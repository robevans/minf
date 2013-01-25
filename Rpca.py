__author__ = 'Robert Evans'

import numpy as np
import rpy2.robjects as robjects
import rpy2.robjects.numpy2ri
rpy2.robjects.numpy2ri.activate()

r = robjects.r

with open("HorizontalArmSpin-Jibran.csv") as f:
	m = np.loadtxt(f,delimiter=",")

#m = r.matrix(r.rnorm(100), ncol=5)
pca = r.princomp(m)
r.plot(pca, main="Eigen values")
r.biplot(pca, main="biplot")