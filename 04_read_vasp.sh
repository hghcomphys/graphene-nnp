#!/usr/bin/env bash

REF="vasp"

rm -f ${REF}/input.data
echo removed ${REF}/input.data

for n in $(seq 1 1 300)
do
  # echo $n
  cp ${REF}/tmp/run$n/POSCAR .
  cp ${REF}/tmp/run$n/OUTCAR .

  python vasp_to_runner.py input.data
  cat input.data >> ${REF}/input.data
done
# echo number of sample: $n
rm -f input.data *CAR

echo "Done."
