from numpy import cos
import torch


def contact_distance(u1, u2, rij_angle,  chi, sigma_0):
    a = (cos(u1 - rij_angle) + cos(u2 - rij_angle)) ** 2 / (1 + chi * cos(u1 - u2))
    b = (cos(u1 - rij_angle) - cos(u2 - rij_angle)) ** 2 / (1 - chi * cos(u1 - u2))
    c = (1 / 2) * chi * (a + b)
    sigma = sigma_0 * (1 - c) ** (-(1 / 2))
    return sigma


def free_energy_hgo(yhat, rho, x, simpson_matrix, hgo_excluded_area, lambd):
    f1 = torch.mm(yhat, yhat.T) * hgo_excluded_area
    dx = x[1] - x[0]
    first_term = (dx / 3) * torch.mm(simpson_matrix, yhat * torch.log(rho * yhat))
    second_term = (rho / 2) * (dx / 3) ** 2 * torch.mm(torch.mm(simpson_matrix, f1), simpson_matrix.T)
    third_term = lambd * (((dx / 3) * (torch.mm(simpson_matrix, yhat))) - 1) ** 2
    loss = first_term + second_term + third_term
    return loss
