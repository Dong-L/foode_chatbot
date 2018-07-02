#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAI7rFN3VwgBAPEWabCGV5GbSrWIAtLf2elh4hCOQElZBR5FHp15tCVqaXZBANrtzK2ZCmdhPDNZBCVtCwrKSxg7JnnEu51CZBqbmTnY5Vui99PtB0t9v5ZB2XjkC4d3A5sNwvq0vxMNMEIfnnkjF7xNFS5dKN1kqgQfGZBFbmXrNZBPCzePvtIv'
VERIFY_TOKEN = 'u++57drXp8pWo8blt7Ym+vffSOLFGS2C/GfKYTGKKJo='
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#chooses an automated response to the message depending on the substance of the message
def get_automated_message(message):
    response = "With FoodE, you have a ton of options to choose from. Visit our facebook here: https://www.facebook.com/FoodEOfficial/"
    response_2 = "You can contact us by emailing foodEofficial@gmail.com with any comments or concerns. Also, feel free to reach out to us on instagram @foodEOfficial!/"
    about = "FoodE is a fun and innovative way to connect with local restaurants in order to get the delicious meals you deserve. \
                Eating out has never been so easy and accessible. Save the meals you want, discard the ones you don't."
    dev_message = "FoodE is still in development, but like us on FaceBook, follow us on Instagram, and sign up for our mailing \
                list to stay up to date on the latest versions of the app."
    if "restaurant" || "food" || "eat" in message:
                return response
    elif "problem" || "complaint" || "confused" || "help" in message:
                return response_2
    elif "what" and ("foode" or "this") in message.lower():
                return about
    elif "when" and ("foode" or "app" or "release") in message.lower():
                return dev_message
    else: 
                return "I'm sorry, we don't quite understand."
                

     
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
