from flask import Flask, render_template, request, jsonify
from watsonx_helper import get_ai_response

app = Flask(__name__)

# Store user conversation states in memory (simple version)
user_context = {
    "step": 0,
    "device_type": None,
    "device_category": None,
    "budget": None
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"].strip().lower()

    # 🟢 Reset or start conversation on page load or "start" message
    if user_context["step"] == 0 or user_message == "start":
        user_context.update({"step": 1, "device_type": None, "device_category": None, "budget": None})
        return jsonify({"reply": "👋 Hi, I’m your AI Device Selector! What type of device are you looking for? (Laptop, Mobile, Tablet)"})

    # Step 2: Save device type
    elif user_context["step"] == 1:
        if "laptop" in user_message:
            user_context["device_type"] = "laptop"
            user_context["step"] = 2
            return jsonify({"reply": "Got it! What type of laptop do you need? (Gaming, Office, Student, ThinkPad)"})
        elif "mobile" in user_message or "phone" in user_message:
            user_context["device_type"] = "mobile"
            user_context["step"] = 2
            return jsonify({"reply": "Cool! What type of mobile are you looking for? (Gaming, Camera, Budget, Flagship)"})
        elif "tablet" in user_message:
            user_context["device_type"] = "tablet"
            user_context["step"] = 2
            return jsonify({"reply": "Alright! What kind of tablet do you need? (Drawing, Study, Entertainment, Productivity)"})
        else:
            return jsonify({"reply": "Please choose either Laptop, Mobile, or Tablet."})

    # Step 3: Save category/type
    elif user_context["step"] == 2:
        user_context["device_category"] = user_message
        user_context["step"] = 3
        return jsonify({"reply": "Nice! What’s your budget range? (e.g., under ₹50k, ₹50k–₹1L, above ₹1L)"})

    # Step 4: Save budget and show filtered devices
    elif user_context["step"] == 3:
        user_context["budget"] = user_message
        user_context["step"] = 4

        # 🧠 Watsonx filter prompt for recommendations
        filters = (
            f"You are an expert tech advisor. Suggest 3 best {user_context['device_category']} "
            f"{user_context['device_type']}s under the budget {user_context['budget']}. "
            f"Include brand names and a one-line feature summary for each device. "
            f"Return the response in numbered list format like:\n"
            f"1. <Device Name> — <short description>\n"
            f"2. <Device Name> — <short description>\n"
            f"3. <Device Name> — <short description>"
        )

        reply = get_ai_response(filters)

        # 🧩 Format the reply into a clean list (with line breaks)
        formatted_reply = (
            reply.replace("1.", "<br><br>1️⃣ ")
                 .replace("2.", "<br>2️⃣ ")
                 .replace("3.", "<br>3️⃣ ")
        )

        return jsonify({"reply": formatted_reply})

    # Step 5: Reset after recommendation
    elif user_context["step"] == 4:
        user_context.update({"step": 0, "device_type": None, "device_category": None, "budget": None})
        return jsonify({"reply": "Would you like to search for another device?"})

if __name__ == "__main__":
    app.run(debug=True)
