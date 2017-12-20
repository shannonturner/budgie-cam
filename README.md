## Budgie Cam

Send a text message -> receive a picture of your beautiful bird!

![alt text](https://github.com/shannonturner/budgie-cam/raw/master/images/beakin-that-toy.jpg "My little guy beakin' that toy")

## Repeatable instructions to get your budgie-cam up and running!

### Shopping List: $90

* [Raspberry Pi 3 - Model B - ARMv8 with 1G RAM: $35](https://www.adafruit.com/product/3055)
* [5V 2.4A Switching Power Supply w/ 20AWG 6' MicroUSB Cable: $8](https://www.adafruit.com/product/1995)
* [Raspberry Pi Camera Board v2 - 8 Megapixels: $30](https://www.adafruit.com/product/3099)
* [8GB SD Card with Raspbian Jessie Operating System: $12](https://www.adafruit.com/product/2767)
* [Adjustable Pi Camera Mount: $5](https://www.adafruit.com/product/1434)
* [Raspberry Pi Model B+ / Pi 2 / Pi 3 Case Lid - Yellow: $3](https://www.adafruit.com/product/2245)
* [Pi Model B+ / Pi 2 / Pi 3 Case Base - Green: $5](https://www.adafruit.com/product/2251)
* Optional but recommended: [Flex Cable for Raspberry Pi Camera or Display - 300mm / 12": $2](https://www.adafruit.com/product/1648)

### Shopping notes: 
* Depending on your cage and home setup, you may want to choose a different length of flex cable for the Raspberry Pi camera. Note that the longer your cable, the more likely you are to have degraded picture quality. Shorter cables are better here. It's a tradeoff between ease of mounting and picture quality.
* Not included: a way to mount the Pi to your cage or fasten the camera to the cage. Get creative!
* For best results and maximum style, choose a Raspberry Pi case color that matches your budgie's coloration

### How to set up Budgie Cam to run on your Raspberry Pi

1. From the terminal, clone the repository.

`git clone https://github.com/shannonturner/budgie-cam.git`

2. Install virtualenv if you do not currently have it

`sudo pip install virtualenv`

3. Create a virtualenv on the cloned repository.

`virtualenv budgie-cam`

4. Now the virtualenv will be active; you can activate it again later on by running `source bin/activate` from within the budgie-cam directory.

5. With your virtualenv active, install the required Python packages

`pip install -r requirements.txt`

6. Edit the budgiecam/settings.py file and change the SECRET_KEY to be a non-blank string of 50 random characters. You can generate a secret key by running this Python script:

`from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
print get_random_string(50, chars)`

7. Edit the txt2pi/twilio_credentials.py file with your ACCOUNT_SID and AUTH_TOKEN from your Twilio account. (If you don't have a Twilio account yet, you'll need to create one at: twilio.com)

7a. Your Account SID and Auth token are available on your Twilio Dashboard under Project Info: [https://www.twilio.com/console](https://www.twilio.com/console)

8. Make sure that your Raspberry Pi camera is running correctly by running: `raspistill -o` (if it doesn't work you may need to enable the camera and restart your Raspberry Pi by running `sudo raspi-config`)

9. Install Apache according to this guide: [https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md](https://www.raspberrypi.org/documentation/remote-access/web-server/apache.md) -- this will allow you to serve images that Twilio will be able to find.

10. Open a browser and go to [http://localhost](http://localhost) and you should see a "It Works!" page. (If you are running in command-line mode rather than the desktop mode, you can start desktop mode by running `startx`)

11. From your terminal, change your directory to /var/www/html (if that doesn't exist, use /var/www/)

`cd /var/www/html`

12. Create a new folder for your pictures.

`sudo mkdir budgiecam`

13. Change the permissions on your new folder to allow you to add items to this folder. If you are logged in as a different user than `pi`, then substitute your username in place of `pi`.

`sudo chown pi: budgiecam`

14. From your browser, go to [http://192.168.1.1](http://192.168.1.1) to log in to your router. You will need your router's administrator password.

15. Find the IP address of your Raspberry Pi, usually 192.168.1.XXX. Write this down.

16. Find your external-facing IP address (the one that does not begin with 192.168.) Write this down; you'll use this external-facing IP address to tell Twilio where to go. In later steps we will use the example IP address 123.45.67.89 so when you see this, replace it with your own.

Note: If you have a dynamic IP address, your IP address may change without warning and your Budgie Cam may stop working until you update your new IP address in Twilio. This does not happen frequently, but it may happen periodically depending on your internet service provider.

17. You need to set up port forwarding for two ports. Your first port forwarding will allow access to your Apache web server that serves the images taken by your camera.

For my port forwarding, I set up requests to my Raspberry Pi's address with a port of 80 to go to a destination of XXXXX. (In place of XXXXX, use any number you like)

So it looks like:
Raspberry Pi
192.168.1.xxx:80    Destination XXXXX
                    TCP Any -> XXXXX

This will allow my images to be found by Twilio. In place of XXXXX, use any port number you like as long as it is not in use by another service or system.

Your second port forwarding will allow POST requests to go through to the Django server you will be running soon.

It will look like:
Raspberry Pi
192.168.1.xxx:YYYYY Destination YYYYY
                    TCP Any -> YYYYY

Again, which ports you use for XXXXX and YYYYY don't matter much as long as they are not in use by something else.

Your port forwarding system may look different depending on your router.

18. Edit the txt2pi/budgie_settings.py file with your BUDGIE_PASSPHRASE, BUDGIE_FILE_PATH, BUDGIE_WEB_PATH, and RASPI_IP

**BUDGIE_PASSPHRASE:** Budgie Cam will check to make sure that this password exists somewhere in your text message before taking a photo and sending it back. While not essential, it's probably a good idea since this is essentially a camera in your home.

**BUDGIE_FILE_PATH:** This is the file path of where the photos are stored, created in step 12 above. (example: /var/www/html/budgiecam/) If raspistill is unable to save your photos or they are being saved in the wrong place, check this setting and make sure you are using a trailing slash.

**BUDGIE_WEB_PATH:** This is the web path where your images are accessible from the web. If you followed the instructions and are using /var/www/html/budgiecam/ for your BUDGIE_FILE_PATH, your BUDGIE_WEB_PATH is then /budgiecam/. If Twilio is unable to locate your photos, check this setting and make sure that you are using slashes properly.

**RASPI_IP:** This is the external-facing web/IP address of your Raspberry Pi as found in Step 16. This is your also your HOME'S IP ADDRESS so you probably do NOT want to commit this to GitHub (Same with Django's SECRET_KEY). If your IP address changes as noted in Step 16, you will need to update it here and in Twilio. Use the format: http://123.45.67.89:XXXXX where XXXXX is the port number you used in port forwarding in Step 17.

19. Run the Django server:

`./manage.py runserver 0.0.0.0:YYYYY`

Note: Using 0.0.0.0 (instead of localhost) acts as a wildcard, allowing any computer on your network to access the device, which can be useful for testing.

20. Purchase a phone number from Twilio ($1/month) with SMS capability

21. In the [Twilio Console](https://www.twilio.com/console/phone-numbers/incoming), configure your phone number to send a POST request to your Raspberry Pi when it receives an SMS message.

In the Configure tab for your phone number, scroll to the bottom under "Messaging." Where it says "A message comes in", enter the web/IP address of your Raspberry Pi's Django server as noted in Steps 16 and 19. 

If you followed the instructions, yours will be something like: http://123.45.67.89:YYYYY/budgiecam/ where 123.45.67.89 is your IP address from Step 16 and YYYYY is your port number from Step 17. /budgiecam/ is the path used by the Django URL, so you don't want to change it. Be sure to use trailing slashes.

Use HTTP POST as the request type.

Save your phone number's configuration.

22. Let's test to make sure everything is working. From your browser, go to http://localhost:YYYYY/budgiecam and you should see a message saying that your Budgie Cam is configured and ready to go! (Remember to replace YYYYY with the port you used in Step 17)

22a. You can also test to see if your port forwarding worked correctly by opening a browser on a different computer connected to your home router and navigating to http://192.168.1.xxx:YYYYY/budgiecam, where xxx is your Raspberry Pi's IP address and YYYYY is the port you used in Step 17.

23. Save your Twilio phone number in your phone as Budgie Cam so you can send a text message.

24. Send a text message from your phone that includes your BUDGIE_PASSPHRASE from Step 18. Wait about 10-15 seconds. Watch your Django's runserver output to see any logging messages. If all goes well, you should see a 200 POST request. If something went wrong, you'll get a 500 error and a clue with what you need to fix.

25. REJOICE

26. Optional but recommended: Create a startup script so that your Budgie Cam will run automatically when you start your Raspberry Pi without any input from you.

    TODO: STARTUP SCRIPT SO YOU CAN RUN HEADLESS

27. Mount the camera and Pi on your cage and enjoy!

28. If you're still reading this and have completed all of the steps I would love to see your beautiful bird. [https://twitter.com/svthmc](Send pictures) you've taken with your Budgie Cam to me! 