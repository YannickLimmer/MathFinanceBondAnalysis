import numpy as np
import scipy.linalg as la

class Covariance:

    matrix = None
    eigenValue_array = None
    eigenVector_matrix = None

    def __init__(self, data):
        # Initialize empty matrix
        size = len(data)
        self.matrix = np.empty((size,size))
        
        # Calculate the mean
        mean_array = []
        for randomvariable in data:
            sum = 0.0
            counter = 0
            for sample in randomvariable:
                sum += sample
                counter += 1
            mean_array.append(sum/counter)

        sampleSize = counter

        # Fill matrix
        for i in range(size):
            for j in range(size):
                sum = 0.0
                for k in range(sampleSize):
                    sum += (data[i][k] - mean_array[i])\
                        *(data[j][k] - mean_array[j])
                self.matrix[i,j] = sum/(sampleSize-1)
        
        # Calculate Eigenvalues and Eigenvectors
        self.eigenValue_array, self.eigenVector_matrix = la.eig(self.matrix)
        self.eigenValue_array = (self.eigenValue_array).real
        

