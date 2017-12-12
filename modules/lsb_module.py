from PIL import Image
import binascii

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
        img = Image.open(self.file_path)
        pixels_orig = img.load() 
        (w,h)=img.size
        
        outimg_r, outimg_g, outimg_b, outimg_rgb, outimg_rgbi = Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white"), Image.new('RGB', (w,h), "white")
        pximg_r, pximg_g, pximg_b, pximg_rgb, pximg_rgbi = outimg_r.load(), outimg_g.load(), outimg_b.load(), outimg_rgb.load(), outimg_rgbi.load()
        is_r, is_g, is_b = 0, 0, 0
        r_text, g_text, b_text, rgb_text = "", "", "", ""

        for i in range(0,h):
            for j in range(0,w):
                (r,g,b) = pixels_orig[j,i]
                #print "r:"+str(bin(r))+" g:"+str(bin(g))+" b:"+str(bin(b))  
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
                pximg_rgbi[j,i]=(self._au_contraire(is_r), self._au_contraire(is_g), self._au_contraire(is_b))
            
        #Hidden Text
        rf_text = binascii.unhexlify('%x' % int(r_text[:(len(r_text)/8)*8],2))
        rfi_text = binascii.unhexlify('%x' % int(r_text[::-1][:(len(r_text)/8)*8],2)) # Reverse binary
        gf_text = binascii.unhexlify('%x' % int(g_text[:(len(g_text)/8)*8],2))
        gfi_text = binascii.unhexlify('%x' % int(g_text[::-1][:(len(g_text)/8)*8],2))
        bf_text = binascii.unhexlify('%x' % int(b_text[:(len(b_text)/8)*8],2))
        bfi_text = binascii.unhexlify('%x' % int(b_text[::-1][:(len(b_text)/8)*8],2))
        rgbf_text = binascii.unhexlify('%x' % int(rgb_text[:(len(rgb_text)/8)*8],2))
        rgbfi_text = binascii.unhexlify('%x' % int(rgb_text[::-1][:(len(rgb_text)/8)*8],2))


        strs = []
        strs += find_strings(rf_text, self.min_len)
        strs += find_strings(rfi_text, self.min_len)
        strs += find_strings(gf_text, self.min_len)
        strs += find_strings(gfi_text, self.min_len)
        strs += find_strings(bf_text, self.min_len)
        strs += find_strings(bfi_text, self.min_len)
        strs += find_strings(rgbf_text, self.min_len)
        strs += find_strings(rgbfi_text, self.min_len)
        for s in strs:
            self._save_in_output(s)


        #Save Images
        filename = self.file_path.split("/")[-1]
        outimg_r.save(self.save_directory + "/"+ filename + "_r.png","png")
        outimg_g.save(self.save_directory + "/"+ filename + "_g.png","png")
        outimg_b.save(self.save_directory + "/"+ filename + "_b.png","png")
        outimg_rgb.save(self.save_directory + "/"+ filename + "_rgb.png","png")
        outimg_rgbi.save(self.save_directory + "/"+ filename + "_rgbi.png","png")


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

    
    def _au_contraire(self,px):
        return 0 if px==255 else 255


#fourier
#convert ball_3h6SOemwRR_PmQhXh2AM.png -fft  +depth +adjoin fourier-%d.png
#convert fourier-0.png -auto-level -evaluate log 12000 spectrum.png