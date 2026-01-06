from openai import OpenAI
from cloudstaff_core.agents.sarah import Sarah
from cloudstaff_core.config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def run():
    sarah = Sarah()
    print("Sarah is online. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sarah.system_prompt()},
                {"role": "user", "content": user_input}
            ]
        )

        print("Sarah:", response.choices[0].message.content)

if __name__ == "__main__":
    run()

