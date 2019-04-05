"""A simple adaptor for RuNNer io file formats"""


class AtomicData:
    """A class that holds atomic data such as positions, forces, total_energy, charges, etc."""
    def __init__(self, position=(0.0, 0.0, 0.0), symbol='X', charge=0.0, energy=0.0, force=(0.0, 0.0, 0.0)):
        self.position= position
        self.symbol = symbol
        self.charge = charge
        self.energy = energy
        self.force = force


class CollectiveData:
    """A class that holds collective quantities of simulated system such as total energy or charge."""
    def __init__(self, box=(0.0, 0.0, 0.0), total_energy=0.0, total_charge=0.0):
            self.box = box
            self.total_energy = total_energy
            self.total_charge = total_charge


class Sample:
    """ A class that holds a list of atomic data and also collective data for a single sample."""

    def __init__(self):
        self.atomic = []
        self.collective = None

    @property
    def number_of_atoms(self):
        return len(self.atomic)


class DataSet:
    """This class holds a collection of samples."""

    def __init__(self):
        self.samples = []

    def append(self, sample):
        """Append a sample to list of samples."""
        self.samples.append(sample)

    @property
    def number_of_samples(self):
        return len(self.samples)


class RunnerAdaptor:
    """A bas class for conversion file formats of RuNNer package."""

    def __init__(self):
        self.dataset = DataSet()

    def read_runner(self, filename):
        """Read RuNNer data format."""
        pass

    def write_runner(self, filename):
        """Write RuNNer input data."""
        with open(filename, "w") as out_file:
            # loop over samples
            for sample in self.dataset.samples:
                out_file.write("begin\n")
                out_file.write("lattice %f %f %f\n" % (sample.collective.box[0], 0.0, 0.0))
                out_file.write("lattice %f %f %f\n" % (0.0, sample.collective.box[1], 0.0))
                out_file.write("lattice %f %f %f\n" % (0.0, 0.0, sample.collective.box[2]))
                # loop over atoms in a sample
                for atom in sample.atomic:
                    out_file.write("atom ")
                    out_file.write("%f %f %f " % atom.position)
                    out_file.write("%s %f %f " % (atom.symbol, atom.charge, atom.energy))
                    out_file.write("%f %f %f\n" % atom.force)
                out_file.write("energy %f\n" % sample.collective.total_energy)
                out_file.write("charge %f\n" % sample.collective.total_charge)
                out_file.write("end\n")
        return self


class RuNNerAdaptorLAMMPS(RunnerAdaptor):
    """A inherited class for conversion file formats between RuNNer and LAMMPS packages."""

    def __init__(self):
        RunnerAdaptor.__init__(self)

    def read_lammps(self, filename, symbol_dict=None):

        with open(filename, 'r') as in_file:
            # loop over lines in file
            for line in in_file:

                # create a instance of sample data
                sample = Sample()

                # number of steps
                line = next(in_file)
                steps = int(line.split()[0])
                # number of atoms
                line = next(in_file)
                line = next(in_file)
                number_of_atoms = int(line.split()[0])
                # read box sizes, TODO: only orthogonal box
                box = []
                line = next(in_file)
                for n in range(3):
                    line = next(in_file)
                    line = line.rstrip("/n").split()
                    box.append(float(line[1]) - float(line[0]))
                # set collective data
                sample.collective = CollectiveData(tuple(box))

                # read atomic positions, symbol, charge, forces, energy, etc.
                line = next(in_file)
                for n in range(number_of_atoms):
                    line = next(in_file).rstrip("/n").split()
                    position = (float(line[0]), float(line[1]), float(line[2]))
                    symbol = line[3]
                    charge = float(line[4])
                    energy = float(line[5])
                    force = (float(line[6]), float(line[7]), float(line[8]))
                    # convert number to an atomic symbol
                    if symbol_dict is not None:
                        symbol = symbol_dict[symbol]
                    # create atomic data and append it to sample
                    sample.atomic.append(AtomicData(position, symbol, charge, energy, force))

                # add sample to DataSet (list of samples)
                self.dataset.append(sample)
        return self





# lammps_filename="dump.airebo.data", runner_filename="input.nn"

if __name__ == "__main__":

    data = RuNNerAdaptorLAMMPS().read_lammps("dataset/dump.airebo.data", {'1': 'O'})
    print ("number of samples:", data.dataset.number_of_samples)
    print ("number of atoms in each sample:", data.dataset.samples[0].number_of_atoms)
    data.write_runner("dataset/input.data")
