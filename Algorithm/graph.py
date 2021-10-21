import numpy as np
import matplotlib.pyplot as plt


def create_graph(runtime, indp_var):
    degree = 4
    coeffs = np.polyfit(indp_var,runtime, degree)
    p = np.poly1d(coeffs)
    plt.plot(indp_var, runtime, 'or')
    plt.plot(indp_var, [p(n) for n in indp_var], '-b')

    plt.xlabel(indp_var)
    plt.ylabel("Runtime (seconds)")

    plt.show()

