from subprocess import Popen, PIPE


class Stego_module:
    def __init__(self, file_path, search=None, min_len=5):
        self.file_path = file_path
        self.search = search
        self.min_len = min_len
        self.found = False
        self.found_array = []
        self.usefull_urls = ["Stegdetect have more tools for stego(https://github.com/abeluck/stegdetect):\n\t./stegcompare orig.jpg modified.jpg\n\t./stegdeimage orig.jpg deimages.jpg\n\t./stegbreak [-V] [-r <rules>] [-f <wordlist>] [-t <schemes>] file.jpg ..."]
        self.output = []
        self.name = "Stego"


    def get_found(self):
        return self.found


    def get_found_array(self):
        return self.found_array

    
    def check_found(self, toCheck):
        if self.search in toCheck:
            self.found = True
            self.found_array.append(toCheck)
        return toCheck


    def print_found(self):
        for val in self.found_array:
            print val

    
    def execute(self): #This code is a modified version of the one found in https://github.com/ianare/exif-py/blob/develop/EXIF.py
        self._stegdetect_tool()
        self._zsteg_tool()


    def mprint(self):
        print "###### "+self.name+" ######"
        if self.usefull_urls:
            print "Usefull "+self.name+" URLS:"
            for val in self.usefull_urls:
                print val
            print
    
        for out in self.output:
            print out
        print "###### "+self.name+" END ######\n"


    def _stegdetect_tool(self):
        #Install help
        #sudo ln -s /usr/bin/automake /usr/bin/automake-1.14
        #sudo ln -s /usr/bin/aclocal /usr/bin/aclocal-1.14
        #Change Makefile.in and add "--add-missing" in AUTOMAKE_OPTIONS
        try:
            self.output.append("#### Stegdetect ####")
            self._execute_line("stegdetect "+self.file_path)
            self.output.append("#### Stegdetect End ####")
        except:
            self.output.append("Error: Do you have installed Stegdetect and in PATH? (https://github.com/abeluck/stegdetect)")
        

    def _zsteg_tool(self):
        try:
            self.output.append("#### Zsteg ####")
            self._execute_line("zsteg -a --no-color --min-str-len "+self.min_len+" "+self.file_path)
            self.output.append("#### Zsteg End ####")
        except:
            self.output.append("Error: Do you have installed Zsteg and in PATH? (https://github.com/zed-0xff/zsteg.git)")
        

    def _execute_line(self, cmd):
        pw = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        stdout,stderr = pw.communicate()
        for l in stdout.split("\n"):
            self._save_in_output(l)


    def _save_in_output(self, out):
        self.output.append(self.check_found(out))