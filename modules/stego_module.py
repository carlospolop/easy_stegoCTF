import os
from subprocess import Popen, PIPE
from threading import Thread


class Stego_module:
    def __init__(self, file_path, out_dir, search=None, min_len=5, try_all=True, try_stego=False, try_hexdump=False, try_entropy=False):
        self.file_path = file_path
        self.out_dir = out_dir
        self.search = search
        self.min_len = min_len
        self.found = False
        self.found_array = []
        self.usefull_urls = []
        self.output, self.steghide_out, self.outguess_out, self.outguess013_out = [], [], [], []
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
                    self.output.append("CRACKED!! ("+cmd+") --> "+stdout)
                    return
                else:
                    self.output.append("Something probably not insteresting dicovered ("+cmd+") --> "+stdout)
                    return
        
        self.output.append("Nothing found")
        return
    
    def execute(self):
        if (self.try_all or self.try_stego):
            #Crackers
            absPath = os.path.dirname(os.path.abspath(__file__))+"/../"
            wordlist = absPath + "/stegocracker_dict.txt"
            #print "Wordlist: "+wordlist

            steghideCracker = absPath + "/scripts/steghideCracker.sh"
            steghideCracker_out = self.out_dir+"/steghideCracker"
            steghideThread = Thread(target= self._execute_cracker, args=("SteghideCracker", [steghideCracker, "-i", self.file_path, "-w", wordlist, "-o", steghideCracker_out], self.steghide_out))
            #print "[*] "+steghideCracker+" executed"

            outguessCracker = absPath + "/scripts/outguessCracker.sh"
            outguessCracker_out = self.out_dir+"/outguess"
            outguessThread = Thread(target= self._execute_cracker, args=("OutguessCracker", [outguessCracker, "-i", self.file_path, "-w", wordlist, "-o", outguessCracker_out], self.outguess_out))
            #print "[*] "+outguessCracker+" executed"

            outguess013Cracker = absPath + "/scripts/outguess013Cracker.sh"
            outguess013Cracker_out = self.out_dir+"/outguess013"
            outguess013Thread = Thread(target= self._execute_cracker, args=("Outguess013Cracker", [outguess013Cracker, "-i", self.file_path, "-w", wordlist, "-o", outguess013Cracker_out], self.outguess013_out))
            #print "[*] "+outguess013Cracker+" executed"


            #jphideCracker = absPath + "/../scripts/jphideCracker.sh" #Need to fix!!
            #jphideCracker_out = self.out_dir+"/jphide"
            #self._execute_tool("JPHide", [jphideCracker, "-i", self.file_path, "-w", wordlist, "-o", jphideCracker_out])

            #cloackedpixelCracker = absPath + "/../scripts/cloackedpixelCracker.sh" #Very slow!!
            #cloackedpixelCracker_out = self.out_dir+"/loackedpixel"
            #self._execute_tool("CloackedpixelCracker", [cloackedpixelCracker, "-i", self.file_path, "-w", wordlist, "-o", cloackedpixelCracker_out])

            #openstegoCracker = absPath + "/../scripts/openstegoCracker.sh" #Very slow!!
            #openstegoCracker_out = self.out_dir+"/openstego"
            #self._execute_tool("OpenstegoCracker", [openstegoCracker, "-i", self.file_path, "-w", wordlist, "-o", openstegoCracker_out])

            steghideThread.start()
            outguessThread.start()
            outguess013Thread.start()

            #Generals
            self._execute_tool("File", ["file", self.file_path])
            self._execute_tool("Identify", ["identify", "-verbose", self.file_path])
            self._execute_tool("Exiftool", ["exiftool", self.file_path])
            self._execute_tool("Binwalk", ["binwalk", self.file_path])
            self._execute_tool("Foremost", ["foremost", "-o", self.out_dir+"/foremost", "-i", self.file_path])
            self._execute_tool("Strings (head 20)", "strings -n "+str(self.min_len)+" "+self.file_path+" | head -n 20", shell=True)
            self._execute_tool("Strings (tail 20)", "strings -n "+str(self.min_len)+" "+self.file_path+" | tail -n 20", shell=True)           

            #Stego
            for t,name in zip(["j", "o", "p", "i", "f", "F", "a"],["JSteg", "Outguess", "JPHide", "Invisible secrets", "F5", "Sophisticated F5", "At end of file (camouflage or appendX)"]):
                self._execute_tool("StegDetect -t "+t+" ("+name+")", ["stegdetect", "-t", t, self.file_path])
            
            #print "[*] StegDetect executed"
            self._execute_tool("PngCheck", ["pngcheck", self.file_path])
            #print "[*] PngCheck executed"
            self._execute_tool("ZSteg", ["zsteg", "-a", "--min-str-len", str(self.min_len), self.file_path])
            #print "[*] ZSteg executed"
            self._execute_tool("StegHide", ["steghide", "extract", "-sf", self.file_path, "-p", '""'])
            #print "[*] StegHide executed"
            self._execute_tool("StegoVeritas", ["stegoveritas.py", self.file_path, "-outDir", self.out_dir, "-imageTransform", "-colorMap", "-trailing"])
            #print "[*] StegoVeritas executed"

            path_jsteg_out = self.out_dir+"/jstegOUT"
            self._execute_tool("Jsteg", ["jsteg", "reveal", self.file_path, path_jsteg_out])
            self._check_file(path_jsteg_out, "jsteg reveal "+self.file_path+ " " +path_jsteg_out)
            #print "[*] Jsteg executed"

            path_outguess_out = self.out_dir+"/outguessOUT"
            self._execute_tool("Outguess", ["outguess", "-r", self.file_path, path_outguess_out], check=path_outguess_out)
            #print "[*] Outguess executed"
            
            path_outguess013_out = self.out_dir+"/outguessOUT-013"
            self._execute_tool("Outguess-0.13", ["outguess-0.13", "-r", self.file_path, path_outguess013_out], check=path_outguess013_out)
            #print "[*] Outguess-0.13 executed"

            path_openstego_out = self.out_dir+"/openstego"
            self._execute_tool("OpenStego", "echo -e \"\\n\" | openstego extract -sf "+self.file_path+" -xf "+path_openstego_out, shell=True, check=path_openstego_out)
            #print "[*] OpenStego executed"

            path_lsbsteg_out = self.out_dir+"/lsbsteg"
            self._execute_tool("LSBSteg", ["LSBSteg", "decode", "-i", self.file_path, "-o", path_lsbsteg_out], check=path_lsbsteg_out)
            #print "[*] LSBSteg executed"

            steganoTool = absPath + "/scripts/check_steganoTool.sh"
            steganoTool_out = self.out_dir+"/steganoTool"
            self._execute_tool("SteganoTool", [steganoTool, "-i", self.file_path, "-o", steganoTool_out])
            #print "[*] "+steganoTool+" executed"

            #Wait for the threads
            steghideThread.join()
            outguessThread.join()
            outguess013Thread.join()

            #Add outputs
            self.output = self.output + self.steghide_out + self.outguess_out + self.outguess013_out
   
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


    def _execute_tool(self, name, line, shell=False, check=False):
        try:
            self.output.append("#### "+name+" ####")
            self._execute_line(line, shell=shell)
            if check:
                self._check_file(check, " ".join(line))
                            
            self.output.append("#### "+name+" End ####\n")
        except Exception as e:
            self.output.append("Error: Do you have installed "+name+" and in PATH?")
            self.output.append(e)


    def _execute_cracker(self, name, line, out):
        try:
            out.append("#### "+name+" ####")
            self._execute_line(line, out=out)
            out.append("#### "+name+" End ####\n")
        except Exception as e:
            out.append("Error: ")
            out.append(e)


    def _execute_line(self, cmd, shell=False, out=False):
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

        elif "jsteg" in cmd:
            if (("invalid JPEG" in stdout) or ("not contain hidden" in stdout) or (len(stdout) < 5)):
                self.output.append("Nothing detected with jsteg:(")
            else:
                self.output.append("Detected: "+str(stdout))

        else:
            for l in stdout.split("\n"):
                if out:
                    out.append(l)
                else:
                    self._save_in_output(l)        
        

    def _save_in_output(self, out):
        self.output.append(self.check_found(out))
