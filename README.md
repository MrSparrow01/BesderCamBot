# Bot for Besder IP Camera

This bot works with any camera that has **AlertServer** configured to the server's IP. In this example I use **Besder IP Camera**. Using _asyncio_ and _telebot_, you can receive **Human Detection** notifications. To simplify sending, the frequency of notifications is set to 1 per minute using _regex_.

In `CHAT_ID` you can paste own privates's or group's id.

> [!IMPORTANT]
> You need to create your bot via [BotFather](https://t.me/BotFather) and set it and chat's id as secrets on [fly.io](https://fly.io/). Also, add an server's IP from fly.io to your camera settings.

> [!TIP]
> Alert data from camera looks like: `b'\xff\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4\x05\xc1\x00\x00\x00{ "Address" : "0x0A01A8C0", "Channel" : 0, "Descrip" : "", "Event" : "HumanDetect", "SerialID" : "cdf680a9a0279bf8", "StartTime" : "2024-01-27 21:10:58", "Status" : "Start", "Type" : "Alarm" }\n'`

# Additionally 

Enabling and disabling notifications and logs were added.

<p align="center">
  <img src="https://github.com/MrSparrow01/CameraBot/assets/92633536/aded1ccd-8e2b-49db-805d-44e6a991f158" alt="Message example">
</p>


