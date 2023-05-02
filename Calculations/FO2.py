import matplotlib.pyplot as plt

fo2_frequencies = {'120 40 Max': 1000/40, '120 32 Max': 1000/32, '120 25 Max': 1000/25, '120 25 Sub': 1000/25}

def plot_fo2(fo2_slopes):
    treatments = fo2_slopes.keys()
    data = fo2_slopes.values()
    freqs = [fo2_frequencies[treatment] for treatment in treatments]
    plt.figure()
    plt.plot(freqs, data, '-.')
    plt.plot(freqs, data, '.', color='Red')
