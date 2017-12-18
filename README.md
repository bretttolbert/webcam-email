Basic usage:
```
python webcam_email.py --toaddr="recipient@gmail.com" --username="sender@gmail.com" --password="topsecret" --subject="webcam test"
```

By default it assumes Gmail and uses ```--smtpserver="smtp.gmail.com:587"```. Try it once, then check sender inbox for a "Review blocked sign-in attempt" message from Google. It will give you a link to "allow access to insecure apps". Using your primary google account for sending is possible but not recommended. Instead, create a throwaway account to use for sending. You can then use that account to send to your primary email account. 

Help:
```
python webcam_capture_and_email.py -h
usage: webcam_capture_and_email.py [-h] [--imgdir IMGDIR] [--toaddr TOADDR]
                                   [--fromaddr FROMADDR] [--subject SUBJECT]
                                   [--smtpserver SMTPSERVER]
                                   [--username USERNAME] [--password PASSWORD]
                                   [--capture_src CAPTURE_SRC]
                                   [--delay_ms DELAY_MS]
                                   [--cam_res_x CAM_RES_X]
                                   [--cam_res_y CAM_RES_Y]
                                   [--cam_dev_id CAM_DEV_ID]
                                   [--burst_frames BURST_FRAMES]

optional arguments:
  -h, --help            show this help message and exit
  --imgdir IMGDIR       local image directory
  --toaddr TOADDR       destination email address
  --fromaddr FROMADDR   source email address
  --subject SUBJECT     email subject
  --smtpserver SMTPSERVER
                        SMTP server
  --username USERNAME   username
  --password PASSWORD   password
  --capture_src CAPTURE_SRC
                        capture source
  --delay_ms DELAY_MS   delay milliseconds
  --cam_res_x CAM_RES_X
                        camera resolution x
  --cam_res_y CAM_RES_Y
                        camera resolution y
  --cam_dev_id CAM_DEV_ID
                        camera device id
  --burst_frames BURST_FRAMES
                        number of images to take in a burst

```

Supported capture sources:

* ```fswebcam```      # Linux option 1
* ```pygame```        # Linux option 2 (PyGame + OpenCV)
* ```videocapture```  # Windows option <http://videocapture.sourceforge.net/>

Installing fswebcam:
```
sudo apt install fswebcam
fswebcam -d /dev/video0 -r 640x480 test.jpg
xdg-open test.jpg
```

List webcam resolutions
```
sudo apt install uvcdynctrl
uvcdynctrl -l
```