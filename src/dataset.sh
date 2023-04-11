#cd /Users/ardatezcan/Downloads/deneme/deneme

#the dataset path
cd /data/scratch/bariskurtkaya/oxford/2014-12-16-18-44-24/stereo/centre/

#the path as the same with this sh
ls -1 > /home/bariskurtkaya/github/DL-DAS/src/files.txt

declare -i x=1

#the path as the same with this sh
input="/home/bariskurtkaya/github/DL-DAS/src/files.txt"
while IFS= read -r line
do
    if [[ "$x" -eq "8" ]]
    then
      declare -i x=1
    else
       x=$((x+1))
       rm -rf /data/scratch/bariskurtkaya/oxford/2014-12-16-18-44-24/stereo/centre/$line #the dataset path before "$line" 
    fi
done < "$input"