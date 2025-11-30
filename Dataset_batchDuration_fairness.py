import json
import numpy as np



def read_data(path):
    with open(path, 'r') as reader:
        return json.load(reader)


data_path = "results/Dataset_batchDuration/"
algorithms = [ "MyAlg-0.25","MyAlg-0.50","MyAlg-0.75", "TORA", "CD"]

batch_duration = str(120)
low_emiss = 151
high_emiss = 250

low_driver_perc = 0
med_driver_perc = 0
high_driver_perc = 0
data = read_data(data_path + f"rideInfo_CD.json")[batch_duration][0]
for (emission, cnt) in data:
    if emission <= low_emiss:
        low_driver_perc += 1
    elif emission <= high_emiss:
        med_driver_perc += 1
    else:
        high_driver_perc += 1

n = low_driver_perc + med_driver_perc + high_driver_perc
print(f"Low drivers: {100*low_driver_perc/n} - Med drivers: {100*med_driver_perc/n} - High drivers: {100*high_driver_perc/n}")

for alg in algorithms:
    data = read_data(data_path + f"rideInfo_{alg}.json")[batch_duration]
    low_perc = []
    high_perc = []
    for trial in range(len(data)):
        trial_data = data[trial]
        n_low = 0
        n_med = 0
        n_high = 0
        for (emission, cnt) in trial_data:
            if emission <= low_emiss:
                n_low += cnt
            elif emission <= high_emiss:
                n_med += cnt
            else:
                n_high += cnt
        n = n_low + n_med + n_high
        low_perc.append(n_low / n)
        high_perc.append(n_high / n)

    low_perc_val = np.average(low_perc)*100
    high_perc_val = np.average(high_perc)*100
    print(f"{alg}: Low: {low_perc_val}% - Med: {100-low_perc_val - high_perc_val} - High: {high_perc_val}")


print("\n\nDeadhead / Total Trip ratio:")

for alg in algorithms:
    data = read_data(data_path + f"driverInfo_{alg}.json")[batch_duration]
    low_perc = []
    med_perc = []
    high_perc = []
    for trial in range(len(data)):
        trial_data = data[trial]
        for (emission, frac) in trial_data:
            val = frac / (1 + frac)
            if emission <= low_emiss:
                low_perc.append(val)
            elif emission <= high_emiss:
                med_perc.append(val)
            else:
                high_perc.append(val)


    low_perc_val = np.average(low_perc)*100
    med_perc_val = np.average(med_perc)*100
    high_perc_val = np.average(high_perc)*100
    print(f"{alg}: Low: {low_perc_val}% - Med: {med_perc_val} - High: {high_perc_val}")


