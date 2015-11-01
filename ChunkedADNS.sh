#!/usr/bin/env bash

start_time=$(date +%s)
DATE=$(date +"%Y_%m_%d")

export LD_LIBRARY_PATH="/usr/local/lib"

printf "Make sure you're running this script within a tmux session. ADNS resolution takes a HUGE amount of time\n\nPress any key to continue"
read dummy


existing_output_chunk_list=( $(find temp/output/ -type f) )
existing_output_chunk_count=${#existing_output_chunk_list[*]}
#echo "CHUNK COUNT is $existing_output_chunk_count"

if [ $existing_output_chunk_count -eq 0  ]; then 	
	printf "\nEnter the chunk size that you want to use\nThe single input file will be split into multiple chunks, each having a number of lines = the chunk size that you specify.\nIt is recommended to not use a size above 10000\nENTER_CHUNK SIZE: "
	read chunk_size
else
	printf "\nThere are already some processed output chunk files present. "
	existing_chunk_size=$(cat ${existing_output_chunk_list[0]} | wc -l)
	printf "\nExisting chunk size was: "
	echo $existing_chunk_size

	printf "Setting current chunk size = $existing_chunk_size"
	chunk_size=$existing_chunk_size
fi

printf "\n\nEnter the relative or absolute file path of your Input File.\nThis file should have one domain name per line\nIMPORTANT: There is no validation on this input so make sure the file exists and its format is correct!\nENTER INPUT FILE PATH: "
read mega_input_file

printf "\nGenerating input file chunks in the temp/input/ directory...." 
split -l $chunk_size --numeric-suffixes $mega_input_file temp/input/input_
printf "Done\n\n"

input_chunk_directory="temp/input/"
for input_chunk_name in `ls temp/input | grep input_` 
do 
	input_chunk_path=$input_chunk_directory$input_chunk_name
	echo $input_chunk_path
	line_count=$(cat $input_chunk_path | wc -l)
	echo "Chunk Size = "$line_count
	printf "\n"
done


printf "\n\n-----------------------------------------\n"
printf "CHUNKED ADNS ACTIVITY LOGGER"
printf "\n-----------------------------------------\n"

count=0
for input_chunk_name in `ls temp/input | grep input_`
do
	input_chunk_path=$input_chunk_directory$input_chunk_name
	count=$((count+1))
    	if [ $count -eq 2 ]; then
        	wait
		printf "<----Wait---->\n"
		#sleep 3
        	count=1
	fi
	python ChunkedADNSResolver.py $input_chunk_path &   
done	
wait

printf "\n\n-----------------------------------------\n"
printf "COLLATING OUTPUT CHUNK FILES"
printf "\n-----------------------------------------\n"

FINAL_OUTPUT_FILE_PATH="results/ADNS_OUTPUT_$DATE.csv"
touch $FINAL_OUTPUT_FILE_PATH
output_chunk_directory="temp/output/"
for output_chunk_name in `ls temp/output`
do
        output_chunk_path=$output_chunk_directory$output_chunk_name
        cat $output_chunk_path >> $FINAL_OUTPUT_FILE_PATH
done
wait


printf "\n\n-----------------------------------------\n"
printf "CLEANING UP TEMPORARY FILES"
printf "\n-----------------------------------------\n"

rm temp/output/output_*
rm temp/input/input_*


end_time=$(date +%s)
printf "\n\n"
printf "Total Time Taken (in seconds) = "
echo "$(( ${end_time}-${start_time} ))s"

printf "\n\n---------------------------------------------------\n"
printf "THE CHUNKED ADNS BASH SCRIPT HAS FINISHED EXECUTING"
printf "\n---------------------------------------------------"

