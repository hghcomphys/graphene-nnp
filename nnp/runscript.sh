#! /bin/csh

rm -f *.out

# convert input data to symmetry functions and split data into training and test set
cp input.nn-1 input.nn
RuNNer.serial.x | tee mode1.out

# run the fit
cp input.nn-2 input.nn
RuNNer.serial.x | tee mode2.out

# prepare fit for mode 3
cp optweights.006.out weights.006.data

# run prediction for first structure in input.data
#cp input.nn-3 input.nn
#RuNNer.serial.x | tee mode3.out

