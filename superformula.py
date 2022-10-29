from dataclasses import dataclass
from typing import Tuple

import numpy as np

EPSILON = 1e-8


@dataclass
class Superformula:

    a: float = 1.0
    b: float = 1.0
    m: float = 8.0
    n1: float = 0.5
    n2: float = 0.5
    n3: float = 8.0

    def rho(self, alpha: np.ndarray) -> np.ndarray:
        term1 = np.abs(np.cos(self.m * alpha / 4) / (self.a + EPSILON))
        term2 = np.abs(np.sin(self.m * alpha / 4) / (self.b + EPSILON))
        base = np.power(term1, self.n2) + np.power(term2, self.n3)
        exponent = -1 / (self.n1 + EPSILON)
        result = np.power(base, exponent)
        return result

    def xyz(
        self, theta: np.ndarray, phi: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
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
