from llama_cpp import Llama


class LlamaChat:
    def __init__(
        self, model_path: str, chat_format: str = "chatml", temperature: float = 0.7
    ):
        """
        Initialize the Llama model.
        :param model_path: Path to the Llama model file.
        :param chat_format: Chat format, default is 'chatml'.
        :param temperature: Sampling temperature for the model.
        """
        self.llm = Llama(model_path=model_path, chat_format=chat_format)
        self.temperature = temperature
        print("Llama model initialized.")

    def send_message(self, user_message: str):
        """
        Send a message to the Llama model and get the response.
        :param user_message: The user's input message.
        :return: Response from the Llama model.
        """
        try:
            response = self.llm.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that outputs in JSON. you should always return a list of 3 valid movie names.",
                    },
                    {"role": "user", "content": user_message},
                ],
                response_format={
                    "type": "json_object",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "general_response": {"type": "string"},
                            "movies": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 3,
                                "maxItems": 3,
                            },
                        },
                        "required": ["general_response", "movies"],
                    },
                },
                temperature=self.temperature,
            )

            if response:
                return response["choices"][0]["message"]["content"]
            else:
                return "No response from the model."
        except Exception as e:
            return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    model_path = "./Meta-Llama-3-8B-Instruct.Q2_K.gguf"
    llama_chat = LlamaChat(model_path=model_path)

    print("You can now ask questions. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = llama_chat.send_message(user_input)
        print("Llama: ", response)