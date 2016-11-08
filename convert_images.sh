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

get_vec() {
	python ./saturn/olivia/cli_vectorizer.py \
		--prm-name ~/SaturnServer/Googlenet_791113_192patch.prm \
		--image $1 
}

echo The dir is: $1

rm id_names.csv && true
touch id_names.csv
csv=vectors.csv
rm $csv && true
touch $csv

id=0
inc=100
for dir in $1/*; do 
	feature=$(echo $dir | sed 's,.*/,,g'); id=$((id+$inc))
	echo "${feature},${id}" >> id_names.csv
	echo "--[ ${feature} ]--"	
	
	for image in $dir/*; do
		vec=$(get_vec $image 2>/dev/null  | sed 's,\[,,g' | sed 's,\],,g' | sed "s,',,g")
		echo "${id},${vec}" >> $csv
		echo $image
	done	
done	


