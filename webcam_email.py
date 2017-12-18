#!/usr/bin/env python3
import os
import smtplib
import datetime
import argparse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

imgdir = 'img'
toaddr = 'you@gmail.com'
fromaddr = toaddr
subject = 'Intruder Alert'
smtpserver = 'smtp.gmail.com:587'
username = 'yourusername'
password = 'yourpassword'
capture_src = 'fswebcam' 
delay = datetime.timedelta(milliseconds=0)
cam_res = (1280,960)
burst_frames = 3
cam_dev_id = "/dev/video0" # Which webcam to use for PyGame or fswebcam
if capture_src == 'videocapture':
    cam_dev_id = 0 # Which webcam to use for VideoCapture (if you only have one webcam, set this to 0)
    from VideoCapture import Device
elif capture_src == 'pygame':
    import pygame
    import pygame.camera
    from pygame.locals import *
    pygame.init()
    pygame.camera.init()
    cam_dev_id = pygame.camera.list_cameras()[0]
    os.environ['PYGAME_CAMERA'] = 'opencv'
elif capture_src == 'fswebcam':
    pass
else:
    raise Exception("Invalid capture_src ", capture_src)

def capture_imgs():
    if not os.path.exists(imgdir):
        os.mkdir(imgdir)
    imgs = []
    cam = None
    if capture_src == 'videocapture':
        cam = Device(cam_dev_id)
        #cam.setResolution(cam_res[0], cam_res[1])
    elif capture_src == 'pygame':
        cam = pygame.camera.Camera(cam_dev_id,cam_res)
        cam.start()

    for i in range(burst_frames):
        dt = datetime.datetime.now()
        fname = '{0}/{1}.jpg'.format(imgdir, dt.strftime('%Y-%m-%d_%H.%M.%S.%f'))
        if capture_src == 'videocapture':
            cam.saveSnapshot(fname, timestamp=1, boldfont=1, textpos='bl')
        elif capture_src == 'pygame':
            img = cam.get_image()
            pygame.image.save(img, fname)
        elif capture_src == 'fswebcam':
            cmd = 'fswebcam -d {} -r {}x{} {}'.format(cam_dev_id, cam_res[0], cam_res[1], fname)
            os.system(cmd)
        imgs.append(fname)
        while (datetime.datetime.now() - dt) < delay:
            pass
    return imgs

def email(imgs):
    mroot = MIMEMultipart('related')
    mroot['Subject'] = subject
    mroot['From'] = fromaddr
    mroot['To'] = toaddr

    for frame_num,frame in enumerate(imgs):
        with open(frame, 'rb') as fp:
            mimage = MIMEImage(fp.read())
            mimage.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(frame))
            mroot.attach(mimage)

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.starttls()
    print("SMTP login username:", username)
    smtp.login(username, password)
    smtp.sendmail(fromaddr, toaddr, mroot.as_string())
    smtp.quit()

def parse_args():
    global imgdir
    global toaddr
    global fromaddr
    global subject
    global smtpserver
    global username
    global password
    global capture_src
    global delay_ms
    global cam_res_x
    global cam_res_y
    global cam_dev_id
    global burst_frames

    parser = argparse.ArgumentParser()
    parser.add_argument("--imgdir", help="local image directory",
                        type=str)
    parser.add_argument("--toaddr", help="destination email address",
                        type=str)
    parser.add_argument("--fromaddr", help="source email address",
                        type=str)
    parser.add_argument("--subject", help="email subject",
                        type=str)
    parser.add_argument("--smtpserver", help="SMTP server",
                        type=str)
    parser.add_argument("--username", help="username",
                        type=str)
    parser.add_argument("--password", help="password",
                        type=str)
    parser.add_argument("--capture_src", help="capture source",
                        type=str)
    parser.add_argument("--delay_ms", help="delay milliseconds",
                        type=str)
    parser.add_argument("--cam_res_x", help="camera resolution x",
                        type=int)
    parser.add_argument("--cam_res_y", help="camera resolution y",
                        type=int)
    parser.add_argument("--cam_dev_id", help="camera device id",
                        type=str)
    parser.add_argument("--burst_frames", help="number of images to take in a burst",
                        type=int)

    args = parser.parse_args()
    print(args)

    if args.imgdir:
        imgdir = args.imgdir
    if args.toaddr:
        toaddr = args.toaddr
        fromaddr = args.toaddr
    if args.fromaddr:
        fromaddr = args.fromaddr
    if args.subject:
        subject = args.subject
    if args.smtpserver:
        smtpserver = args.smtpserver
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    if args.capture_src:
        capture_src = capture_src
    if args.delay_ms:
        delay = datetime.timedelta(milliseconds=args.delay_ms)
    if args.cam_res_x:
        cam_res[0] = args.cam_res_x
    if args.cam_res_y:
        cam_res[1] = args.cam_res_y
    if args.cam_dev_id:
        cam_dev_id = cam_dev_id
    if args.burst_frames:
        burst_frames = args.burst_frames

def main():
    parse_args()
    imgs = capture_imgs()
    email(imgs)

if __name__ == "__main__":
    main()
