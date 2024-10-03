import csv
import numpy as np
import matplotlib.pyplot as plt


test_names = ['blackscholes', 'canneal', 'dedup', 'ferret', 'freqmine', 'radix', 'vips']
x = [1, 2, 4, 8]
blackscholes = [[124.426, 72.653, 46.261, 36.132], [124.595, 72.674, 46.251, 36.280], [124.607, 72.703, 46.142, 36.497]]
canneal = [[248.526, 154.811, 104.896, 84.481], [250.396, 151.352, 105.089, 85.451], [255.295, 154.397, 105.757, 84.885]]
dedup = [[20.528, 11.985, 9.119, 9.838], [20.414, 12.365, 9.547, 11.147], [19.754, 12.151, 9.395, 9.981]]
ferret = [[319.446, 163.657, 93.113, 79.817], [321.154, 163.907, 93.223, 79.923], [319.405, 164.924, 92.950, 80.019]]
freqmine = [[490.537, 249.269, 125.602, 101.516], [489.190, 248.574, 125.917, 102.024], [489.047, 248.142, 126.174, 103.356]]
radix = [[53.868, 26.940, 13.689, 8.654], [52.934, 27.041, 13.753, 8.683], [52.917, 27.178, 13.771, 8.660]]
vips = [[99.308, 50.958, 25.584, 22.418], [99.111, 49.851, 25.938, 22.161], [99.710, 51.981, 25.853, 22.033]]

def get_meanstd(array):
    for list in array:
        for i in range(len(list) - 1, -1, -1):
            list[i] = list[0] / list[i]
    array = [np.array(x) for x in array]
    array_mean = [np.mean(k) for k in zip(*array)]
    array_std = [np.std(k) for k in zip(*array)]
    return array_mean, array_std

tests = {test_names[0]: blackscholes, test_names[1]: canneal, test_names[2]: dedup, test_names[3]: ferret, test_names[4]: freqmine, test_names[5]: radix, test_names[6]: vips}

plt.style.use('ggplot')
plt.rc('axes', labelsize=13)
plt.xlabel("Number of threads")
plt.ylabel("Speedup", loc='top', rotation='horizontal')
plt.xlim([0, 9])
plt.ylim([0, 9])
plt.yticks(range(0, 9), fontsize=10)
plt.xticks(range(0, 9), fontsize=10)
for test in test_names:
    y, y_err = get_meanstd(tests[test])
    #plt.plot(x, y, label=test+" interference", marker='o')
    #plt.plot(x, y, label="parsec-" + test, marker='o')
    plt.errorbar(x, y, yerr=0, label="parsec-" + test, capthick=1.3, elinewidth=1.5, fmt='-o', mec='white', mew=.75)
    #plt.errorbar(x, y, xerr=x_err, yerr=y_err)
dashed = [0, 9]
plt.plot(dashed, dashed, linestyle='dashed', color='gray')
plt.legend(fontsize=8)
plt.gca().set_aspect('equal')
plt.savefig('plot2b.pdf', bbox_inches='tight')
#plt.show()
plt.close()
