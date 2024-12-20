from flask import Flask, request, jsonify, render_template, Response
from model import LlamaChat
from flask_cors import CORS

# Initialize the model once
model_path = "./Lexi-Llama-3-8B-Uncensored_Q5_K_M.gguf"
llama_chat = LlamaChat(model_path=model_path)

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if "query" not in data:
        return jsonify({"error": "Missing 'query' field in the request body"}), 400
    user_query = data["query"]
    preMessage = data["preMessage"]
    schema = data["schema"]
    response = llama_chat.get_movie_suggestions(user_query, preMessage, schema)
    if response:
        return response,200
    return jsonify({"error": "Failed to generate a response"}), 500


@app.route("/chat", methods=["POST"])
def chat():
    # Get the messages from the request
    data = request.json
    messages = data.get("messages", [])
    preMessage = data.get("preMessage", "You are a helpful assistant.")
    schema = data.get("schema", None)
    def generate_response():
        for chunk in llama_chat.send_message(messages, preMessage, schema):
            yield chunk  # Send each chunk to the frontend

    # Return the streaming response
    return Response(generate_response(), content_type="text/plain")

@app.route("/story", methods=["POST"])
def story():
    data = request.get_json()
    if "name" not in data:
        return jsonify({"error": "Missing 'name' field in the request body"}), 400
    if "topic" not in data:
        return jsonify({"error": "Missing 'topic' field in the request body"}), 400
    name = data["name"]
    topic = data["topic"]
    systemPrompt = data.get("systemPrompt", "You are a Children's book author.")
    assistantPrompts = data.get(
        "assistantPrompts",
        [
            "You are a Children's book author.",
            "you should always reply the user with a new unique story that you generate on the spot.",
            "avoid using gender specific terms, instead of boy or girl, use kid for example. use 'they' pronounce.",
            "the main character of the story is the name of the user given to you on the prompt.",
            "try to teach the kid about the topic given to you.",
            "the story should be positive and appropriate for kids.",
            "the story should be at least 2500 words long.",
        ],
    )
    print("systemPrompt", assistantPrompts)
    prompt = data.get("prompt", f"the name of the child is {name}. teach them an important lesson about {topic}, by writing a new story for them.")
    # prompt = "hey there how are you doing? please tell me a story",
    schema = data.get(
        "schema",
        {
            "type": "string",
            "description": "This response must be a plain text story written in English.",
        },
    )
    # print("schema", schema)
    # print("prompt", prompt)
    # # print("systemPrompt", systemPrompt)
    # print("assistantPrompts", assistantPrompts)
    response = llama_chat.generate_story(prompt=prompt, systemPrompt=systemPrompt ,assistantPrompts=assistantPrompts, schema=schema)
    return jsonify(response)
@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234)
