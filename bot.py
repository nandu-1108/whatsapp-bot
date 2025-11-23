from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def sms_reply():
    incoming_msg = request.values.get("Body", "").lower()

    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg:
        msg.body("Hello! How can I help you?")
    elif "hi" in incoming_msg:
        msg.body("Hi! 😊")
    elif "time" in incoming_msg:
        msg.body("Sorry, I can't tell time yet 😅")
    elif "bye" in incoming_msg:
        msg.body("Goodbye! 👋")
    else:
        msg.body("I didn't understand that.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
