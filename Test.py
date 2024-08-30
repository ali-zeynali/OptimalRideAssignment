import numpy as np
from matplotlib import pyplot as plt
def custom_exponential_sample(lam, low, high):
    # Generate a sample from the exponential distribution
    sample = np.random.exponential(scale=1 / lam)

    # Normalize the sample to a [0, 1] range (assuming the exponential distribution's range)
    sample = 1 - np.exp(-sample)  # Invert the distribution

    # Scale and shift the sample to the [low, high] range
    scaled_sample = low + sample * (high - low)

    return scaled_sample


def plot_CDF(data):
    for lab in data:
        sorted_data = sorted(data[lab])
        x = []
        y = []
        n = len(sorted_data)
        for i, v in enumerate(sorted_data):
            x.append(v)
            y.append((i + 1) / n)
        plt.plot(x, y, label=lab)
    plt.legend()
    plt.show()


data1 = [custom_exponential_sample(0.1, 10, 50) for _ in range(10000)]
data2 = [custom_exponential_sample(1, 10, 50) for _ in range(10000)]
data3 = [custom_exponential_sample(5, 10, 50) for _ in range(10000)]

data = {}
data['0.1'] = data1
data['1'] = data2
data['100'] = data3

plot_CDF(data)