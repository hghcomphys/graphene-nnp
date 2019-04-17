#! /bin/csh

clear

rm -f *.out *.data
echo "Generating initial airebo dataset..."
lmp_serial < md.airebo.in #> md.airebo.out
cp airebo.data airebo0.data
# ----------------------------------------
#rm -f *.out 
#cp airebo0.data airebo.data


for i in $(seq 1 1 1)
do
	echo "Extending dataset... (step $i)"

	python lammps_to_runner.py airebo.data input.data

	echo "Using RuNNer..."
	cd nnp
	rm -f *.out *.data
	mv ../input.data .
	sh runscript.sh | tee runscript.out
	cd ..

	rm -f nnp.data

	echo "Running NNP-MD..."
	lmp_serial < md.nnp.in #> md.nnp.$i.out

	echo "Rerunning Airebo..."
	lmp_serial < rerun.airebo.in #> rerun.airebo.$i.out

	echo "---------------------------"
  
done



