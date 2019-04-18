#!/usr/bin/env bash

clear
echo
echo "Graphene-NNP"
echo "============================="

if [-z "$1"]
  then
   echo "Generating initial dataset..."
    rm -f lmp/*.out lmp/*.data
    lmp_serial < md.airebo.in > lmp/md.airebo.out
    cp lmp/airebo.data lmp/airebo0.data
    cp lmp/restart.data lmp/restart0.data
    python lammps_to_runner.py lmp/airebo.data lmp/input.data

    echo "RuNNer..."
    cd nnp
    rm -f *.out *.data
    mv ../lmp/input.data .
    sh runscript.sh > runscript.out
    cd ..
fi

for i in $(seq 1 1 2)
do
    echo "-----------------------------"
	echo "Extending dataset... ($i)"

    echo "Running MD using NNP..."
	rm -f lmp/nnp.data
	lmp_serial < md.nnp.in > lmp/md.nnp.$i.out

	echo "Rerunning using Airebo..."
	lmp_serial < rerun.airebo.in > lmp/rerun.airebo.$i.out
	python lammps_to_runner.py lmp/airebo.data lmp/input.data

	echo "RuNNer..."
	cd nnp
	rm -f *.out *.data
	mv ../lmp/input.data .
	sh runscript.sh > runscript.out
	cd ..
  
done



