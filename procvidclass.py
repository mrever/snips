from numpy import *
from glob import glob
from matplotlib.pyplot import *
import cv2
import sys
import subprocess

class pvid(object):

    def __init__(self,fullpathin):
        self.fullpathin = fullpathin
        self.fname = fullpathin.split('/')[-1]
        self.basename, self.ext = self.fname.split('.')[:2]
        self.outname = self.basename + '_proc.' + self.ext

        cap = cv2.VideoCapture(fullpathin)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.w = int((cap.get(cv2.CAP_PROP_FRAME_WIDTH)) )
        self.h = int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.fourcc = int((cap.get(cv2.CAP_PROP_FOURCC)))
        cap.release()

        self.mask = None

    def downscale(self):
        resizewidth=640
        if self.w>resizewidth:
            newfile =  self.basename + '_small.' + self.ext
            subprocess.call('ffmpeg -y -i ' + self.fullpathin + ' -vf scale=' + str(resizewidth) + ':' + str(round(1.0*resizewidth/self.w*self.h)) + ' '+newfile)
            self.fullpathin = newfile
            cap = cv2.VideoCapture(self.fullpathin)
            self.fps = cap.get(cv2.CAP_PROP_FPS)
            self.w = int((cap.get(cv2.CAP_PROP_FRAME_WIDTH)) )
            self.h = int((cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.fourcc = int((cap.get(cv2.CAP_PROP_FOURCC)))
            cap.release()

    def genmask(self):
        fwidth = 160
        fheight = 90
        subprocess.call('rm *.png')
        subprocess.call('ffmpeg -i ' + self.fullpathin + ' -vf select=\'eq(pict_type\\,I)\' -vsync 2 -s ' +str(fwidth)+ 'x' +str(fheight)+ ' -f image2 keyfrs-%06d.png')

        fis = glob('*.png')

        print(len(fis))

        framestack = zeros((fheight,fwidth,len(fis))).astype('uint8')

        for findex in range(len(fis)):
            thisframe = cv2.imread(fis[findex],0)
            framestack[:,:,findex] = thisframe

        dev = std(framestack,2)
        avg = mean(framestack,2)
        rms = dev/avg

        thresh = 0*thisframe

        thresh[rms<0.32]=255
   
        mask = thresh

        offset = 45
        x = arange(fwidth)
        y = arange(fheight)
        xv, yv = meshgrid(x,y)

        mask[logical_and(yv>offset,yv<fheight-offset)]=0
        mask[logical_and(xv>offset,xv< fwidth-offset)]=0

        kernel = ones((5,5),uint8)
        mask = cv2.dilate(mask,kernel,iterations = 3)
        self.mask = cv2.resize( mask, dsize = (self.w,self.h) )
        
        subprocess.call('rm *.png')
        cv2.imwrite('mask.png', mask)



    def frameproc(self,framein,mask=None):
        # frameout = cv2.flip(framein,0)
        frameout = framein
        if mask != None:
            frameout = cv2.inpaint(framein,mask,3,cv2.INPAINT_TELEA)

        return frameout


    def procvid(self):
        cap = cv2.VideoCapture(self.fullpathin)
        out = cv2.VideoWriter(self.outname,self.fourcc, self.fps, (self.w,self.h))

        fcount=0

        while(cap.isOpened()):
            ret, frame = cap.read()

            # if fcount>2000:
                # break

            if ret==True:
                frame=self.frameproc(frame,self.mask)
                out.write(frame)
                fcount+=1
                sys.stdout.write('\r'+'frame number: '+str(fcount))
                sys.stdout.flush()

            else:
                print('')
                break

        out.release()
        cap.release()

        subprocess.call('ffmpeg -y -i ' + self.outname + ' -i ' + self.fullpathin + ' -c:v copy -c:a copy -strict experimental -map 0:v:0 -map 1:a:0 output.'+self.ext)
        subprocess.call('rm ' + self.outname)
        subprocess.call('mv output.' + self.ext + ' '  + self.outname)

###


# fname = './sub/fttf.mp4'
fname = './ddin.avi'

if len(sys.argv) > 1:
    fname = sys.argv[1]

print("converting file: " + fname)

f=pvid(fname)
f.downscale()
f.genmask()
f.procvid()

