
#!/bin/bash


base_directory="/home/aryagami/pract"
destination="/home/aryagami/nooo/archive.7z"

k=$(find $base_directory -type d -mtime -1 | sed 's|^/home/aryagami/pract/||' | tr '\n' ' ')

#echo $n
cd $base_directory || exit

7z a $destination $k



