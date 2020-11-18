import matplotlib.pyplot as plt
import numpy as np
import torch
from Functions import contact_distance
from scipy import integrate

'''
Class: Data
input_variable() will return a two dimension data set, [sin(x), cos(x)]

@Author: Naicheng Deng
'''


class Data():

    def __init__(self, points, lower, upper, k, sigma_0):
        self.points = points
        self.upper = upper
        self.lower = lower
        self.k = k
        self.chi = (self.k**2 - 1)/(self.k**2 + 1)
        self.sigma_0 = sigma_0
        self.x = np.linspace(self.lower, self.upper, self.points, endpoint=False)
        self.x = torch.from_numpy(self.x)
        self.hgo_excluded_area = torch.zeros([self.points, self.points])
        self.simpson_matrics = torch.ones(self.points)
        self.input_var = torch.zeros((self.points, 2))

    def variables(self):
        for i in range(self.points):
            self.input_var[i][0] = torch.cos(self.x[i])
            self.input_var[i][1] = torch.sin(self.x[i])
        return self.x, self.input_var

    def calculate_area(self):
        i = 0
        for u1 in self.x:
            j = 0
            for u2 in self.x:
                contact_distance_list = []
                for rij in self.x:
                    contact_distance_list.append(contact_distance(u1, u2, rij, self.chi, self.sigma_0))
                I = (1 / 2) * integrate.simps(contact_distance_list, self.x)
                self.hgo_excluded_area[i][j] = I
                j += 1
            i += 1
        return self.hgo_excluded_area

    def simpson_matrix(self):
        for i in range(self.points):
            if i % 2 == 0:
                self.simpson_matrics[i] = 2
            if i % 2 != 0:
                self.simpson_matrics[i] = 4
        self.simpson_matrics[0], self.simpson_matrics[-1] = 1, 1
        self.simpson_matrics = self.simpson_matrics.reshape(1, -1)
        return self.simpson_matrics



