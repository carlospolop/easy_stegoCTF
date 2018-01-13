from exifread.tags import DEFAULT_STOP_TAG, FIELD_TYPES
from exifread import process_file, exif_log, __version__


class Exif_module:
    def __init__(self, file_path, search=None):
        self.file_path = file_path
        self.search = search
        self.found = False
        self.found_array = []
        self.usefull_urls = ["https://metashieldclean-up.elevenpaths.com/#analizeButton", "https://onlineexifviewer.com/", "http://exifdata.com/", "http://metapicz.com/#landing", "http://exif-viewer.com/", "http://exif.regex.info/exif.cgi"]
        self.output = []
        self.name = "Exif"


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
            img_file = open(str(self.file_path), 'rb')
        except IOError:
            self._save_in_output("File is unreadable\n")
            return

        # get the tags
        data = process_file(img_file, stop_tag=DEFAULT_STOP_TAG, details=True, strict=False, debug=False)

        if not data:
            self._save_in_output("No EXIF information found\n")
            return

        if 'JPEGThumbnail' in data:
            self._save_in_output('File has JPEG thumbnail')
            self._save_in_output(data['JPEGThumbnail'])
        if 'TIFFThumbnail' in data:
            self._save_in_output('File has TIFF thumbnail')
            self._save_in_output(data['TIFFThumbnail'])
            #del

        tag_keys = list(data.keys())
        tag_keys.sort()

        for i in tag_keys:
            try:
                self._save_in_output(str(i)+" ("+str(FIELD_TYPES[data[i].field_type][2])+"): "+str(data[i].printable))
            except:
                self._save_in_output(str(i)+" : "+str(data[i]))


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