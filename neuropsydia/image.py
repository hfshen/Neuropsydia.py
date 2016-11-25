# -*- coding: utf-8 -*-
import PIL
import numpy as np

from .path import *
from .core import *


# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
class Preload():
    """
    Preload images.

    Parameters
    ----------
    NA

    Returns
    ----------
    NA

    Example
    ----------
    NA

    Authors
    ----------
    Dominique Makowski

    Dependencies
    ----------
    - pygame 1.9.2
    - PIL
    """
    def __init__(self, files, x=0, y=0, size=1.0, path='', extension=''):
        self.dict_PIL = {}

        if isinstance(files, list) is False:
            list_files = []
            list_files.append(files)
        else:
            list_files = files
        n_files = len(list_files)

        if isinstance(x, list) is False:
            list_x = []
            list_x.append(x)
        else:
            list_x = x
        n_x = len(list_x)
        if n_x != n_files:
            list_files = list_files*n_x
            list_x = list_x*n_files
            list_files = list_files[:max([n_files,n_x])]
            list_x = list_x[:max([n_files,n_x])]

        if isinstance(y, list) is False:
            list_y = []
            list_y.append(y)
        else:
            list_y = y
        n_y = len(list_y)
        if n_y != n_files:
            list_files = list_files*n_y
            list_y = list_y*n_files
            list_files = list_files[:max([n_files,n_y])]
            list_y = list_y[:max([n_files,n_y])]

        if isinstance(size, list) is False:
            list_size = []
            list_size.append(size)
        else:
            list_size = size
        n_size = len(list_size)
        if n_size != n_files:
            list_files = list_files*n_size
            list_size = list_size*n_files
            list_files = list_files[:max([n_files,n_size])]
            list_size = list_size[:max([n_files,n_size])]



        for n, name in enumerate(list_files):
            if os.path.isfile(path+name+extension) is False:
                print("NEUROPSYDIA WARNING: preload_image(): wrong name, path or extension")
                if os.path.isfile(path+name+'.png') is True:
                    print("NEUROPSYDIA WARNING: preload_image(): image found adding '.png'")
                    extension = ".png"
                if os.path.isfile(path+name+'.jpg') is True:
                    print("NEUROPSYDIA WARNING: preload_image(): image found adding '.jpg'")
                    extension = ".jpg"

            image = PIL.Image.open(path+name+extension, "r")
            self.dict_PIL["%s%s%s_%s%s%s" %(path, name, extension, str(list_x[n]), str(list_y[n]), str(list_size[n]))] = image


    def to_PIL(self):
        return(self.dict_PIL)

    def to_arrays(self):
        dict_of_arrays = {}
        for i in self.cache:
            dict_of_arrays[i] = np.array(self.cache[i])
        return(dict_of_arrays)
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
def preload(file, x=0, y=0, cache=None, path='', extension='', size=1.0, unit="n", scale_by="height", fullscreen=False, rotate=0, scramble=False, compress=False, compression=0, opacity=100, key=None, monitor_diagonal=monitor_diagonal):
    """
    Preload images.

    Parameters
    ----------
    NA

    Returns
    ----------
    NA

    Example
    ----------
    NA

    Authors
    ----------
    Dominique Makowski

    Dependencies
    ----------
    - pygame 1.9.2
    - PIL
    """
    if isinstance(file, list) is False:
        files = []
        files.append(file)
    else:
        files = file

    if cache != None:
        dictionary = cache
    else:
        dictionary = {}


    for i in files:
        #Check existence of the given files
        if os.path.isfile(path+i+extension) is False:
            print("NEUROPSYDIA WARNING: preload_image(): wrong name, path or extension")
            if os.path.isfile(path+i+'.png') is True:
                print("NEUROPSYDIA WARNING: preload_image(): image found adding '.png'")
                extension = ".png"
            if os.path.isfile(path+i+'.jpg') is True:
                print("NEUROPSYDIA WARNING: preload_image(): image found adding '.jpg'")
                extension = ".jpg"


        image = PIL.Image.open(path+i+extension, "r")
        w, h = image.size

        if fullscreen is False:
            if unit == "n":  # size=1 means height is equals to 1
                if scale_by=="height":
                    new_w = int(w/h*size*screen_height/20.0)
                    new_h = int(h/h*size*screen_height/20.0)
                if scale_by=="width":
                    new_w = int(w/w*size*screen_height/20.0)
                    new_h = int(h/w*size*screen_height/20.0)
            if unit == "cm" or unit == "inch":
                if scale_by=="height":
                    new_h = int(Coordinates.to_pygame(distance_y=Coordinates.from_physical(distance_y=size, unit=unit)))
                    new_w = int(new_h * w / h)
                if scale_by=="width":
                    new_w = int(Coordinates.to_pygame(distance_x=Coordinates.from_physical(distance_x=size, unit=unit)))
                    new_h = int(new_w * h / w)

        else:
            if w > h:
                new_w = int(w/w*screen_width)
                new_h = int(h/w*screen_width)
            else:
                new_w = int(w/h*screen_height)
                new_h = int(h/h*screen_height)
        image = image.resize((new_w, new_h),PIL.Image.ANTIALIAS)
        image = image.rotate(rotate)

        if scramble == True:
            array = np.array(image)
            array = np.random.permutation(array)
            image = PIL.Image.fromarray(array)
        if compress == True:
            image = image.resize((int(w*(100-compression)/100), int(h*(100-compression)/100)), PIL.Image.ANTIALIAS)
            image.save(path + "temp.jpg", quality=10, optimize=True)
            image = PIL.Image.open(path + "temp.jpg", "r")
            image = image.resize((new_w, new_h),PIL.Image.ANTIALIAS)
            os.remove(path + "temp.jpg")

        if opacity != 100:
            image = image.convert('RGBA')
            image.putalpha(int(opacity * 255 / 100))


        image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)


        if key == None:
            dictionary[path + i + '_' + str(size) + '_' + str(unit) + '_' + str(scale_by) + '_' + str(rotate) + '_' + str(opacity) + extension] = image
        else:
            dictionary[key] = image




    #return
    return(dictionary)



#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
# # # # --- image ---
#version : 1.0
#display an image.
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
def image(file, x=0, y=0, cache=None, path='', extension='', size = 1.0, unit="n", scale_by="height", fullscreen=False, rotate=0, scramble=False, background=None, compress=False, compression=0, allow=None, wait=None, opacity=100):
    """
    Help incomplete, sorry.

    Parameters
    ----------
    NA

    Returns
    ----------
    NA

    Example
    ----------
    NA

    Authors
    ----------
    Dominique Makowski, Léo Dutriaux

    Dependencies
    ----------
    - pygame 1.9.2
    - PIL
    - time
    """
    if background is not None:
        newpage(background, auto_refresh=False)

    if cache is None:
        cache = preload(file=file, cache=cache, path=path, extension=extension, size=size, unit=unit, scale_by=scale_by, fullscreen=fullscreen, rotate=rotate, scramble=scramble, compress=compress, compression=compression, opacity=opacity)

        image = cache[path + file + '_' + str(size) + '_' + str(unit) + '_' + str(scale_by) + '_' + str(rotate) + '_' + str(opacity) + extension]

    else:
        try:
            image = cache.Cache[path + file + '_' + str(size) + '_' + str(unit) + '_' + str(scale_by) + '_' + str(rotate) + '_' + str(opacity) + extension]
        except:
            try:
                image = cache[path + file + '_' + str(size) + '_' + str(unit) + '_' + str(scale_by) + '_' + str(rotate) + '_' + str(opacity) + extension]
            except:
                print('NEUROPSYDIA ERROR: image(): file not in given cache: ' + file)
                cache = preload(file=file, cache=cache, path=path, extension=extension, size=size, unit=unit, scale_by=scale_by, fullscreen=fullscreen, rotate=rotate, scramble=scramble, compress=compress, compression=compression)
                image = cache[path + file + '_' + str(size) + '_' + str(unit) + '_' + str(scale_by) + '_' + str(rotate) + '_' + str(opacity) + extension]


    x,y = Coordinates.to_pygame(x=x,y=y)
    rectangle = image.get_rect()
    rectangle.center = (x,y)
    screen.blit(image,rectangle)

    #In case or one must wait until something
    if allow is not None or wait is not None:
        refresh()
        if allow is None and wait is not None:
            time.wait(wait)
            return(wait)
        if allow is not None:
            return(response(allow=allow, time_max=wait))
    else:
        return(cache)





