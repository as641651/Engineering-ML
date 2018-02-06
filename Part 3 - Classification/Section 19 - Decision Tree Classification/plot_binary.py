import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def plot_binary(X,y,classifier,stp=0.01):
   X_set, y_set = X, y
   X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = stp),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = stp))
   plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
   plt.xlim(X1.min(), X1.max())
   plt.ylim(X2.min(), X2.max())
   for i, j in enumerate(np.unique(y_set)):
       plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
   return plt
   #plt.title('KNN (Training set)')
   #plt.xlabel('Age')
   #plt.ylabel('Estimated Salary')
   #plt.legend()
   #plt.show()
