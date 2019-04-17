#! /bin/csh

clear

echo "Generating initial airebo dataset..."
rm -f lmp/*.out lmp/*.data
lmp_serial < md.airebo.in #> md.airebo.out
cp lmp/airebo.data lmp/airebo0.data
# ----------------------------------------
#rm -f lmp/*.out 
#cp lmp/airebo0.data lmp/airebo.data


for i in $(seq 1 1 3)
do
	echo "---------------------------"
	echo "Extending dataset... (step $i)"

	python lammps_to_runner.py lmp/airebo.data lmp/input.data

	echo "Using RuNNer..."
	cd nnp
	rm -f *.out *.data
	mv ../lmp/input.data .
	sh runscript.sh #| tee runscript.out
	cd ..

	echo "Running MD using NNP..."
	rm -f lmp/nnp.data
	lmp_serial < md.nnp.in #> md.nnp.$i.out

	echo "Rerunning Airebo..."
	lmp_serial < rerun.airebo.in #> rerun.airebo.$i.out
  
done



