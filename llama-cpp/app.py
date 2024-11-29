from flask import Flask, request, jsonify
from model_cpu import LlamaChat

# Initialize the model once
model_path = "./Meta-Llama-3-8B-Instruct.Q2_K.gguf"
llama_chat = LlamaChat(model_path=model_path)

# Initialize Flask app
app = Flask(__name__)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if "query" not in data:
        return jsonify({"error": "Missing 'query' field in the request body"}), 400
    user_query = data["query"]
    response = llama_chat.send_message(user_query)
    print(response)
    if response:
        return response,200
    return jsonify({"error": "Failed to generate a response"}), 500


if __name__ == "__main__":
    print("Starting the API server. Send requests to http://localhost:1234/ask")
    app.run(host="0.0.0.0", port=1234)
