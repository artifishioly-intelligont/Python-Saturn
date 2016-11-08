#!/bin/bash

# Arg1 ($1) is the folder containing all the folders with images
# e.g. expected folder layout:
#  
# $1
#  |-trees
#  |	|-img1.jpg
#  |	|-img2.jpg
#  |	|-..etc..
#  |-ponds
#  |	|-img1.jpg
#  |	|-img2.jpg
#  |	|-..etc..
#  |-houses
#  |	|-img1.jpg
#  |	|-img2.jpg
#  |	|-..etc..
#  |..etc..
#
#

# Ensure that the script is being run in the correct folder
if  [ -f ./install.sh  ]; then
	echo "Script running in correct location: ${PWD}."
else
	echo "Script running in incorrect ${PWD}, this is the incorrect folder."
	echo "Run this script when the pwd is the git repo"
	exit -1
fi

# Run the vectorizer and return the attr vec
get_vec() {
	python ./saturn/olivia/cli_vectorizer.py \
		--prm-name ~/SaturnServer/Googlenet_791113_192patch.prm \
		--image $1 
}

echo The dir is: $1

# Set up the files for logging
rm id_names.csv && true
touch id_names.csv
csv=vectors.csv
rm $csv && true
touch $csv


# Fix the location path where we are looking for files (ensure that the content var ends in /* not //*)
last_char=${#1}-1
if [ "${1:last_char}" == "/"  ];then
	content=$1*
	echo 'ends in /'
else
	content=$1/*
	echo 'doesnt end in /'
fi

# Determine the number of files to process
files=$(find $content -type f | wc -l)
echo "There are ${files} files to process"

filecount=1
id=0
inc=100
for dir in $content; do 
	feature=$(echo $dir | sed 's,.*/,,g'); id=$((id+$inc))
	echo "${feature},${id}" >> id_names.csv
	echo "--[ ${feature} ]--"	
	
	for image in $dir/*; do
		vec=$(get_vec $image 2>/dev/null  | sed 's,\[,,g' | sed 's,\],,g' | sed "s,',,g")
		echo "${id},${vec}" >> $csv
		echo $filecount/$files:  $image
		filecount=$(($filecount+1))
	done	
done	


