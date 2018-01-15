import os
from subprocess import Popen, PIPE


class Stego_module:
    def __init__(self, file_path, out_dir, search=None, min_len=5, try_all=True, try_stego=False, try_hexdump=False, try_entropy=False):
        self.file_path = file_path
        self.out_dir = out_dir
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


    def _check_file(self, path, cmd):
        if os.path.isfile(path):
            if os.path.getsize(path) > 1:
                pw = Popen(["file", path], stdout=PIPE, stderr=PIPE, shell=shell)
                stdout,stderr = pw.communicate()
                if not "data" in stdout:
                    self.output.append("CRACKED!! ("+cmd+")")

    
    def execute(self): #This code is a modified version of the one found in https://github.com/ianare/exif-py/blob/develop/EXIF.py
        if (self.try_all or self.try_stego):
            #Generals
            self._execute_tool("File", ["file", self.file_path])
            self._execute_tool("Identify", ["identify", "-verbose", self.file_path])
            self._execute_tool("Exiftool", ["exiftool", self.file_path])
            self._execute_tool("Binwalk", ["binwalk", self.file_path])
            self._execute_tool("Foremost", ["foremost", "-o", self.out_dir, "-i", self.file_path])
            self._execute_tool("Strings (head 20)", "strings -n "+str(self.min_len)+" "+self.file_path+" | head -n 20")
            self.output.append("[......]")
            self._execute_tool("Strings (tail 20)", "strings -n "+str(self.min_len)+" "+self.file_path+" | tail -n 20")           

            #Stego
            for t,name in zip(["j", "o", "p", "i", "f", "F", "a"],["JSteg", "Outguess", "JPHide", "Invisible secrets", "F5", "Sophisticated F5", "At end of file (camouflage or appendX)"]):
                self._execute_tool("StegDetect -t "+t+" ("+name+")", ["stegdetect", "-t", t, self.file_path]) #https://github.com/abeluck/stegdetect
            
            self._execute_tool("PngCheck", ["pngcheck", self.file_path])
            self._execute_tool("ZSteg", ["zsteg", "-a", "--min-str-len", str(self.min_len), self.file_path]) #https://github.com/zed-0xff/zsteg.git
            self._execute_tool("StegHide", ["StegHide", "extract", "-sf", self.file_path, "-p", '""'])
            self._execute_tool("StegoVeritas", ["stegoveritas.py", self.file_path, "-outDir", self.out_dir, "-imageTransform", "-colorMap", "-trailing"])

            path_jsteg_out = self.out_dir+"/jstegOUT"
            self._execute_tool("Jsteg", ["jsteg", "reveal", self.file_path, path_jsteg_out])
            self._check_file(path_jsteg_out, "jsteg reveal "+self.file_path+ " " +path_jsteg_out)

            path_outguess_out = self.out_dir+"/outguessOUT"
            self._execute_tool("Outguess", ["outguess", "-r", self.file_path, path_outguess_out])
            self._check_file(path_outguess_out, "outguess -r "+self.file_path+ " " +path_jsteg_out)
            
            path_outguess013_out = self.out_dir+"/outguessOUT-013"
            self._execute_tool("Outguess-0.13", ["outguess-0.13", "-r", self.file_path, path_outguess013_out])
            self._check_file(path_outguess013_out, "outguess-0.13 -r "+self.file_path+ " " +path_jsteg_out)

            path_openstego_out = self.out_dir+"/openstego"
            self._execute_tool("OpenStego", "echo -e \"\\n\" | openstego extract -sf "+self.file_pat+" -xf "+path_openstego_out, True)
            self._check_file(path_openstego_out, "openstego extract -sf "+self.file_pat+" -xf "+path_openstego_out)

            path_lsbsteg_out = self.out_dir+"/lsbsteg"
            self._execute_tool("LSBSteg", ["lsbsteg", "decode", "-i", self.file_path, "-o", path_lsbsteg_out])
            self._check_file(path_lsbsteg_out, "lsbsteg decode -i "+self.file_path+ " " +path_jsteg_out)

            #Crackers
            absPath = os.path.realpath(__file__)
            wordlist = absPath + "/../stegocracker_dict.txt"

            steghideCracker = absPath + "/../scripts/steghideCracker.sh"
            steghideCracker_out = self.out_dir+"/stegCracker"
            self._execute_tool("StegCracker", [steghideCracker, "-i", self.file_path, "-w", wordlist, "-o", steghideCracker_out])

            outguessCracker = absPath + "/../scripts/outguessCracker.sh"
            outguessCracker_out = self.out_dir+"/outguess"
            self._execute_tool("OutguessCracker", [outguessCracker, "-i", self.file_path, "-w", wordlist, "-o", outguessCracker_out])

            outguess013Cracker = absPath + "/../scripts/outguess013Cracker.sh"
            outguess013Cracker_out = self.out_dir+"/outguess013"
            self._execute_tool("Outguess013Cracker", [outguess013Cracker, "-i", self.file_path, "-w", wordlist, "-o", outguess013Cracker_out])

            steganoTool = absPath + "/../scripts/check_steganoTool.sh"
            steganoTool_out = self.out_dir+"/steganoTool"
            self._execute_tool("SteganoTool", [steganoTool, "-i", self.file_path, "-w", wordlist, "-o", steganoTool_out])

            #jphideCracker = absPath + "/../scripts/jphideCracker.sh" #Need to fix!!
            #jphideCracker_out = self.out_dir+"/jphide"
            #self._execute_tool("JPHide", [jphideCracker, "-i", self.file_path, "-w", wordlist, "-o", jphideCracker_out])

            #cloackedpixelCracker = absPath + "/../scripts/cloackedpixelCracker.sh" #Very slow!!
            #cloackedpixelCracker_out = self.out_dir+"/loackedpixel"
            #self._execute_tool("CloackedpixelCracker", [cloackedpixelCracker, "-i", self.file_path, "-w", wordlist, "-o", cloackedpixelCracker_out])

            #openstegoCracker = absPath + "/../scripts/openstegoCracker.sh" #Very slow!!
            #openstegoCracker_out = self.out_dir+"/openstego"
            #self._execute_tool("OpenstegoCracker", [openstegoCracker, "-i", self.file_path, "-w", wordlist, "-o", openstegoCracker_out])

        if (self.try_hexdump):
            self._execute_tool("HexDump", ["hexdump", "-C", self.file_path])

        
        if (self.try_all or self.try_entropy):
            self._execute_tool("Ent", ["ent", self.file_path])


    def mprint(self):
        if len(self.output) > 0:
            print "###### "+self.name+" ######"
            if self.usefull_urls:
                print "Usefull "+self.name+" URLS:"
                for val in self.usefull_urls:
                    print val
                print
        
            for out in self.output:
                print out
            print "###### "+self.name+" END ######\n"


    def _execute_tool(self, name, line):
        try:
            self.output.append("#### "+name+" ####")
            self._execute_line(line)
            self.output.append("#### "+name+" End ####\n")
        except Exception as e:
            self.output.append("Error: Do you have installed "+name+" and in PATH?")
            self.output.append(e)


    def _execute_line(self, cmd, shell=False):
        pw = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell)
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

        elif "jsteg" in cmd:
            if (("invalid JPEG" in stdout) or ("not contain hidden" in stdout)):
                self.output.append("Nothing detected with jsteg:(")
            else:
                self.output.append("Detected: "+str(stdout))

        else:
            for l in stdout.split("\n"):
                self._save_in_output(l)


    def _save_in_output(self, out):
        self.output.append(self.check_found(out))