import cv2
import numpy as np

def segment_ycrcb(orig, params, tola, tolb):
    ycrcb_im = cv2.cvtColor(orig, cv2.COLOR_BGR2YCR_CB)
    Cb_key, Cr_key = params
    blue = ycrcb_im[:, :, 2]
    red = ycrcb_im[:, :, 1]

    diffbsq = (blue - Cb_key)**2
    diffrsq = (red - Cr_key)**2
    dist = np.sqrt(diffbsq + diffrsq).astype(np.float32)

    mask = ((dist - tola) / (tolb - tola)).astype(np.float32)
    mask[dist < tola] = 0.0
    mask[dist > tolb] = 1.0
    return mask

def get_region(img):
    r=(80,80,100,100)
    cv2.destroyAllWindows()
    return r


def get_params_ycrcb(img, region):
    ycrcb_img = cv2.cvtColor( np.array(img), cv2.COLOR_BGR2YCR_CB)
    cv2.destroyAllWindows()
    r = [int(x) for x in region]
    region = ycrcb_img[int(region[1]):int(
        region[1] + region[3]), int(region[0]):int(region[0] + region[2])]
    y_mean, Cr_mean, Cb_mean = np.mean(region, axis=(0, 1))
    y_std, Cr_std, Cb_std = np.std(region, axis=(0, 1))
    return [Cb_mean, Cr_mean]


def get_params_hls(img, region):
    hls_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2HLS)
    r = [int(x) for x in region]
    region = hls_img[int(region[1]):int(region[1] + region[3]),
                     int(region[0]):int(region[0] + region[2])]
    h_mean, l_mean, s_mean = np.mean(region, axis=(0, 1))
    h_std, l_std, s_std = np.std(region, axis=(0, 1))
    return [h_mean, h_std, l_mean, l_std, s_mean, s_std]

def mod_mask(mask, low, high):
    mask = mask.copy()
    mask[mask > high] = 1.0
    mask[mask < low] = 0.0
    return mask


# def get_mask(img, bg, param_ycrcb, param_hls, tola=16, tolb=50, low_thresh=0.05, high_thresh=0.25, alpha=1.0, beta=0.0, gamma=1.0, sz=5, space=200, erode_sz=3):
def get_mask(img,param_ycrcb, tola=16, tolb=50, low_thresh=0.05, high_thresh=0.25, sz=5, space=200,erode_sz=2):
 #     brimg = brighten(img,alpha,beta,gamma)
    brimg = img
    if not (sz<=0 or space<=1):
        brimg = cv2.bilateralFilter(brimg, sz, space, space)
    mask = segment_ycrcb(brimg, param_ycrcb, tola, tolb)
    mask = mod_mask(mask, low_thresh, high_thresh)
    if not(erode_sz <= 1):
        kernel = np.ones((erode_sz,erode_sz),np.uint8)
        mask = cv2.erode(mask,kernel,iterations = 1)
    return mask

def get_key_param(img):
    key_region = get_region(img)
    ycrcb = get_params_ycrcb(img, key_region)
    hls = get_params_hls(img, key_region)
    return (ycrcb, hls)

def segmenter(img):
    img[np.where((img==[0,0,0]).all(axis=2))]= [0,255,0]
    cv2.imwrite("test.jpg",img)
    cv2.imshow('image1s',img)
    try:
        img.shape
    except AttributeError:
        print("shape not found")
    # exit(1)
    key_param = get_key_param(img)
    cv2.namedWindow('controls')
    def nothing(gyxfdd):
        pass

    cv2.createTrackbar('Keying tol low', 'controls', 23 , 100, nothing)
    cv2.createTrackbar('Keying tol high', 'controls', 50, 200, nothing)
    cv2.createTrackbar('Mask low Thresh (x100)', 'controls', 5, 100, nothing)
    cv2.createTrackbar('Mask high Thresh (x100)', 'controls', 25, 100, nothing)
    cv2.createTrackbar('Erode size', 'controls', 3, 10, nothing)
    cv2.createTrackbar('BiLat size', 'controls', 5, 100, nothing)
    cv2.createTrackbar('BiLat space', 'controls', 200, 500, nothing)
    cv2.createTrackbar('Sat mul low', 'controls', 5, 100, nothing)
    cv2.createTrackbar('Sat mul high', 'controls', 7, 100, nothing)
    cv2.createTrackbar('Light mask strength', 'controls', 20, 100, nothing)
    cv2.createTrackbar('Light mask size', 'controls', 3, 20, nothing)
    tola = cv2.getTrackbarPos('Keying tol low', 'controls')
    tolb = cv2.getTrackbarPos('Keying tol high', 'controls')
    low_thresh = cv2.getTrackbarPos('Mask low Thresh (x100)', 'controls')/100
    high_thresh = cv2.getTrackbarPos('Mask high Thresh (x100)', 'controls')/100
    erode_sz = cv2.getTrackbarPos('Erode size', 'controls')
    sz = cv2.getTrackbarPos('BiLat size', 'controls')
    space  = cv2.getTrackbarPos('BiLat space', 'controls')
    sat_mul_lo  = cv2.getTrackbarPos('Sat mul low', 'controls')
    sat_mul_hi  = cv2.getTrackbarPos('Sat mul high', 'controls')
    scale_blur  = cv2.getTrackbarPos('Light mask strength', 'controls')
    blur_size  = cv2.getTrackbarPos('Light mask size', 'controls')
    key_mask = get_mask( img, key_param[0], tola, tolb, low_thresh ,high_thresh, sz, space, erode_sz)
    cv2.imwrite('C:\\Users\\1025040\\Documents\\git\\CysrtallBall\\src\\python\\whiteBlack1.jpg',key_mask*255)
    cv2.imshow('img',key_mask)
   
    return key_mask*255

if __name__=="__main__":
    segmenter(cv2.imread('C:\\Users\\1025040\\Documents\\git\\CysrtallBall\\src\\python\\Cap1.JPG'))

