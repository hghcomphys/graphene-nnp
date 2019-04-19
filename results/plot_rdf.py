
import matplotlib.pylab as plt
import numpy as np

for sample in ["airebo", "nnp"]:

    rdf= np.loadtxt("gr-%s.dat" % sample)
    plt.plot(rdf[:,0], rdf[:,1], label=sample.upper())

plt.title("T=300K", fontsize=13)
plt.ylabel("g(r) (Arbit. unit)", fontsize=13)
plt.xlabel("r ($\AA$)")
plt.xlim([2, 6])
plt.legend(fontsize=13)
plt.grid()
plt.tight_layout()
plt.savefig("rdf.png")
plt.show()