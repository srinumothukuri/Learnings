
#!/bin/bash

read -p"Enter file name:" file

touch $file
filename=$file
datetime=$(date +%Y-%m-%d_%H-%M-%S)
new_file=$filename"_"$datetime.txt
cp $filename $new_file
rm $filename

#echo "CREATE TABLE employee(sno INT(10),Name VARCHAR(255),Age INT(10));">>$new_file

#sudo mysql -u"srinivas" -p"Bulzer220" -D"srinivas" </home/aryagami/pract/$new_file

sudo mysqldump -u"srinivas" -p"Bulzer220" srinivas > /home/aryagami/pract/$new_file
