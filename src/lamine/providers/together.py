from together import Together as Together_source

from ..datatypes import Answer, Message, Model
from . import Provider


class Together(Provider):
    model_ids = ["deepseek-ai/DeepSeek-V3", "meta-llama/Llama-3-8b-chat-hf"]
    env_vars = ["TOGETHER_API_KEY"]

    def get_answer(self, model: Model, conversation: list[Message], **kwargs) -> Answer:
        client = Together_source()
        messages = [message.to_dict for message in conversation]
        response = client.chat.completions.create(model=model.id, messages=messages, **kwargs)
        return Answer(
            content=response.choices[0].message.content,
            tokens_in=response.usage.prompt_tokens,
            tokens_out=response.usage.completion_tokens,
            source=response,
        )
