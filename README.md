# Conversational_AI
 
1. Install all the dependencies provided in requirements.txt<br>
   -- Command line for windows cmd --<br>
   pip install -r requirements.txt<br>

2. Train the model with rasa<br>
   -- Command line for windows cmd --<br>
   rasa train<br>

3. Start the rasa server<br>
   -- Command line for windows cmd --<br>
   rasa run<br>

4. Start the actions server in another command prompt window<br>
   -- Command line for windows cmd --<br>
   rasa run actions<br>

5. Start ngrok server in another command prompt window<br>
   -- Command line for windows cmd --<br>
   ngrok http 5005<br>

6. Copy the Forwarding URL value - <copy value 1><br>
   Forwarding                    https://****-**-***-**-**.ngrok.io<br>

## Facebook integration

1. Open credentials.yml copy the value of verify from facebook - <copy value 2><br>
   facebook:<br>
    verify: <copy this value><br>

2. Navigate to the page "https://developers.facebook.com/"
3. Login using meta developer credentials
4. Go to my apps
5. Click on MessengerBot
6. On the left pane select Settings of Messenger under Products
7. Click on Edit callback URL in Webhooks
8. Paste <copy value 1> in Callback URL as below:<br>
   <copy value 1>/webhooks/facebook/webhook
9. Paste <copy value 2> in Verfiy token
10. Click Verify and save

Open the EduBot page, click on Message and have a chat with it and get your recommendation.<br>
Please make sure you wake up the bot by saying Hi
    
