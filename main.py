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


@app.route("/loveourwar", methods=["POST"])
def love_our_war():
    body = request.get_json(force=True)

    # Get user ID (to remember mode per user)
    user_id = (
        body.get("userRequest", {})
        .get("user", {})
        .get("id", "anonymous")
    )

    action = body.get("action", {})
    params = action.get("params", {})
    # We will send a "mode" param from Kakao blocks
    mode_param = params.get("mode", "")

    # 1) PARTY ON
    if mode_param == "party_on":
        user_modes[user_id] = "party"
        text = (
            "🍻 PARTY MODE ON!\n\n"
            "Chaos effects may now include drinking actions or social dares.\n"
            "Whenever you want a chaos event, type CHAOS."
        )
        return jsonify(simple_text(text))

    # 2) PARTY OFF
    if mode_param == "party_off":
        user_modes[user_id] = "normal"
        text = (
            "✨ PARTY MODE OFF!\n\n"
            "Chaos effects will now be clean and alcohol-free.\n"
            "Whenever you want a chaos event, type CHAOS."
        )
        return jsonify(simple_text(text))

    # 3) CHAOS
    if mode_param == "chaos":
        current_mode = user_modes.get(user_id, "normal")
        if current_mode == "party":
            text = random.choice(PARTY_CHAOS)
        else:
            text = random.choice(NORMAL_CHAOS)

        return jsonify(simple_text(text))

    # Fallback if something weird happens
    text = (
        "I’m not sure what you want.\n"
        "Try PARTY ON, PARTY OFF, or CHAOS again."
    )
    return jsonify(simple_text(text))


if __name__ == "__main__":
    # Replit usually sets PORT automatically, but 8000 is fine.
    app.run(host="0.0.0.0", port=8000)
