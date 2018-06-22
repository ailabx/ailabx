from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

def poly_model(degree=1):
    poly_features = PolynomialFeatures(degree=degree,include_bias=True)
    linear = LinearRegression(normalize=True)
    pipeline = Pipeline([('polynomial_features',poly_features),('linear_regression',linear)])
    return pipeline

model = poly_model()

import numpy as np
x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                    [9.779], [6.182], [7.59], [2.167], [7.042],
                    [10.791], [5.313], [7.997], [3.1]])

y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                    [3.366], [2.596], [2.53], [1.221], [2.827],
                    [3.465], [1.65], [2.904], [1.3]])
model.fit(x_train,y_train)
score = model.score(x_train,y_train)
print(score)
mse = mean_squared_error(y_train,model.predict(x_train))
print(mse)

import matplotlib.pyplot as plt
plt.scatter(x_train,y_train)
plt.plot(x_train,model.predict(x_train),'r-')
plt.show()