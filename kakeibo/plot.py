# coding: utf-8

import matplotlib.pyplot as plt


def plot_gas_and_electricity(data_list):
    gas_x = []
    gas_y = []
    elec_x = []
    elec_y = []

    for data in data_list:
        if data.shop.find("大阪ガス") != -1:
            gas_x.append(data.date)
            gas_y.append(data.charge)

        if data.shop.find("関西電力") != -1:
            elec_x.append(data.date)
            print(data)
            elec_y.append(data.charge)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(gas_x, gas_y, label="Gas")
    ax.plot(elec_x, elec_y, label="Electricity")
    plt.legend()
    plt.show()


