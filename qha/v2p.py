#!/usr/bin/env python3
"""
:mod:`v2p` -- title
========================================

.. module v2p
   :platform: Unix, Windows, Mac, Linux
   :synopsis:
.. moduleauthor:: Tian Qin <qinxx197@umn.edu>
.. moduleauthor:: Qi Zhang <qz2280@columbia.edu>
"""

import numpy as np

from qha.tools import _lagrange4
from qha.tools import vectorized_find_nearest
from qha.type_aliases import Matrix, Vector

# ===================== What can be exported? =====================
__all__ = ['v2p']


def v2p(funv: Matrix, p_tv: Matrix, p_vector: Vector) -> Matrix:
    """
    Obtain funp(T,P) given funv(T,V) and P(T,V)
    :param funv: property on (T,V) grid
    :param p_tv: pressure on (T,V) grid
    :param p_vector: desired pressure vector
    :return: property on (T,P) grid
    """
    nt, nv = funv.shape
    funp = np.empty((nt, nv))
    funv_large = np.empty((nt, nv + 2))
    funv_large[:, 1:-1] = funv
    funv_large[:, 0] = funv[:, 3]
    funv_large[:, -1] = funv[:, -4]
    p_large = np.empty((nt, nv + 2))
    p_large[:, 1:-1] = p_tv
    p_large[:, 0] = p_tv[:, 3]
    p_large[:, -1] = p_tv[:, -4]

    for i in range(nt):
        rs = np.zeros(len(p_vector))
        vectorized_find_nearest(p_large[i], p_vector, rs)
        for j in range(nv):
            np_k = int(rs[j])
            x1 = p_large[i, np_k]
            x2 = p_large[i, np_k + 1]
            x3 = p_large[i, np_k + 2]
            x4 = p_large[i, np_k + 3]
            f1 = funv_large[i, np_k]
            f2 = funv_large[i, np_k + 1]
            f3 = funv_large[i, np_k + 2]
            f4 = funv_large[i, np_k + 3]
            funp[i, j] = _lagrange4(p_vector[j], x1, x2, x3, x4, f1, f2, f3, f4)
    return funp