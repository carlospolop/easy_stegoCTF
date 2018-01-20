# easy_stegoCTF

## USAGE:
```
python easy_stegoCTF.py -f <inputfile> -o <outputdirectory> [-s <String_to_search> [-g/--stego] [-m/--metadata] [-b/--binwalk] [-l/--lsb] [-t/--strings] [-x/--hexdump] [-e/--entropy] [-n/--noprint] [-r/--min-len <min_len_of_strings>]]

Extract all but hexdump and only a few strings: python easy_stegoCTF.py -f <inputfile> -o <outputdirectory>
Extract stego info: python easy_stegoCTF.py -f <inputfile> -o <outputdirectory> --stego
Extract hexdump and and strings (min length 5): python easy_stegoCTF.py -f <inputfile> -o <outputdirectory> --strings --min-len 5 --hexdump
```

## INSTALL:
You have to install the tools that you dont already have, in order to do that i recommend you to use the installation scripts of: https://github.com/DominicBreuker/stego-toolkit

## GENERAL FEATURES:
- [x] Automatically detects hidden files inside a file using "Binwalk".
- [x] Automatically detects metadata.
- [x] Automatically extracts strings.
- [x] Automatically checks the file using "File". 
- [x] Automatically extracts information of the file using "Identify".
- [x] Automatically extracts hidden files using "Foremost".
- [x] Automatically shows the entropy of the file using "Ent".
- [x] Automatically shows an hexdump.

## STEGO IN IMAGES:
- [x] Automatically check if the is information hidden in jpg by several algorithms using "StegDetect" (Algorithms: JSteg, Outguess, JPHide, Invisible Secrets, F5, Sophisticated F5, Append at the end)
- [x] Automatically check if is a real PNG file using "PNGCheck"
- [x] Automatically extract hidden information of a PNG using "ZSteg"
- [x] Automatically tries to extract information using "StegHide" without password
- [x] Automatically runs "StegoVeritas" with parameters: -imageTransform -colorMap -trailing, in order to stract possible hidden information.
- [x] Automatically tries to extract information using "JSteg" without password
- [x] Automatically tries to extract information using "Outguess" without password
- [x] Automatically tries to extract information using "Outguess-0.13" without password
- [x] Automatically tries to extract information using "OpenStego" without password
- [x] Automatically tries to extract information using "LSBSteg" without password
- [x] Automatically tries to extract information using "SteganoTool"
- [x] Automatically tries to bruteforce "StegHide" using the 500 most common passwords
- [x] Automatically tries to bruteforce "Outguess" using the 500 most common passwords
- [x] Automatically tries to bruteforce "Outguess-0.13" using the 500 most common passwords
- [x] Automatically extracts strings and create new images using the LSB.
