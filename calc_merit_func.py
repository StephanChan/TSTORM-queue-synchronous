import numpy as np
import random

class merit_func():
    def __init__(self):
        super().__init__()

    def calc(self,image):
        image_fft=np.fft.fft2(image)
        merit_value=0
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                merit_value+=((i+0.5-image.shape[0]/2.0)**2+(j+0.5-image.shape[1]/2.0)**2)*image_fft[i][j]
        image_fft_sum=np.sum(image_fft)
        return merit_value/image_fft_sum

if __name__=='__main__':
    image=np.ones((2048*2048,),dtype=np.uint16)
    for i in range(2048*2048):
        image[i]=random.randint(0,65535)
    test=merit_func()
    print(test.calc(image.reshape(2048,2048)))
