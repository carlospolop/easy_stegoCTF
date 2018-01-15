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

#Chech if output is created and if it has something
check_result_file() {
    RESULT_FILE=$1
    PASS=$2
    if [ ! -f "$RESULT_FILE" ]; then
        return 0
    fi

    SIZE=`stat -c %s "$RESULT_FILE"`
    if [ ! "`file $RESULT_FILE`" = "$RESULT_FILE: data" ] && [ $SIZE -ge 1 ]; then
        echo ""
        echo "Cracked!! (openstego extract -p $PASS -sf $in_file -xf $out_file)"
        echo "Cracked file $in_file using password: $PASS"
        echo "The hidden data has been written to: $RESULT_FILE"
        echo "Result size: $SIZE (type: '`file $RESULT_FILE`')"
        echo "--------------"
        head -n 20 $RESULT_FILE
        echo ""
        echo "--------------"
        exit 0
    elif [ $SIZE -ge 1 ]; then
        echo "Something Found using pass: \"$PASS\" (openstego extract -p $pass -sf $in_file -xf $out_file)"
        echo "Result size: $SIZE (type: '`file $RESULT_FILE`')"
    fi
    rm $RESULT_FILE
    return 0
}

echo "Warning!! openstego is VERY SLOW..."
#Main
while read pass; do
    if (( verbose > 0 ));then 
        echo -en "$pass\r"
    fi
    openstego extract -p "$pass" -sf $in_file -xf $out_file > /dev/null 2>&1
    check_result_file $out_file $pass
done < $wordlist

echo "Nothing found, sry."
exit 1