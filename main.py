from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Very simple in-memory state: user_id -> mode ("party" or "normal")
user_modes = {}

# Chaos lists
PARTY_CHAOS = [
    "CHAOS (Party Mode): Take one drink if you played a Red Flag.",
    "CHAOS (Party Mode): The player with the lowest Love Points takes a sip.",
    "CHAOS (Party Mode): Swap drinks with the player on your right.",
    "CHAOS (Party Mode): The Judge drinks if they choose a Green Flag."
]

NORMAL_CHAOS = [
    "CHAOS (Normal Mode): The Judge must pick the worst response this round.",
    "CHAOS (Normal Mode): Swap hands with the player on your left.",
    "CHAOS (Normal Mode): Everyone discards one card and draws a new one.",
    "CHAOS (Normal Mode): All Red Flags score +4 instead of +3 this round."
]


def simple_text(text: str) -> dict:
    """Build Kakao simpleText JSON response."""
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ]
        }
    }


def get_user_id(body):
    return (
        body.get("userRequest", {})
        .get("user", {})
        .get("id", "anonymous")
    )


@app.route("/party_on", methods=["POST"])
def party_on():
    body = request.get_json(force=True)
    user_id = get_user_id(body)

    user_modes[user_id] = "party"

    text = (
        "🍻 PARTY MODE ON!\n\n"
        "Chaos effects may now include drinking actions or social dares.\n"
        "You can switch modes at any time by typing “PARTY OFF”.\n\n"
        "Whenever you want a chaos event, type:\n"
        "• CHAOS"
    )
    return jsonify(simple_text(text))


@app.route("/party_off", methods=["POST"])
def party_off():
    body = request.get_json(force=True)
    user_id = get_user_id(body)

    user_modes[user_id] = "normal"

    text = (
        "✨ PARTY MODE OFF!\n\n"
        "Chaos effects will now be clean and alcohol-free.\n"
        "You can switch modes at any time by typing “PARTY ON”.\n\n"
        "Whenever you want a chaos event, type:\n"
        "• CHAOS"
    )
    return jsonify(simple_text(text))


@app.route("/chaos", methods=["POST"])
def chaos():
    body = request.get_json(force=True)
    user_id = get_user_id(body)

    current_mode = user_modes.get(user_id, "normal")

    if current_mode == "party":
        text = random.choice(PARTY_CHAOS)
    else:
        text = random.choice(NORMAL_CHAOS)

    return jsonify(simple_text(text))


@app.route("/", methods=["GET"])
def health():
    return "LOVE Our WAR skill is running.", 200
