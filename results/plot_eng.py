
import matplotlib.pylab as plt
import numpy as np

for sample in ["airebo", "nnp"]:

    log= np.loadtxt("param-%s.dat" % sample)[1:, :]
    plt.plot(log[:, 1], log[:, 2], 'o', label=sample.upper())

# plt.title("T=300K")
# plt.ylabel("<h$^2$> ($\AA^2$)")
# plt.xlabel("elapsed time (ps)")
plt.ylabel("energy (eV/atom)", fontsize=13)
plt.xlabel("temperature (K)", fontsize=13)
plt.legend(fontsize=13, loc='lower right')
plt.grid()
plt.tight_layout()
plt.savefig("eng.png")
plt.show()