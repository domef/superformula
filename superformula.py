import math
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

    def xyz(self, theta: np.ndarray, phi: np.ndarray) -> np.ndarray:
        rho_theta = self.rho(theta)
        rho_phi = self.rho(phi)
        x = rho_theta * np.cos(theta) * rho_phi * np.cos(phi)
        y = rho_theta * np.sin(theta) * rho_phi * np.cos(phi)
        z = rho_phi * np.sin(phi)
        xyz = np.stack([x, y, z], axis=2)
        return xyz

    def point_cloud(self, resolution: int) -> np.ndarray:
        theta = np.linspace(-np.pi, np.pi, resolution, endpoint=False)
        phi = np.linspace(-np.pi / 2, np.pi / 2, resolution // 2, endpoint=False)
        theta, phi = np.meshgrid(theta, phi)
        xyz = self.xyz(theta, phi)
        pc = xyz.reshape(-1, 3)
        return pc

    def triangulate(self, pc: np.ndarray) -> np.ndarray:
        dim = math.floor(math.sqrt(len(pc) * 2) / 2)
        indeces = np.arange(len(pc)).reshape((dim, -1))
        indeces = np.concatenate([indeces, indeces[:, [0]]], axis=1)
        v1 = indeces[:-1, :-1]
        v2 = indeces[:-1, 1:]
        v3 = indeces[1:, 1:]
        v4 = indeces[1:, :-1]
        tr1 = np.stack([v1, v3, v4], axis=2).reshape(-1, 3)
        tr2 = np.stack([v1, v2, v3], axis=2).reshape(-1, 3)
        triangles = np.concatenate([tr1, tr2], axis=0)
        return triangles
