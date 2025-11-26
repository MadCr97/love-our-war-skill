from flask import Flask, request, jsonify
import random
import re

app = Flask(__name__)

# Very simple in-memory state: user_id -> mode ("party" or "normal")
user_modes = {}

# Chaos lists
PARTY_CHAOS = [
    "🍻 If you’ve ever lied on a dating app, finish your drink.",
    "🍻 For the next 2 minutes, drink 1 sip every time someone laughs.",
    "🍻 Judge takes 2 sips, or gives them to another player.",
    "🍻 Swap drinks with the player on your left, then take 1 sip.",
    "🍻 Do a 10-second dance move, or take 2 sips.",
    "🍻 Speak in a silly accent until your next turn, or take 1 sip.",
    "🍻 Everyone points at someone; the person with the most fingers drinks.",
    "🍻 Pick a word; anyone who says it drinks.",
    "🍻 If you’ve ever ghosted someone, finish your drink.",
    "🍻 Everyone drinks 1 sip.",
    "🍻 Count from 1 to 20 in random order; players who say the same number drink 1 sip, and anyone who stays silent finishes their drink.",
    "🍻 Make a face that matches a bot-chosen emoji; fail and take 1 sip.",
    "🍻 Ask a player a question; if they hesitate, they drink 2 sips.",
    "🍻 Show a dance move, the player on your right imitates it; the chain continues. First player to mess up drinks 2 sips.",
    "🍻 Build a story together, one sentence each; if you hesitate, take 1 sip.",
    "🍻 Everyone sings a song containing the given word; if you run out of ideas, take 2 sips.",
    "🍻 Everyone stands up; the last one drinks 2 sips.",
    "🍻 When the host shouts “Freeze!”, anyone who moves drinks 1 sip.",
    "🍻 Give a player a dare; if they refuse, they drink 2 sips.",
    "🍻 Find something red; the slowest player drinks 1 sip.",
    "🍻 Put all phones in the center; first notification drinks 1 sip.",
    "🍻 Everyone drinks 2 sips.",
    "🍻 Everyone drinks 3 sips.",
    "🍻 Whisper a word around the circle; if the last version is totally different, everyone drinks 1 sip.",
    "🍻 Pick a player for a staring contest; first to blink drinks 1 sip.",
    "🍻 Bring an item matching the bot’s description; the slowest player drinks 1 sip."
]

NORMAL_CHAOS = [
    "☠️ Everyone says a fun fact about themselves; if you can’t think of one, you skip your next turn.",
    "☠️ Describe an object in the room without naming it; first to guess gets 1 point.",
    "☠️ Make a sound effect and everyone must repeat it; worst imitation loses 1 point.",
    "☠️ Tell a tiny 3-word story; funniest one wins a point.",
    "☠️ The bot chooses a color; everyone points at something in that color. Slowest loses 1 point.",
    "☠️ Everyone does a mini pose; best pose wins 1 point.",
    "☠️ Say a compliment to the person on your right; hesitate and you lose 1 point.",
    "☠️ Everyone draws something in the air with their finger; prettiest wins 1 point.",
    "☠️ Whisper a word around the circle; if the last version is totally different, everyone loses 1 point.",
    "☠️ The bot gives a letter; everyone says a word starting with it. If you repeat a word already said, you lose 1 point.",
    "☠️ Everyone shares a tiny goal for today; the sweetest one gets 1 point.",
    "☠️ Everyone mimics an emotion (joy, surprise, confusion…); best imitation wins 1 point.",
    "☠️ Describe your day in exactly five words; most creative one gets 1 point.",
    "☠️ Count from 1 to 20 in random order; players who say the same number lose 1 point, and anyone who stays silent loses 3 points.",
    "☠️ Describe your ideal hangout with someone you care about; most heart-melting idea wins 1 point.",
    "☠️ Everyone says a “green flag” they love in people; the bot picks the sweetest for 1 point.",
    "☠️ Tell a chaotic but harmless icks-inspired story; driest story loses 1 point.",
    "☠️ Make your best “I’m jealous but pretending I’m not” expression; the most obvious loses 1 point.",
    "☠️ Build a story together, one sentence each; if you freeze, lose 1 point.",
    "☠️ Everyone stands up; last one loses 1 point.",
    "☠️ Put all phones in the center; first one to light up loses 1 point.",
    "☠️ When the bot says “Freeze!”, anyone who moves loses 1 point.",
    "☠️ Pick a word; anyone who says it in the next round loses 1 point.",
    "☠️ Find something heart-shaped or cute; slowest player loses 1 point.",
    "☠️ Show a dance move; the next player copies it, and so on. First to mess up loses 1 point."
]


# ---------------------------------------------------------
# 🔥 FIX PARA QUE NO SE CORTEN PALABRAS EN KAKAO
# ---------------------------------------------------------
def clean_text(text: str) -> str:
    """Removes invisible characters and fixes awkward line breaks."""
    # Eliminar caracteres invisibles
    text = re.sub(r"[\u2028\u2029\u200b\u2060]", "", text)

    # Reemplazar saltos de línea internos por espacios
    text = text.replace("\n", " ")

    # Evitar acumulación de espacios dobles
    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


def simple_text(text: str) -> dict:
    """Build Kakao simpleText JSON response (cleaned)."""
    text = clean_text(text)      # ← AQUI SE APLICA EL FIX

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
        "🍻PARTY MODE ON!🍻\n\n"
        "Chaos effects may now include drinking actions or social dares.\n\n"
        "You can switch modes at any time by typing 'PARTY OFF'.\n\n"
        "Whenever you want a chaos event, type: CHAOS"
    )
    return jsonify(simple_text(text))


@app.route("/party_off", methods=["POST"])
def party_off():
    body = request.get_json(force=True)
    user_id = get_user_id(body)

    user_modes[user_id] = "normal"

    text = (
        "✨PARTY MODE OFF!✨\n\n"
        "Chaos effects will now be clean and alcohol-free.\n\n"
        "You can switch modes at any time by typing 'PARTY ON'.\n\n"
        "Whenever you want a chaos event, type: CHAOS"
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

