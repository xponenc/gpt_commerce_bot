from typing import Optional

from openai import OpenAI, PermissionDeniedError


def gpt_chat(user_msg: str, system_prompt: str = None):
    client = OpenAI()
    if not system_prompt:
        system_prompt = "Будь приветлив и краток"
    try:
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_msg}
                      ],
            temperature=0,
        )
        answer = stream.choices[0].message.content
        return answer
    except PermissionDeniedError:
        return None

