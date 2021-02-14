from typing import Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class Superformula(object):

    a: float = 1.
    b: float = 1.
    m1: float = 8.
    m2: float = 8.
    n1: float = 0.5
    n2: float = 0.5
    n3: float = 8.

    def rho(self, alpha: np.ndarray) -> np.ndarray:
        term1 = np.abs(np.cos(self.m1 * alpha / 4) / self.a)
        term2 = np.abs(np.sin(self.m2 * alpha / 4) / self.b)
        result = np.power(np.power(term1, self.n2) + np.power(term2, self.n3), -1/self.n1)
        return result

    def xyz(self, theta: np.ndarray, phi: np.ndarray) -> Tuple[np.ndarray]:
        rho_theta = self.rho(theta)
        rho_phi = self.rho(phi)
        x = rho_theta * np.cos(theta) * rho_phi * np.cos(phi)
        y = rho_theta * np.sin(theta) * rho_phi * np.cos(phi)
        z = rho_phi * np.sin(phi)
        return x, y, z

    def point_cloud(self, step: float) -> np.ndarray:
        theta = np.arange(-np.pi, np.pi, step)
        phi = np.arange(-np.pi / 2, np.pi / 2, step / 2)
        theta, phi = np.meshgrid(theta, phi)
        x, y, z = self.xyz(theta, phi)
        pc = np.stack((np.ravel(x), np.ravel(y), np.ravel(z)), axis=1)
        return pc
