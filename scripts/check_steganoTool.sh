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


check_result_file() {
    if [ ! -f "$out_file" ]; then
      return
    fi

    SIZE=`stat -c %s "$out_file"`
    if [ ! "`file $out_file`" = "$out_file: data" ] && [ $SIZE -ge 1 ]; then
      echo ""
      echo -e "Found something!!!"
      echo "Result size: $SIZE (type: '`file $out_file`')"
    else
      echo "Some data found... Result size: $SIZE (type: '`file $out_file`')"
    fi
    rm $out_file
}

echo
echo "### stegano-lsb End ###"

for ENCODING in UTF-8 UTF-32LE; do
  echo "- stegano-lsb (encoding $ENCODING)"
  stegano-lsb reveal --input $in_file -e $ENCODING -o $out_file
  check_result_file $out_file
done

echo
echo "### stegano-lsb-set End ###"

# TODO: check why stegano is so buggy...
# - geneators not working: ackermann ackermann_naive (require arguments - how to parse?)

for GENERATOR in composite eratosthenes fermat fibonacci identity log_gen mersenne triangular_numbers; do
  # generator 'carmichael' left out since it is slow
  for ENCODING in UTF-8 UTF-32LE; do
    echo "- stegano-lsb-set (generator $GENERATOR | encoding $ENCODING)"
    stegano-lsb-set reveal --input $input_file -e $ENCODING -g $GENERATOR -o $out_file
    check_result_file $out_file
  done
done

echo
echo "### stegano-red ###"
stegano-red reveal --input $input_file
echo "### stegano-red End ###"