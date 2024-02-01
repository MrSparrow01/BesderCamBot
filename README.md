# CameraBot

This bot works with any camera that has **AlertServer** configured to the server's IP. Using _asyncio_ and _telebot_, you can receive **Human Detection** notifications. To simplify sending, the frequency of notifications is set to 1 per minute using _regex_.

Alert data from camera looks like: `b'\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x05\xc1\x00\x00\x00{ "Address" : "0x0A01A8C0", "Channel" : 0, "Descrip" : "", "Event" : "HumanDetect", "SerialID" : "cdf680a9a0279bf8", "StartTime" : "2024-01-27 21:10:58", "Status" : "Start", "Type" : "Alarm" }\n'`

In `CHAT_ID` you can paste own chat's or group's id.

# Additionally 

Enabling and disabling notifications and logs were added.
