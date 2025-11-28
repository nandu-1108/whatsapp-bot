from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import random
from datetime import datetime

app = Flask(__name__)

# per-user game state
number_game = {}
quiz_game = {}
chat_history = []

greetings = [
    "🤗 Heyyy friend! I’m so happy you texted me!",
    "🌈 Hiiiii! You made my day brighter!",
    "😄 Hello superstar! How are you feeling today?"
]

happy_replies = [
    "😊 Your happiness is contagious! I love that vibe!",
    "✨ Stay smiling, you’re shining like a star!",
]

sad_replies = [
    "💛 Aww, come here, virtual hug for you 🤗",
    "🌧️ It’s okay to feel sad. I’m here with you."
]

angry_replies = [
    "😌 Take a deep breath with me… in… out…",
    "🧘 You are powerful when calm, my friend."
]

jokes = [
    "😂 Why did the phone go to school? Because it lost its contacts!",
    "🤣 I told my pillow a joke… now it can’t sleep!"
]

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    # Normalize incoming text
    incoming_msg = request.values.get("Body", "") or ""
    text = incoming_msg.strip().lower()
    user = request.values.get("From", "unknown")
    chat_history.append(text)

    resp = MessagingResponse()
    msg = resp.message()

    # ---- greetings ----
    if text in ("hi", "hello", "hlo", "hey"):
        msg.body(random.choice(greetings) + "\nType 'menu' to see what we can do 💖")
        return str(resp)

    # ---- menu ----
    if text == "menu":
        msg.body(
            "🤖 FUN BOT MENU\n"
            "1 - Talk to me 😊\n"
            "2 - Games 🎮\n"
            "3 - Date & Time 🕒\n"
            "4 - Jokes 😂\n"
            "5 - Chat History 🧾\n\n"
            "Reply with the number or keywords (e.g. 'games')."
        )
        return str(resp)

    # ---- talk to me (option 1) ----
    if text in ("1", "talk", "talk to me", "talk to me 😊"):
        msg.body("Tell me your mood: happy / sad / angry")
        return str(resp)

    if "happy" in text:
        msg.body(random.choice(happy_replies))
        return str(resp)

    if "sad" in text:
        msg.body(random.choice(sad_replies))
        return str(resp)

    if "angry" in text:
        msg.body(random.choice(angry_replies))
        return str(resp)

    # ---- games menu (option 2) ----
    if text in ("2", "games", "game"):
        msg.body(
            "🎮 GAMES MENU\n"
            "a - Number Guessing\n"
            "b - Rock Paper Scissors\n"
            "c - Dice Roll\n"
            "d - Coin Toss\n"
            "e - Simple Quiz\n\n"
            "Type a/b/c/d/e to start a game."
        )
        return str(resp)

    # ---- Game A: Number Guessing (user types 'a') ----
    if text == "a":
        number_game[user] = random.randint(1, 10)
        msg.body("🎯 I picked a number between 1-10. Reply with your guess (just the number).")
        return str(resp)

    if user in number_game:
        # expecting a numeric guess
        try:
            guess = int(text)
            real = number_game[user]
            if guess == real:
                msg.body("🎉 WOW! You guessed it right!")
            else:
                msg.body(f"❌ Wrong! The number was {real}. Type 'a' to play again.")
            del number_game[user]
        except ValueError:
            msg.body("Please reply with a number between 1 and 10.")
        return str(resp)

    # ---- Game B: Rock Paper Scissors (user types 'b') ----
    if text == "b":
        msg.body("Type: rock / paper / scissors")
        return str(resp)

    if text in ("rock", "paper", "scissors"):
        bot = random.choice(["rock", "paper", "scissors"])
        # Determine winner (simple)
        result = "Tie!"
        if (text == "rock" and bot == "scissors") or (text == "paper" and bot == "rock") or (text == "scissors" and bot == "paper"):
            result = "You win! 🎉"
        elif text == bot:
            result = "It's a tie 🤝"
        else:
            result = "I win 🤖"
        msg.body(f"🤖 I chose: {bot}\n{result}")
        return str(resp)

    # ---- Game C: Dice (user types 'c') ----
    if text == "c":
        roll = random.randint(1, 6)
        msg.body(f"🎲 Dice rolled: {roll}")
        return str(resp)

    # ---- Game D: Coin Toss (user types 'd') ----
    if text == "d":
        coin = random.choice(["Heads", "Tails"])
        msg.body(f"🪙 {coin}")
        return str(resp)

    # ---- Game E: Simple Quiz (user types 'e') ----
    if text == "e":
        quiz_game[user] = {"q": "What is 5 + 3?", "a": "8"}
        msg.body("🧠 Quiz: What is 5 + 3?")
        return str(resp)

    if user in quiz_game:
        answer = quiz_game[user]["a"]
        if text == answer:
            msg.body("✅ Correct! You’re smart!")
        else:
            msg.body(f"❌ Wrong! The correct answer is {answer}.")
        del quiz_game[user]
        return str(resp)

    # ---- date & time (option 3) ----
    if text in ("3", "time", "date", "date & time"):
        now = datetime.now()
        msg.body(f"🕒 Time: {now.strftime('%H:%M:%S')}\n📅 Date: {now.strftime('%d-%m-%Y')}")
        return str(resp)

    # ---- jokes (option 4) ----
    if text in ("4", "jokes", "joke"):
        msg.body(random.choice(jokes))
        return str(resp)

    # ---- chat history (option 5) ----
    if text in ("5", "history", "chat history"):
        last = "\n".join(chat_history[-6:])
        msg.body("🧾 Last messages:\n" + (last or "No history yet."))
        return str(resp)

    # ---- fallback ----
    fallback = [
        "😄 Haha, you’re fun to talk to!",
        "🤗 Tell me more!",
        "🌈 I love chatting with you!",
        "😎 Interesting! Go on..."
    ]
    msg.body(random.choice(fallback))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
