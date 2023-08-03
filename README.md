# Conversational_AI
 
1. Install all the dependencies provided in requirements.txt\n
   -- Command line for windows cmd --
   pip install -r requirements.txt

2. Train the model with rasa
   -- Command line for windows cmd --
   rasa train

3. Start the rasa server
   -- Command line for windows cmd --
   rasa run

4. Start the actions server in another command prompt window
   -- Command line for windows cmd --
   rasa run actions

5. Start ngrok server in another command prompt window
   -- Command line for windows cmd --
   ngrok http 5005

6. Copy the Forwarding URL value - <copy value 1>
   Forwarding                    https://****-**-***-**-**.ngrok.io

## Facebook integration

1. Open credentials.yml copy the value of verify from facebook - <copy value 2>
   facebook:
    verify: <copy this value>

2. Navigate to the page "https://developers.facebook.com/"
3. Login using meta developer credentials
4. Go to my apps
5. Click on MessengerBot
6. On the left pane select Settings of Messenger under Products
7. Click on Edit callback URL in Webhooks
8. Paste <copy value 1> in Callback URL as below:
   <copy value 1>/webhooks/facebook/webhook
9. Paste <copy value 2> in Verfiy token
10. Click Verify and save

Open the EduBot page, click on Message and have a chat with it and get your recommendation. 
Please make sure you wake up the bot by saying Hi
    
