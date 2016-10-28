#!/bin/bash


# Description:
#	Runs all the python unit tests (given they start with 'test__', naming convention underneath)
# 
# Test Naming Convention:
# 	A test for a .py file must start with 'test__' followed by the name of the .py file.
#	It must also be in the same directory as the python file under test.
#	e.g. 
#		a test for 'Perceptron.py' would be named 'test__Perceptron.py'
# Usage:
# 	Will search current directory and sub directories for tests.
#	
# 	$./run_tests.sh
#

echo '=============================================================='
echo '	                  run_tests.sh'
echo '=============================================================='
echo '--------------------------------------------------------------'
echo '                 Searching for tests'
echo '--------------------------------------------------------------'
echo "Searching for tests in ${PWD}"
echo ''

tests=$(find . -name test__*.py)

if [[ -z $tests ]]; then
	echo 'No tests found, exiting.'
	exit 0
fi 

echo 'Tests found:'
for test in $tests; do 
	echo $test
done
echo; echo;


echo '--------------------------------------------------------------'
echo '                 Setting up log'
echo '--------------------------------------------------------------'
rm passed_tests.log && true
 touch passed_tests.log
echo "Created ./passed_tests.log"

rm failed_tests.log && true
 touch failed_tests.log
echo "Created ./failed_tests.log"
echo; echo;

for test in $tests; do
	echo '--------------------------------------------------------------'
	echo "     test: ${test}"
	echo '--------------------------------------------------------------'
	python $test

	# If the test failed
	if [ $? -ne 0 ]; then
		echo $test >> failed_tests.log
	else
		echo $test >> passed_tests.log
	fi	
done


echo '--------------------------------------------------------------'
echo '                 Results'
echo '--------------------------------------------------------------'
echo ' Passed Tests:'
cat ./passed_tests.log
echo;
echo ' Failed Tests:'
cat ./failed_tests.log

# If any tests failed then this script will exit with a fail exit code
#	a pass code is exit code 0
#	a fail code is any non-zero number 
if [ -s ./failed_tests.log ];then
	echo;
	echo '=============================================================='
	echo '	    		    FAILED'
	echo '=============================================================='
	echo 'At least one failed test, entire test failed'
	exit -1
else
	
	echo '=============================================================='
	echo '	    		    PASSED'
	echo '=============================================================='
	echo 'All tests passed'
fi

