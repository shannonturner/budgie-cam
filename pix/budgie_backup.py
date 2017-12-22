from index_consts import HEADER, FOOTER
from PIL import Image
from StringIO import StringIO
import os.path
import re
import requests
import subprocess
import time

###################################################################
# CONFIGURATION DETAILS - EDIT THESE TO MATCH YOUR CONFIGURATION! #
###################################################################

# Publicly-accessible web address of all of the pictures and videos
# Example as used in the README: http://123.45.67.89:XXXXX/budgiecam
WEB_ADDRESS = ''

# What folder should we save our pictures to?
SAVE_FOLDER = '/Users/shannon/Dropbox/github/budgiecam/pix/'

###################################################################
########################## END  EDITABLE ##########################
###################################################################

try:
    # Sure, I could set WEB_ADDRESS to a static internal IP at 192.168.1.XXX
    # But this will alert me if the IP address changes, so I can fix it
    source = requests.get(WEB_ADDRESS).text
except Exception:
    print "[ERROR] Failed to fetch source!"
    print "\n\n[WARN] Did the external IP address of the Raspberry Pi change? \n\n"
    raise
else:
    print "[OK] Fetched source!"

print "[OK] Fetching pictures!"
with open("{0}index.html".format(SAVE_FOLDER), "w") as index_file:
    index_file.write(HEADER)

    for picture in re.finditer('href\="(\d+\.(png|jpg))"', source): # href="2016629171422.png"

        # Fetch all JPG/PNG images
        if not (os.path.isfile("{0}saved/{1}".format(SAVE_FOLDER, picture.group(1)))):
            try:
                time.sleep(1)
                r = requests.get("{0}/{1}".format(WEB_ADDRESS, picture.group(1)))
            except Exception:
                print "[ERROR] Failed to fetch: {0}".format(picture.group(1))
            else:
                try:
                    i = Image.open(StringIO(r.content))
                    i.save("{0}saved/{1}".format(SAVE_FOLDER, picture.group(1)))
                except Exception, e:
                    print "[WARN] Failed to save image ({0}): {1} for {2}{0}".format(picture.group(1), e, WEB_ADDRESS)
                    raw_input("[DEBUG] Press ENTER to continue")

        index_file.write('<div class="col-lg-4"><img src="saved/{0}" class="img-responsive"></div>'.format(picture.group(1)))

    index_file.write(FOOTER)


print "[OK] Fetching videos!"
for video in re.finditer('href\="(\d+\.(h264))"', source):
    if not (os.path.isfile("{0}videos/{1}".format(SAVE_FOLDER, video.group(1)))):
        try:
            time.sleep(1)
            print "\t Fetching {0}".format(video.group(1))
            r = requests.get("{0}/{1}".format(WEB_ADDRESS, video.group(1)), stream=True)
        except Exception:
            print "[ERROR] Failed to fetch: {0}".format(video.group(1))
        else:
            try:
                print "\t Saving local copy of {0}".format(video.group(1))
                with open("{0}videos/{1}".format(SAVE_FOLDER, video.group(1)), "w") as video_file:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            video_file.write(chunk)
            except Exception, e:
                print "[WARN] Failed to save video ({0}): {1}".format(video.group(1), e)

    # Has this video been converted yet?
    if not (os.path.isfile("{0}videos/{0}.mp4".format(SAVE_FOLDER, video.group(1)[:-5]))):
        try:
            print "\t Converting {0} to mp4".format(video.group(1))
            subprocess.call([
                'ffmpeg',
                '-i',
                '{0}videos/{1}'.format(SAVE_FOLDER, video.group(1)),
                "{0}videos/{1}.mp4".format(SAVE_FOLDER, video.group(1)[:-5])
            ])
        except Exception:
            print "[ERROR] Failed to convert {0} to mp4".format(video.group(1))
