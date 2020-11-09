
import numpy as np
import matplotlib.pyplot as plt
from numpy import cos

k = 3
chi = (k**2 - 1) / (k**2 + 1)
sigma_0 = 1
## r_points is theta_1
r_points = np.linspace(0, 2 * np.pi, 100, endpoint=True)
## orientation_points is theta_2
orientation_points = np.linspace(0, 2 * np.pi, 20, endpoint=True)
#%%
def contact_distance_1(chi, r, sigma_0):
    a = (2 * cos(r))**2/(1 + chi)
    b = (1/2) * chi * a
    sigma = sigma_0 * (1 - b)**(-(1/2))
    return sigma

def contact_distance_2(r, orientation, chi, sigma_0):
    a = (cos(r) + cos(r - orientation)) **2 / (1 + chi * cos(orientation))
    b = (cos(r) - cos(r - orientation)) **2 / (1 - chi * cos(orientation))
    c = 1 - (1/2)*chi*(a)
    sigma = sigma_0 * c*(-1/2)
    return sigma

contact_distance = {}
for orientation in orientation_points:
    contact_distance["theta_2 = " + str(orientation)] = []
    for r in r_points:
        contact_distance["theta_2 = " + str(orientation)].append(contact_distance_2(r, orientation, chi, sigma_0))


fig = plt.figure()
ax_2 = fig.add_subplot(111, projection='polar' )
for i in range(len(orientation_points)):
    ax_2.cla()
    ax_2.plot (r_points, contact_distance["theta_2 = " + str(orientation_points[i])])
    plt.pause(0.5)
