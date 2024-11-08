from skimage import img_as_ubyte
import scipy.ndimage as ndi
from PIL import Image        

def histogram_equalization(im):
    hist = ndi.histogram(im, min=0, max=255, bins=256)
    cdf = hist.cumsum()/hist.sum() 
    im_eq = cdf[im]*1             #Mengembalikan range float ke [-1,1] 
    im_eq = img_as_ubyte(im_eq)
    hist_eq = ndi.histogram(im_eq, 0, 255, bins=256)

    return hist, im_eq, hist_eq

from skimage import exposure
def adaptive_HE(im, clip_lim):
    im_ahe = exposure.equalize_adapthist(im, clip_limit=clip_lim)
    im_ahe = img_as_ubyte(im_ahe)
    
    return im_ahe

import numpy as np
def contrast_stretching(im, a_min, a_max, a_low, a_high):
    stretch_im = (im-a_low) * ((a_max-a_min)/(a_high-a_low))
    hist_cs = ndi.histogram(stretch_im, min=0, max=255, bins=256)
    im_cs = stretch_im/np.amax(stretch_im)   #Clipping agar piksel berada di rentang 0-255     
    im_cs = np.clip(im_cs, 0, 1)
    im_cs = img_as_ubyte(im_cs)       #mengubah kembali tipe citra menjadi uint8
    
    return im_cs, hist_cs

from numpy import sqrt
def mean_filter(im, filter_size):
    image = im @ [0.2126, 0.7152, 0.0722]
    image = image/255
    image = img_as_ubyte(image)
    output = np.zeros(image.shape, np.uint8)
    result = 0

    m_size = int((sqrt(filter_size)/2)-0.5)
    for j in range(m_size, image.shape[0]-m_size):
        for i in range(m_size, image.shape[1]-m_size):
            for y in range(-m_size, (m_size+1)):
                for x in range(-m_size, (m_size+1)):
                    result = result + image[j+y, i+x]
            output[j][i] = int(result/filter_size)    
            result = 0

    return output

# def max_filter(im_max, kmax_size):
#     output_max = np.zeros(im_max.shape, np.uint8)
#     max_size = int((kmax_size/2)-0.5)
#     img_max = []
#     for x in range(max_size, im_max.shape[0]-max_size):
#         for y in range(max_size, im_max.shape[1]-max_size):
#             for s in range(x-max_size, x+max_size):
#                 for t in range(y-max_size, y+max_size):
#                     img_max.append(im_max[s,t])   
#             out_max = max(img_max)
#             output_max[x,y] = out_max
#             img_max.clear()
#     return output_max   

# def min_filter(im_min, kmin_size):
#     output_min = np.zeros(im_min.shape, np.uint8)
#     min_size = int((kmin_size/2)-0.5)
#     img_min = []
#     for x in range(min_size, im_min.shape[0]-min_size):
#         for y in range(min_size, im_min.shape[1]-min_size):
#             for s in range(x-min_size, x+min_size):
#                 for t in range(y-min_size, y+min_size):
#                     img_min.append(im_min[s,t])      
#             out_min = min(img_min)
#             output_min[x,y] = out_min
#             img_min.clear()
#     return output_min  

def evaluation_ENL(im):
    image = Image.open(im).convert('L')    #convert grayscale
    image = img_as_ubyte(image)
    
    mean = np.square(np.mean(image))
    stdev = np.square(sqrt(np.mean(abs(image - np.mean(image))**2)))
    im_enl = mean/stdev
    
    return im_enl

def evaluation_PSNR(ori, im):
    image = Image.open(im).convert('L')
    image = np.array(image) / 255
    original = Image.open(ori).convert('L')
    original = np.array(original) / 255
    MSE = np.mean((original-image)**2)
    if MSE == 0:
        return 100
    im_psnr = 10*np.log10((255**2)/MSE)
    return im_psnr

def evaluation_NM(ori, im):
    image = Image.open(im).convert('L')
    image = np.array(image) / 255
    original = Image.open(ori).convert('L')
    original = np.array(original) / 255
    im_nm = np.mean(image)/np.mean(original)
    return im_nm

def edgedetect_derivate(im):
    image = im @ [0.2126, 0.7152, 0.0722]
    image = image/255
    image = img_as_ubyte(image)

    vert = np.array([[-0.5],[0],[0.5]])
    gradvert = ndi.convolve(image, vert)
    horz = vert.T
    gradhorz = ndi.convolve(image, horz)
    
    grad_im = np.sqrt(gradvert**2 + gradhorz**2)
    grad_eq = grad_im/np.amax(grad_im)
    grad_eq = np.clip(grad_eq, 0, 255)
    grad_mag = img_as_ubyte(grad_eq)
    return grad_mag

def edgedetection_sobelprewitt(im, horz, vert):
    image = im @ [0.2126, 0.7152, 0.0722]
    image = image/255
    image = img_as_ubyte(image)

    horz_value = ndi.convolve(image, horz)
    vert_value = ndi.convolve(image, vert)
    mag_edges = np.sqrt(horz_value**2 + vert_value**2)        #calculate edge magnitude
    edges = mag_edges/np.amax(mag_edges)  
    edges = np.clip(edges, 0, 255)
    result = img_as_ubyte(edges) 
    return result

def edgedetection_robert(im):
    roberthorz = np.array([[0,1],[-1,0]])
    robertvert = np.array([[1,0],[0,-1]])

    image = im @ [0.2126, 0.7152, 0.0722]
    image = image/255
    image = img_as_ubyte(image)

    horz_value = ndi.convolve(image, roberthorz)
    vert_value = ndi.convolve(image, robertvert)
    mag_edges = np.sqrt(horz_value**2 + vert_value**2)        #calculate edge magnitude
    edges = mag_edges/np.amax(mag_edges)  
    edges = np.clip(edges, 0, 255)
    result = img_as_ubyte(edges) 
    return result

import cv2
def edgedetection_laplacian(image, gk, lk):
    source = cv2.GaussianBlur(image, (gk, gk), 0)
    source_gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)   #convert grayscale
    lapl_img = cv2.Laplacian(source_gray, cv2.CV_16S, ksize=lk)   #ddepth, ksize
    abs_img = cv2.convertScaleAbs(lapl_img)
    return abs_img