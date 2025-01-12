from typing import Optional
from openai import OpenAI, PermissionDeniedError, AsyncOpenAI
from services.loggers import logger
from services.memory import user_buffer_memory
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI


async def answer_gpt_memory(user_id: int,
                            system: str,
                            add: str,
                            user_query: str,
                            model: str,
                            temp: float):
    if user_id not in user_buffer_memory:
        user_buffer_memory[user_id] = ConversationSummaryBufferMemory(
            llm=ChatOpenAI(model=model),
            max_token_limit=3000)

    # Получение истории
    history = await user_buffer_memory[user_id].aload_memory_variables({})
    if isinstance(history['history'], str):  # если строка
        sum_history = history['history']
    else:  # если список
        sum_history = "\n".join(
            message.content for message in history['history'])
    logger.info(f'\nSum_history:\n{sum_history}\n')

    # Запрос с историей и получение ответа от OpenAi
    answer = await answer_gpt(system, add, user_query, sum_history, model, temp)
    # Сохранение сообщений в историю
    await user_buffer_memory[user_id].asave_context({"input": user_query}, {"output": answer})
    logger.info(answer)
    return answer


async def answer_gpt(system: str,
                     add: str,
                     user_query: str,
                     history: str,
                     model: str = "gpt-4o-mini",
                     temp: float = 0) -> str:
    messages = [{"role": "system", "content": system},
                {"role": "user",
                 "content": f'Вот история диалога: \n{history}\n\n{add} \
                 \nВот сообщение пользователя / студента: {user_query}'}]
    completion = await AsyncOpenAI().chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp)
    await tokens_count_and_price(completion, model)
    return completion.choices[0].message.content


# Функция подсчета количества используемых токенов и стоимости
# https://openai.com/pricing
async def tokens_count_and_price(completion, model):
    if model == "gpt-4o-mini":
        input_price, output_price = 0.15, 0.60  # Устанавливаем цены
        price = (input_price * completion.usage.prompt_tokens / 1e6 +
                 output_price * completion.usage.completion_tokens / 1e6)  # Рассчитываем стоимость
        values = {'price': price,
                  'input': completion.usage.prompt_tokens,
                  'output': completion.usage.completion_tokens,
                  'total': completion.usage.total_tokens}
        logger.info(f"Tokens used: {values['input']} + {values['output']} = {values['total']}. "
                    f"*** {model} *** $ {round(values['price'], 8)}\n")
        return values


def gpt_chat(user_msg: str, system_prompt: str = None, model_temperature: float = 0):
    client = OpenAI()
    if not system_prompt:
        system_prompt = "Будь приветлив и краток"
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_msg}
                      ],
            temperature=model_temperature,
        )
        answer = stream.choices[0].message.content
        return answer
    except PermissionDeniedError:
        return None
