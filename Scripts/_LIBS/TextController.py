import pytesseract
import numpy as np
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextController:
    def image_to_text_pillow(self, pil_image, custom_config=None, save_image=False):
        cv2_image = np.array(pil_image)
        return self.image_to_text_cv2(cv2_image=cv2_image, custom_config=custom_config, save_image=save_image)

    def image_to_text_cv2(self, cv2_image, custom_config=None, save_image=False):
        if custom_config is None:
            custom_config = r'--oem 3 --psm 6'
        gray_scale_cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray_scale_cv2_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(thresh, config=custom_config, lang='eng')
        if save_image: cv2.imwrite('thresh.png', cv2_image)
        return text