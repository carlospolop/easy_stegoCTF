import binwalk

class Binwalk_module:
    def __init__(self, file_path, save_directory, hexdump, search=None, sanitize=False):
        self.file_path = file_path
        self.save_directory = save_directory
        self.hexdump = hexdump
        self.search = search
        self.sanitize = sanitize
        self.current_entropy = -1
        self.found = False
        self.found_array = []
        self.usefull_urls = []
        self.output = []
        self.name = "Binwalk"


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

    
    def execute(self):
        for module in binwalk.scan(self.file_path, signature=True, opcodes=True, extract=True, matryoshka=True, depth=100, entropy=True, nplot=True, directory=self.save_directory, hexdump=self.hexdump, quiet=True):
            for result in module.results:
                if result.module == "Entropy":
                    if self._check_entropy(result.description):
                        self._save_in_output("\t%s    %s    0x%.8X    %s" % (result.module, self._sanitize_path(result.file.path), result.offset, result.description))
                else:
                    if result.file:
                        self._save_in_output("\t%s    %s    0x%.8X    %s" % (result.module, self._sanitize_path(result.file.path), result.offset, result.description))
                        if module.extractor.output.has_key(result.file.path):
                        # These are files that binwalk carved out of the original firmware image, a la dd
                            if module.extractor.output[result.file.path].carved.has_key(result.offset):
                                self._save_in_output("Carved data from offset 0x%X to %s" % (result.offset, self._sanitize_path(module.extractor.output[result.file.path].carved[result.offset])) )
                                # These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
                            if module.extractor.output[result.file.path].extracted.has_key(result.offset):
                                self._save_in_output("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(module.extractor.output[result.file.path].extracted[result.offset].files),
                                                                                                        result.offset,
                                                                                                        self._sanitize_path(module.extractor.output[result.file.path].extracted[result.offset].files[0]),
                                                                                                        module.extractor.output[result.file.path].extracted[result.offset].command) )


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


    def _check_entropy(self, entropy):
        if (float(entropy) > self.current_entropy+0.05) or (float(entropy) < self.current_entropy-0.05):
            self.current_entropy = float(entropy)
            return True
        return False


    def _sanitize_path(self,path):
        return "/public/"+path.split("public/")[-1] if self.sanitize else path