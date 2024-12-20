from llama_cpp import Llama

class LlamaChat:

    def __init__(
        self,
        model_path: str,
        chat_format: str = "chatml",
        temperature: float = 0.7,
        n_gpu_layers: int = -1,
        n_ctx: int = 4096,
    ):
        """
        Initialize the Llama model.
        :param model_path: Path to the Llama model file.
        :param chat_format: Chat format, default is 'chatml'.
        :param temperature: Sampling temperature for the model.
        """
        self.temperature = temperature
        self.n_gpu_layers = n_gpu_layers
        self.llm = Llama(
            model_path=model_path,
            chat_format=chat_format,
            temperature=temperature,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
        )
        print("Llama model initialized.")

    def get_movie_suggestions(
        self,
        user_message: str,
        preMessage: str = "You are a helpful assistant that outputs in JSON. you should always return a list of 3 valid movie names.",
        schema: map = {
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
    ):
        """
        Suggest movies based on a user message.
        :param user_message: The user's input message.
        :return: Response from the Llama model.
        """
        try:
            response = self.llm.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": preMessage,
                    },
                    {"role": "user", "content": user_message},
                ],
                response_format=schema,
                temperature=self.temperature,
            )

            if response:
                return response["choices"][0]["message"]["content"]
            else:
                return "No response from the model."
        except Exception as e:
            return f"Error: {e}"

    def send_message(
        self,
        messages: list,
        preMessage: str = "You are a helpful assistant.",
        schema: map = None,
        max_tokens: int = 1000,
    ):
        """
        Send an array of messages to the Llama model for a chat-style interaction.
        :param messages: A list of messages in the format [{"role": "user/assistant", "content": "message"}].
        :param preMessage: A system message to define the assistant's role.
        :param schema: Optional schema for validating the response.
        :return: Response from the Llama model.
        """
        try:
            # Include the system message at the start of the conversation
            full_messages = [{"role": "system", "content": preMessage}] + messages

            response_stream = self.llm.create_chat_completion(
                messages=full_messages,
                response_format=schema,
                temperature=self.temperature,
                stream=True,
                max_tokens=max_tokens,
            )
            # Stream the response in chunks
            for chunk in response_stream:
                delta = chunk['choices'][0]['delta']
                if "content" in delta and "<|im_end|>" in delta["content"]:
                    yield "\n"
                elif 'content' in delta and "<im_start>" in delta['content']:
                    yield ""
                elif 'role' in delta:
                    yield f"{delta['role']}: "
                elif 'content' in delta:
                    yield delta['content']
        except Exception as e:
            yield f"Error: {str(e)}"

    def generate_story(
        self,
        prompt: str,
        systemPrompt: str = "You Children's book author.",
        assistantPrompts: list = [
            "You are a Children's book author.",
            "you should always reply the user with a new unique story that you generate on the spot.",
            "avoid using gender specific terms, instead of boy or girl, use kid for example. use 'they' pronounce.",
            "the main character of the story is the name of the user given to you on the prompt.",
            "try to teach the kid about the topic given to you.",
            "the story should be positive and appropriate for kids.",
            "the story should be at least 2500 words long."
        ],
        schema: map = {
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "story": {"type": "string"},
                },
                "required": ["story"],
            },
        },
    ):
        prepareMessages = [{"role": "system", "content": systemPrompt}]
        # prepareMessages = []
        for assistantPrompt in assistantPrompts:
            prepareMessages.append({"role": "assistant", "content": assistantPrompt})
        prepareMessages.append({"role": "user", "content": prompt})
        print(schema)
        try:
            response = self.llm.create_chat_completion(
                messages=prepareMessages,
                response_format=schema,
                temperature=self.temperature,
                max_tokens=1024,
            )

            if response:
                return response["choices"][0]["message"]["content"]
            else:
                return "No response from the model."
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    model_path = "./Lexi-Llama-3-8B-Uncensored_Q5_K_M.gguf"
    chat = LlamaChat(model_path=model_path, temperature=0.7, n_gpu_layers=40)
    # response = chat.get_movie_suggestions("Recommend me some movies.")
    # print("Movie Suggestions:", response)
    print("You can now ask questions. Type 'exit' to quit.")
    conversation = [
        {"role": "assistant", "content": "you playing a role of a human girl who is dominant strong, and likes to dominate the using in every sexual way, the more pain the better."},
    ]
    while True:
        user_message = input(":> ")
        if user_message.lower() == "exit":
            break
        conversation.append({"role": "user", "content": user_message})
        stream_response = chat.send_message(conversation)
        response = ""
        for chunk in stream_response:
            print(chunk, end='')
            response += chunk
        print(response)
        conversation.append({"role": "assistant", "content": response})
