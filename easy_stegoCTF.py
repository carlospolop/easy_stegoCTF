#!/usr/bin/python
import sys, os, getopt

from modules import Exif_module, Strings_module, Stego_module, LSB_module, Binwalk_module


def main(argv):
    hlp = "-f <inputfile> -o <outputdirectory> [-s <String_to_search> [-g/--stego] [-m/--metadata] [-b/--binwalk] [-l/--lsb] [-t/--strings] [-x/--hexdump] [-n/--noprint] [-r/--min-len <min_len_of_strings>]]"
    try:
        opts, args = getopt.getopt(argv,"hf:o:s:gmbltxnr:",["help","ifile=","odir=","search=","stego","metadata","binwalk","lsb","strings","hexdump","noprint","min-len="])
    except getopt.GetoptError:
        print hlp
        sys.exit(2)

    general_urls = ["HexEditor: https://www.onlinehexeditor.com/","Steganographic Decoder: https://futureboy.us/stegano/decinput.html", "Find hidden images inside images: http://magiceye.ecksdee.co.uk/", "Fourier Transform: http://www.ejectamenta.com/Imaging-Experiments/fourierimagefiltering.html","PDF extractor: http://www.extractpdf.com/", "Gif frame extractor: https://ezgif.com/split", "Lector QR: http://qrlogo.kaarposoft.dk/qrdecode.html", "DTMF Tones: http://dialabc.com/sound/detect/index.html"]
    stego_tools = ["StegSecret(GUI): http://stegsecret.sourceforge.net/","StegSolve(GUI): www.caesum.com/handbook/Stegsolve.jar","Steganabara(GUI): https://github.com/zardus/ctf-tools","Zsteg: https://github.com/zed-0xff/zsteg.git","StegDetect: https://github.com/abeluck/stegdetect","Binwalk: https://github.com/ReFirmLabs/binwalk", "Exif-py: https://github.com/ianare/exif-py"]
    search, out_dir, min_len = "", "", 5
    try_all, print_each, try_stego, try_exif, try_binwalk, try_lsb, try_strings, try_hexdump = True, True, False, False, False, False, False, False

    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit()

        elif opt in ("-f", "--ifile"):
            inputfile = arg
            filename = inputfile.split("/")[-1]
            if (not os.path.isfile(inputfile)):
                print "Not a file: "+filename
                sys.exit(-1)

        elif opt in ("-o","--odir"):
            if(os.path.isdir(arg)):
                out_dir = arg
            else:
                print "Not a directory: "+out_dir
                sys.exit(-1)

        elif opt in ("-g","--stego"):
            try_all = False
            try_stego = True

        elif opt in ("-m","--metadata"):
            try_all = False
            try_exif = True

        elif opt in ("-b","--binwalk"):
            try_all = False
            try_binwalk = True

        elif opt in ("-l","--lsb"):
            try_all = False
            try_lsb = True

        elif opt in ("-t","--strings"):
            try_all = False
            try_strings = True
        
        elif opt in ("-x","--hexdump"):
            try_hexdump = True

        elif opt in ("-s", "--search"):
            search = arg
        
        elif opt in ("-n", "--noprint"):
            print_each = False

        elif opt in ("-r","--min-len"):
            min_len = int(arg)

    if not out_dir or not inputfile:
        print "No out directory"
        print hlp    
        sys.exit()


    print "File input: "+filename+"\n"


    # Binwalk MODULE
    bwlk = Binwalk_module(inputfile, out_dir, try_hexdump, search)
    if (try_all or try_binwalk):
        bwlk.execute()

    # Exif MODULE
    exif = Exif_module(inputfile, search)
    if (try_all or try_exif):
        exif.execute()

    # Strings MODULE
    strings = Strings_module(inputfile, search, min_len)
    if (try_all or try_strings):
        strings.execute()

    # Stego MODULE
    stego = Stego_module(inputfile, search)
    if (try_all or try_stego):
        stego.execute()

    # LSB MODULE
    lsb = LSB_module(inputfile, out_dir, search, min_len)
    if (try_all or try_lsb):
        lsb.execute()



    ######## Print output #########
    print "###### General Usefull URLs ######"
    for url in general_urls:
        print url
    for tool in stego_tools:
        print tool
    print "###### End URLs ######"

    #Search MODULE
    if search != "":
        print "###### Search ######"
        if bwlk.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN BINWALK"
            bwlk.print_found()
        
        if exif.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN EXIF"
            exif.print_found()

        if exif.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN STRINGS"
            strings.print_found()

        if stego.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN STEGO"
            stego.print_found()

        if lsb.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN LSB"
            lsb.print_found()

        print "###### End Search ######"
        print


    if print_each:
        bwlk.mprint()
        exif.mprint()
        strings.mprint()
        stego.mprint()
        lsb.mprint()


if __name__ == "__main__":
   main(sys.argv[1:])