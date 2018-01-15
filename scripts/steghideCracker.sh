#!/bin/bash

verbose=0
hlp_msg="$0 -i input_file [-v] -w wordlist -o out_file\n"
while getopts i:vhw:o: option
do
    case "${option}" in
        i) in_file=${OPTARG};;
        o) out_file=${OPTARG};;
        v) verbose=1;;
        h) echo -e $hlp_msg; exit;;
        w) wordlist=${OPTARG};;
    esac
done

#Check if input file setted
if [ -z ${in_file+x} ]; then 
    echo -e $hlp_msg
    exit
fi

#Check if out file setted
if [ -z ${out_file+x} ]; then 
    echo -e $hlp_msg
    exit
fi

#Check if input file exists
if [ ! -f $in_file ];then
    echo "Input file does not exist: $in_file"
    echo -e $hlp_msg
    exit
fi

#Check if wordlist file exists
if [ ! -f $wordlist ];then
    echo "Wordlist file does not exist: $in_file"
    echo -e $hlp_msg
    exit
fi

#Main
while read pass; do
    if (( verbose > 0 ));then 
        echo -en "$pass\r"
    fi
    if steghide extract -sf $1 -xf $out_file -p "$pass" -f > /dev/null 2>&1; then
        size=`stat -c %s "$out_file"`
        echo "Cracked!! (steghide extract -sf $1 -xf $out_file -p \"$pass\" -f)"
        echo "Cracked file $in_file using password: $pass"
        echo "The hidden data has been written to: $outfile"
        echo "Result size: $size (type: '`file $out_file`')"
        echo "--------------"
        head -n 20 $out_file
        echo ""
        echo "--------------"
        exit 0
    fi
done < $wordlist

echo "Nothing found, sry."
exit 1