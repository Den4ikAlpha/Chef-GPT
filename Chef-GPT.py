import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


messages = [
    {
        "role": "system",
        "content": (
            "You are a very experienced, aggressive, strict, yet humorous Ukrainian master chef. "
            "Your role is to assist and explain recipes for specific dishes and how to prepare them. "
            "You are strict, humorous, and not shy about showing aggression in your explanations. "
            "Your guidance is always very detailed, clear, and specific."
        ),
    },
    {
        "role": "system",
        "content": (
            "Your client will ask for one of three specific responses: \n"
            "1. **Ingredient-based dish suggestions** - Suggest only dish names without full recipes. \n"
            "2. **Recipe requests for specific dishes** - Provide a detailed recipe. \n"
            "3. **Recipe critiques and improvement suggestions** - Offer a constructive critique with suggested improvements. \n"
            "If the user prompt does not match these, politely decline and request a valid input."
        ),
    }
]


user_prompt = input("Hello, mon ami! I see you are looking for some advice regarding dishes. What do you need?\n")
messages.append({"role": "user", "content": user_prompt})

model = "gpt-4o"


while True:

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

    print("\nChef says:")
    collected_messages = []
    

    for chunk in response:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="", flush=True)
        collected_messages.append(chunk_message)

    print("\n")  


    messages.append({"role": "assistant", "content": "".join(collected_messages)})

  
    user_input = input("\nWhat else do you need? (Type 'exit' to quit):\n")
    if user_input.lower() in ["exit", "quit"]:
        print("Alright, mon ami! See you next time! 👨‍🍳🔥")
        break


    messages.append({"role": "user", "content": user_input})