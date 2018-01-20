from PIL import Image

from strings_module import find_strings


class LSB_module:
    def __init__(self, file_path, save_directory, search=None, min_len=5):
        self.file_path = file_path
        self.save_directory = save_directory
        self.search = search
        self.min_len = min_len+1
        self.found = False
        self.found_array = []
        self.usefull_urls = []
        self.output = []
        self.name = "LSB"


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
            img = Image.open(self.file_path)
        except:
            self.output.append("No image")
            return

        pixels_orig = img.load() 
        (w,h)=img.size
        
        outimg_r, outimg_g, outimg_b, outimg_rgb, outimg_rgbi = Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white")
        pximg_r, pximg_g, pximg_b, pximg_rgb, pximg_rgbi = outimg_r.load(), outimg_g.load(), outimg_b.load(), outimg_rgb.load(), outimg_rgbi.load()
        is_r, is_g, is_b = 0, 0, 0
        r_text, g_text, b_text, rgb_text = "", "", "", ""

        #Remove comments if you want to check more things
        for i in range(0,h):
            for j in range(0,w):
                try:
                    (r,g,b) = pixels_orig[j,i]
                except:
                    self.output.append("More than 3bytes py pixel")
                    return
                if(r%2==0):
                    r_text += "0"
                    rgb_text += "0"
                    is_r = 0
                    pximg_r[j,i]=(0,0,0)
                else:
                    r_text += "1"
                    rgb_text += "1"
                    is_r = 255

                if(g%2==0):
                    g_text += "0"
                    rgb_text += "0"
                    is_g = 0
                    pximg_g[j,i]=(0,0,0)
                else:
                    g_text += "1"
                    rgb_text += "1"
                    is_g = 255

                if(b%2==0):
                    b_text += "0"
                    rgb_text += "0"
                    is_b = 0
                    pximg_b[j,i]=(0,0,0)
                else:
                    b_text += "1"
                    rgb_text += "1"
                    is_b = 255

                pximg_rgb[j,i]=(is_r, is_g, is_b)
                #pximg_rgbi[j,i]=(self._au_contraire(is_r), self._au_contraire(is_g), self._au_contraire(is_b))
            
        #Hidden Text
        try:
            rf_text = self._get_text(r_text)
            #rfi_text = self._get_text(r_text[::-1]) # Reverse binary
            gf_text = self._get_text(g_text)
            #gfi_text = self._get_text(g_text[::-1])
            bf_text = self._get_text(b_text)
            #bfi_text = self._get_text(b_text[::-1])
            rgbf_text = self._get_text(rgb_text)
            #rgbfi_text = self._get_text(rgb_text[::-1])
        except Exception as e:
            print "Error extracting text from images: "+e

        strs = []
        strs += find_strings(rf_text, self.min_len)
        #strs += find_strings(rfi_text, self.min_len)
        strs += find_strings(gf_text, self.min_len)
        #strs += find_strings(gfi_text, self.min_len)
        strs += find_strings(bf_text, self.min_len)
        #strs += find_strings(bfi_text, self.min_len)
        strs += find_strings(rgbf_text, self.min_len)
        #strs += find_strings(rgbfi_text, self.min_len)
        for s in strs:
            self._save_in_output(s)


        #Save Images
        filename = self.file_path.split("/")[-1]
        outimg_r.save(self.save_directory + "/"+ filename + "_r.png","png")
        outimg_g.save(self.save_directory + "/"+ filename + "_g.png","png")
        outimg_b.save(self.save_directory + "/"+ filename + "_b.png","png")
        outimg_rgb.save(self.save_directory + "/"+ filename + "_rgb.png","png")
        #outimg_rgbi.save(self.save_directory + "/"+ filename + "_rgbi.png","png")


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


    def _save_in_output(self, out):
        if not out in self.output:
            self.output.append(self.check_found(out))

    
    def _au_contraire(self,px):
        return 0 if px==255 else 255


    def _get_text(self, bin_data):
        return ''.join(chr(int(bin_data[i:i+8], 2)) for i in xrange(0, len(bin_data), 8))
