#!/bin/bash

exec &>> /home/ubuntu/xtra_back/vip_line_backup.log

[ $(which xtrabackup > /dev/null 2>&1; echo ${?}) -ne 0 ] && { echo -e "\npercona-xtrabackup is required...exiting"; exit 1; };

set -x # Enable Debug
set -e  # stops execution if a variable is not set
set -u  # stop execution if something goes wrong

# Custom Variables
weeks=4;											# Number of weeks to backup to keep
backupDirectory=/data/backup/vip_line1;		# Backup Directory
dataDirectory=/var/lib/mysql;						# MySQL Database Location
# userArguments="--user=root --password=ckompare --host=localhost --port=3306";	# MySQL Username & Password
# userArguments="--user=billing --password=Baiqu3lich --host=172.21.16.42 --port=3306";
usage() {
	echo -e "\nusage: $(dirname $0)/$(basename $0) {full|incremental|pack|unpack|restore|help}";
	echo;
	echo -e "full:\t\tCreate a full backup of vip_line /var/lib/mysql using xtrabackup.";
	echo -e "incremental:\tCreate an incremental backup";
	echo -e "pack:\tconverting backups into tar files";
	echo -e "unpack:\tconverting tar files into normal files";
	echo -e "restore:\tRestore the latest backup to Galera Cluster, BE CAREFUL!";
	echo -e "help:\t\tShow this help";
}

full() {
	date;
	if [ ! -d ${backupDirectory} ]; then
		echo "ERROR: the folder ${backupDirectory} does not exists";
		exit 1;
	fi;
	echo "doing full backup...";
	echo "cleaning the backup folder...";

	if [ ${weeks} -gt 1 ]; then
		[ -d "${backupDirectory}/${weeks}" ] && rm -fr ${backupDirectory}/${weeks};
		for (( i = ${weeks}; i > 1; i-- ))
		{
			[ -d "${backupDirectory}/$((${i} - 1))" ] && mv -f ${backupDirectory}/$((${i} - 1)) ${backupDirectory}/${i};
		}
		mkdir -p ${backupDirectory}/1;
	fi;
	echo "cleaning done!";
    xtrabackup ${ARGS} --backup --target-dir=${backupDirectory}/1/FULL;
	date;
	echo "backup done!";
}

incremental() {
	if [ ! -d ${backupDirectory}/1/FULL ]; then
		echo "ERROR: no full backup has been done before. aborting";
		exit -1;
	fi;

	#we need the incremental number
	if [ ! -f ${backupDirectory}/1/last_incremental_number ]; then
		NUMBER=1;
	else
		NUMBER=$(($(cat ${backupDirectory}/1/last_incremental_number) + 1));
	fi;
	date;
	echo "doing incremental number ${NUMBER}";
	if [ ${NUMBER} -eq 1 ]; then
        xtrabackup ${ARGS} --backup --incremental-basedir=${backupDirectory}/1/FULL --target-dir=${backupDirectory}/1/inc${NUMBER};
    else
		xtrabackup ${ARGS} --backup --incremental-basedir=${backupDirectory}/1/inc$((${NUMBER} - 1)) --target-dir=${backupDirectory}/1/inc${NUMBER};
	fi;
	date;
	echo ${NUMBER} > ${backupDirectory}/1/last_incremental_number;
	echo "incremental ${NUMBER} done!";
}

# Function to create a tar file of the entire backup directory
pack() {
    # Loop through subdirectories in the backup directory
    for subdirectory in "$backupDirectory"/*; do
        if [ -d "$subdirectory" ]; then
            # Get the subdirectory name without the full path
            subdirectoryName=$(basename "$subdirectory")

            # Create a tar.gz file for the subdirectory
            tarFilename="${backupDirectory}/${subdirectoryName}.tar.gz"
            tar -czvf "$tarFilename" -C "$backupDirectory" "$subdirectoryName"

            echo "Tar file created: $tarFilename"
        fi
    done
}


unpack() {
    # Loop through subdirectories in the backup directory
    for tarFile in "$backupDirectory"/*.tar.gz; do
        if [ -f "$tarFile" ]; then

            # Create a subdirectory to extract the contents
            extractionDirectory="$backupDirectory/"
            mkdir -p "$extractionDirectory"

            # Extract the contents of the tar.gz file
            tar -xzvf "$tarFile" -C "$extractionDirectory"

            echo "Uncompressed files from: $tarFile to $extractionDirectory"
        fi
    done
}

restore() {
    echo "WARNING: if you have runned PACK function then you need to choose yes to run UNPACK function before running RESTORE function? (Enter 1 or 2)";
	select yn in "Yes" "No"; do
		case $yn in
			Yes )
                unpack
				break
			;;
			No )
				break
			;;
		esac
	done;


	[ `pidof -x mysqld > /dev/null 2>&1; echo ${?}` -eq 0 ] && ( echo "MySQL Daemon is currently running, stop the mysqld service & try again..."; exit 1; );
	echo "WARNING: are you sure this is what you want to do? (Enter 1 or 2)";
	select yn in "Yes" "No"; do
		case $yn in
			Yes )
				break
			;;
			No )
				echo "aborting...";
				exit;
			;;
		esac
	done;

    echo "making prepare"
	xtrabackup --prepare --apply-log-only --use-memory=1G --target-dir=${backupDirectory}/1/FULL;
	echo "preparation done!";

	date;
	echo "doing restore...";

	# Appending all the increments
	P=1;
	while [ -d ${backupDirectory}/1/inc${P} ] && [ -d ${backupDirectory}/1/inc$((${P}+1)) ]; do
		echo "processing incremental ${P}";
		xtrabackup --prepare --apply-log-only --use-memory=1G --target-dir=${backupDirectory}/1/FULL --incremental-dir=${backupDirectory}/1/inc${P};
		P=$((${P}+1));
	done;

	if [ -d ${backupDirectory}/1/inc${P} ]; then
		echo "processing last incremental ${P}";
		xtrabackup --prepare --apply-log-only --use-memory=1G --target-dir=${backupDirectory}/1/FULL --incremental-dir=${backupDirectory}/1/inc${P};
	fi;

	# Preparing the full backup
	xtrabackup --prepare --apply-log-only --use-memory=1G --target-dir=${backupDirectory}/1/FULL;

	#finally we copy the folder
	cp -r ${dataDirectory} ${dataDirectory}.back;
    cp -r "${backupDirectory}/1/FULL"/* "/var/lib/mysql"
	chown -R mysql:mysql ${dataDirectory};
}




ARGS="--user=billing --password=Baiqu3lich --host=172.21.16.42 --port=3306 --backup";
[ ! -d "${backupDirectory}" ] && mkdir -p ${backupDirectory};

if [ $# -eq 0 ]; then
	usage;
	exit 1;
fi;

case $1 in
	"full")
		full;
	;;
	"incremental")
		curr_hour=$(date +"%H")
		curr_min=$(date +"%M")
		if [ "$curr_hour" == "00" ] && [ "$curr_min" == "00" ]; then
			echo "there is no need to take incremental at this time we are taking full backup"
		else
			incremental;
		fi
	;;
	"restore")
		restore;
	;;
	"pack")
		pack;
	;;
    "help")
		usage;
	;;
	*)
		echo "invalid option";
	;;
esac
