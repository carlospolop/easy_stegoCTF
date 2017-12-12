import string, re


class Strings_module:
    def __init__(self, file_path, search=None, min_len=5):
        self.file_path = file_path
        self.search = search
        self.min_len = min_len
        self.found = False
        self.found_array = []
        self.usefull_urls = []
        self.output = []
        self.name = "Strings"


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
        try:
            with open(self.file_path, 'rb') as f:
                content = f.read() 
        except IOError:
            self._save_in_output("File is unreadable\n")
            return

        strs = find_strings(content, self.min_len)
        for s in strs:
            self._save_in_output(s)


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


    def _save_in_output(self, out):
        self.output.append(self.check_found(out))


def check_valid_string(string_toCheck):
    return True if len(re.findall(r'\W', string_toCheck) <= len(string_toCheck)*0.3) else False


def find_strings(data, min_len):
    strings_found, strings_found_comp = []
    current_string, str_comp = "", ""
    for byte in data:
        if byte in string.printable[:95]: #No \t\n\r\x0b\x0c
            current_string += str(byte)
        else:
            if current_string and len(current_string) >= min_len and check_valid_string(current_string):
                cs_rev = current_string[::-1]
                strings_found.append(str(current_string)+" --> "+str(current_string[::-1]))
                current_string = ""
        
    if current_string and len(current_string) >= min_len:
        strings_found.append(str(current_string)+" --> "+str(current_string[::-1]))

    for s in strings_found:
        str_comp += s 
        if str_comp < 25:
            str_comp += " [|] "
        else:
            strings_found_comp.append(str_comp)
            str_comp = ""
    if str_comp:
        strings_found_comp.append(str_comp) 

    return strings_found_comp