MethodsArray=("bwts" "isbwt" "sabwt")

SequenceArray=(100 1000 10000 100000)

for i in "${MethodsArray[@]}"
do
    for j in "${SequenceArray[@]}"
    do
        echo "Running $i with sequence of length $j"
        mprof run -o "results/mprofrun_$i_$j.txt" python benchmark.py -m $i -s $j -r 1
    done
done