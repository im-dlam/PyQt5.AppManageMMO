import cv2, numpy as np, os, requests, traceback

PIXEL = 1.5262201462308829

def dow_img(link):
    return cv2.imdecode(np.frombuffer(requests.get(link).content, np.uint8), -1)[:, :, :3]

def dow_img_the_same(link):
    return cv2.imdecode(np.frombuffer(requests.get(link).content, np.uint8), 1)

class PuzleSolver:
    def __init__(self, size_slide, size_bg, img_slide, img_bg):
        self.size_slide = size_slide
        self.size_bg = size_bg
        self.img_slide = img_slide
        self.img_bg  = img_bg


    def get_position(self):

        self.img_bg  = cv2.resize(self.img_bg , self.size_bg, interpolation = cv2.INTER_LINEAR)
        self.img_slide = cv2.resize(self.img_slide, self.size_slide, interpolation = cv2.INTER_LINEAR)

        img = self.__sobel_operator(self.img_slide)
        background = self.__sobel_operator(self.img_bg)

        res = cv2.matchTemplate(img, background, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.28)
        data = list(zip(*loc[::-1]))
        is_match = len(data) > 0
        if is_match:
            w, h = img.shape[1], img.shape[0]
            x, y = data[0][0] + int(w / 2), data[0][1]
            cv2.rectangle(self.img_bg, (x, y), (x + int(w / 2), y + h), (255,0,0), 1)
            return x
        else:
            return False


    def __sobel_operator(self, img_path):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S
        img = cv2.GaussianBlur(img_path, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

class Bypass_captcha_rotate:
    def __init__(self, img_boder, img_inside):
        self.img_boder = img_boder[:, :, :3]
        self.img_inside = img_inside[:, :, :3]

    def __rotate_img(self, img, angle):
        matrix = cv2.getRotationMatrix2D(
            (img.shape[0]/2, img.shape[1]/2), angle, 1)
        img = cv2.warpAffine(img, matrix, (img.shape[0], img.shape[1]))
        return img

    def __group_img(self, img_boder, img_in, angle: int = 0):
        img_boder_new = img_boder.copy()
        img_in_new = img_in.copy()

        if angle != 0:
            img_boder_new = self.__rotate_img(img_boder_new, angle)
            img_in_new = self.__rotate_img(img_in_new, -angle)

        img_boder_new[68:279, 68:279][img_in_new[:, :] != [
            0, 0, 0]] = img_in_new[img_in_new[:, :] != [0, 0, 0]]
        img_boder_new = cv2.medianBlur(img_boder_new, 5)
        return img_boder_new

    def group_img_by_mask(self, img_boder, img_inside, angle):
        img_boder_new = img_boder.copy()
        img_in_new = img_inside.copy()

        img_boder_new = self.__rotate_img(img_boder_new, angle)
        img_in_new = self.__rotate_img(img_in_new, -angle)

        roi = img_boder_new[68:279, 68:279]

        img2gray = cv2.cvtColor(img_in_new, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img_in_new, img_in_new, mask=mask)

        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg, img2_fg)
        img_boder_new[68:279, 68:279] = dst

        img_boder_new = cv2.medianBlur(img_boder_new, 5)

        return img_boder_new

    def main(self):
        mask = np.zeros([347, 347])
        cv2.circle(mask, (173, 173), 105, 1, 2)
        min_score = 9999999999999

        for i in range(20, 180+1, 1):
            img_temp = self.__group_img(self.img_boder, self.img_inside, i)
            cany = cv2.Canny(img_temp, 128, 128, L2gradient=True)
            score = cany[mask != 0].sum()
            if(score < min_score):
                min_score = score
                angle = i

        img = self.__group_img(self.img_boder, self.img_inside, angle)
        #self.show(img)
        return angle, img

        def show(self, img):
            cv2.imshow("Img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
class SloveCaptcha:
    
    def __init__(self, pathImgOrurl: str) -> None:
        try:
            if 'http' in pathImgOrurl:
                img = SloveCaptcha.__convertLinkImage(pathImgOrurl)
            else:
                img = cv2.imread(pathImgOrurl)
            dim = (340, 212)
            # self.img = img.copy()
            self.img = cv2.resize(img.copy(), dim ,interpolation = cv2.INTER_AREA)
            # cv2.imshow('', self.img)
            # cv2.waitKey()
        except:pass
        
    @staticmethod
    def __convertLinkImage(url: str) -> object:
        try:
            ct = requests.get(url).content
            img = cv2.imdecode(np.frombuffer(ct, np.uint8), -1)[:,:,:3][:,:,::-1]
            # with open('a.png', "wb") as file:
            #     # get request
            #     response = requests.get(url)
            #     # write to file
            #     file.write(response.content)
            return img
        except: return False
    
    def __detect_yelow(self, img):
        return cv2.medianBlur((cv2.inRange(img,(200,200,100),(255,230,150))&(img[:,:,1]-img[:,:,2]>50)&(img[:,:,0]-img[:,:,2]>75))*1,5)
    
    def __detect_red(self, img):
        return cv2.medianBlur((cv2.inRange(img,(220,150,130),(255,200,160))&(img[:,:,0]-img[:,:,1]>30)&(img[:,:,1]>img[:,:,2]))*1,5)
    
    def __detect_gray(self, img):
        return cv2.medianBlur((cv2.inRange(img,(170,150,140),(201,181,180))&((img[:,:,0]-(img[:,:,0]*0.5+img[:,:,2]*0.5))<30))*1,5)
    
    def __detect_violet(self, img):
        return cv2.medianBlur((cv2.inRange(img,(160,90,170),(220,160,225))&(img[:,:,0]-img[:,:,1]>30)&(img[:,:,2]-img[:,:,1]>30))*1,5)
    
    def __detect_green(self, img):
        return cv2.medianBlur((cv2.inRange(img,(140,160,120),(180,230,180))&(img[:,:,1]-img[:,:,0]>30)&(img[:,:,1]-img[:,:,2]>30))*1,5)
    
    def __detect_blue(self, img):
        return cv2.medianBlur((cv2.inRange(img,(120,180,220),(160,210,255))&(img[:,:,1]>img[:,:,0])&(img[:,:,2]>img[:,:,1]))*1,5)
    
    def __contour_box(self, contour):
        con = contour[:,0]
        x1, x2, y1, y2 = con[:,0].min(), con[:,0].max(), con[:,1].min() ,con[:,1].max()
        return x1, y1, x2, y2 
    
    def V2(self, typeReturn: str):
        try:
            yelow = self.__detect_yelow(self.img)
            red = self.__detect_red(self.img)
            gray = self.__detect_gray(self.img)
            violet = self.__detect_violet(self.img)
            green = self.__detect_green(self.img)
            blue = self.__detect_blue(self.img)
            z = np.zeros(self.img.shape[:2])
            list_image_mini = []
            list_rectangle = []
            for img_threshold in [yelow, red, gray, violet, green, blue]:
                for con in cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
                    if cv2.contourArea(con)>100:
                        x1,y1,x2,y2 = self.__contour_box(con)
                        cv2.rectangle(z,(x1,y1),(x2,y2),(255,0,0),2)
                        list_image_mini.append(np.uint8(cv2.threshold(cv2.cvtColor(self.img[y1-5:y2+5,x1-5:x2+5],cv2.COLOR_BGR2GRAY),0,255,cv2.THRESH_OTSU)[1]==0))
                        list_rectangle.append([x1,y1,x2,y2])
            p_min = {'%': 0,'box1':'','box2':''}
            for i in range(len(list_image_mini)):
                h,w = list_image_mini[i].shape[:2]
                im1 = cv2.resize(list_image_mini[i],(w,h))
                x1,y1,x2,y2 = list_rectangle[i]
                cv2.putText(self.img,str(i),(x1,y1),1,2,(255,0,255),2)
                cv2.rectangle(self.img,(x1,y1),(x2,y2),(128,128,128))
                for j in range(i+1,len(list_image_mini)):
                    im2 = cv2.resize(list_image_mini[j],(w,h))
                    x1,y1,x2,y2 = list_rectangle[i]
                    v1 = (x2-x1)/(y2-y1)
                    x1,y1,x2,y2 = list_rectangle[j]
                    v2 = (x2-x1)/(y2-y1)
                    pre2 = v1/v2 if v1<v2 else v2/v1
                    pse_sub = (im1==im2).sum()/(im1.shape[0]*im1.shape[1])
                    pse = np.max(cv2.matchTemplate(im1,im2,cv2.TM_CCOEFF_NORMED))
                    pre_result = (pse**2)*(pre2**2)*(pse_sub**2)
                    if pre_result>p_min['%']:
                        p_min['%'] = pre_result
                        x1,y1,x2,y2 = list_rectangle[i]
                        p_min['box1'] = (x1,y1,x2,y2)
                        x1,y1,x2,y2 = list_rectangle[j]
                        p_min['box2'] = (x1,y1,x2,y2)
            if (p_min['box1']=='')|(p_min['box2']==''):
                return False
            
            if (typeReturn == 'image'):
                color = (255,0,0)
                x1,y1,x2,y2 = p_min['box1']
                cv2.rectangle(self.img,(x1-3,y1-3),(x2+3,y2+3),color,3) 
                x1,y1,x2,y2 = p_min['box2']
                cv2.rectangle(self.img,(x1-3,y1-3),(x2+3,y2+3),color,3)
                cv2.putText(self.img,str(np.round(p_min['%']*100,2))+'%',(30,50),1,2,(255,0,0),2)
                return self.img
            
            else:
                x1,y1,x2,y2 = p_min['box1']
                point_1 = (x1+x2)//2, (y1+y2)//2
                x1,y1,x2,y2 = p_min['box2']
                point_2 = (x1+x2)//2, (y1+y2)//2
                color = (255,0,0)
                x1,y1,x2,y2 = p_min['box1']
                cv2.rectangle(self.img,(x1-3,y1-3),(x2+3,y2+3),color,3) 
                x1,y1,x2,y2 = p_min['box2']
                cv2.rectangle(self.img,(x1-3,y1-3),(x2+3,y2+3),color,3)
                cv2.putText(self.img,str(np.round(p_min['%']*100,2))+'%',(30,50),1,2,(255,0,0),2)
                # cv2.imshow('', self.img)
                # cv2.waitKey(5000)
                return point_1, point_2
        except: print(traceback.print_exc())
