# ICE (Intelligent Course Enrollment)
## _The Best Course Scheduling Software, Ever_

ICE is a course-scheduling software that uses Greedy Algorithm to solve the Registrar's Problem

## Note about `isValid.pl`:
Our `test.py` script (can be found in `~/Algorithm`) has a function called `test` that contains the transcribed functions of `isValid.pl` and it evaluates the validity and performance of the schedule the exact same way. Our algorithm uses this python script to initiate the scheduling process and evaluate the output of the scheduling process. 

## To run it on all of Bryn Mawr's data

1. Navigate to `~/Algorithm` and run the following command

```sh
python3 test.py -f ../data/parsed_data/ -s ../data/schedule_real.txt -a
```

To enable or disable constraints for the scheduling process, navigate to `~/Algorithm/main.py` and change the default keyword argument values for the constraint of interest. This would toggle the constraint and allow the algorithm to run with or without the constraint.

## To run it on random generated data

1. Checkout the `without-constraints` branch from the Github Repository
2. Navigate to `~/Algorithm/misc` and run `bash generateRandomInstances2.sh [instances] [rooms] [classes] [times] [students]` to generate folder with test cases
2. Move the entire folder with test cases into `~/Algorithm/misc/test_cases`
2. Navigate to `~/Algorithm` and run the following command

```sh
python3 test.py -a
```


