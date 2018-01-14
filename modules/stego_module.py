from subprocess import Popen, PIPE


class Stego_module:
    def __init__(self, file_path, search=None, min_len=5, try_all=True, try_stego=False, try_hexdump=False, try_entropy=False):
        self.file_path = file_path
        self.search = search
        self.min_len = min_len
        self.found = False
        self.found_array = []
        self.usefull_urls = []
        self.output = []
        self.name = "Stego"
        self.try_all, self.try_stego, self.try_hexdump, self.try_entropy = try_all, try_stego, try_hexdump, try_entropy



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
        if (self.try_all or self.try_stego):
            self._stegdetect_tool()
            self._zsteg_tool()
            self._stegcracker_tool()

        if (self.try_all or self.try_hexdump):
            self._hexdump_tool()

        
        if (self.try_all or self.try_entropy):
            self._ent_tool()

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
            line = ["stegdetect", self.file_path]
            self.output.append("#### Stegdetect ####")
            self._execute_line(line)
            self.output.append("#### Stegdetect End ####\n")
        except Exception as e:
            self.output.append("Error: Do you have installed Stegdetect and in PATH? (https://github.com/abeluck/stegdetect)")
            self.output.append(e)


    def _zsteg_tool(self):
        try:
            line = ["zsteg", "-a", "--min-str-len", str(self.min_len), self.file_path]
            self.output.append("#### Zsteg ####")
            self._execute_line(line)
            self.output.append("#### Zsteg End ####")
        except Exception as e:
            self.output.append("Error: Do you have installed Zsteg and in PATH? (https://github.com/zed-0xff/zsteg.git)")
            self.output.append(e)

    
    def _stegcracker_tool(self):
        try:
            line = ["stegcracker", self.file_path, "stegcracker_dict.txt"]
            self.output.append("#### StegCracker ####")
            self._execute_line(line)
            self.output.append("#### StegCracker End ####")
        except Exception as e:
            self.output.append("Error: Do you have installed StegCracker and StegHide and in PATH? (https://github.com/Paradoxis/StegCracker.git)")
            self.output.append(e)

    
    def _hexdump_tool(self):
        try:
            line = ["hexdump", "-C", self.file_path]
            self.output.append("#### Entropy(ent) ####")
            self._execute_line(line)
            self.output.append("#### Hexdump End ####")
        except Exception as e:
            self.output.append("Error: Do you have installed hexdump and in PATH?")
            self.output.append(e)


    def _ent_tool(self):
        try:
            line = ["ent", self.file_path]
            self.output.append("#### Entropy(ent) ####")
            self._execute_line(line)
            self.output.append("#### Entropy End ####")
        except Exception as e:
            self.output.append("Error: Do you have installed ent and in PATH?")
            self.output.append(e)


    def _execute_line(self, cmd):
        pw = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout,stderr = pw.communicate()
        if "zsteg" in cmd: 
            if "nothing" in stdout:
                self.output.append("[=] nothing :(")
                return
            for l in stdout.split("\n"):
                ls = l.split()
                str_to_save = []
                for s in l[::-1]:
                    str_to_save.insert(0,s)
                    if "\r" in s:
                        self._save_in_output("".join(str_to_save))
                        break
                     
        elif "stegcracker" in cmd:
            if "Failed to crack file" in stdout:
                self.output.append("Nothing detected with stegcracker:(")
                return
            for l in stdout.split("\n"):
                self.output.append("Cracked !!!!")
                if "Successfully cracked" in l:
                    self.output.append(l)

        else:
            for l in stdout.split("\n"):
                self._save_in_output(l)


    def _save_in_output(self, out):
        self.output.append(self.check_found(out))