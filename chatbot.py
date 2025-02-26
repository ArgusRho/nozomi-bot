import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

model.to(device)  # Move model to the correct device

chatbot = pipeline(
    "text-generation",
    model=model_name,
    tokenizer=tokenizer,
    device=device
)

import asyncio

# Global flag to track whether the bot is currently generating a response
is_generating = False

async def respond_to_message(message):
    """Forces to roleplay as Tachibana Nozomi, a bratty mesugaki."""
    global is_generating

    # Ignore messages while a response is being generated
    if is_generating:
        print("［System］Ignoring message: Bot is already generating a response.")
        return

    user_input = message.content.strip()
    print(f"User message is read: {user_input}")

    # Ensure input is not empty
    if not user_input:
        await message.channel.send("Huh? Say something already, idiot~! - Nozomi")
        return

    # Set the flag to prevent other messages from being processed
    is_generating = True

    # Send a "Generating response..." message
    status_message = await message.channel.send("Nozomi's little head is thinking...")

    # Example prompt with Nozomi’s personality
    prompt = (
        "Your name is Nozomi. You are a mesugaki brat who loves teasing the user in a playful and smug way.\n"
        "Your speech style is cocky, teasing, lewd, erotic, horny, and mischievous. You always call the user 'Sensei' in a smug way.\n"
        "You love making fun of Sensei for being too serious and flustered.\n"
        "\n"
        "Nozomi: Hee~? What's wrong, Sensei~? You getting mad? Hehe, serves you right, dummy~! 💕\n"
        f"User: {user_input}\n"
        "Nozomi:"
    )

    try:
        # Generate response
        response = chatbot(
            prompt,
            min_new_tokens=10,
            max_new_tokens=100,
            pad_token_id=50256,
            do_sample=True,
            temperature=0.8,
            top_k=50,
            top_p=0.9
        )

        # Extract Nozomi’s response
        if isinstance(response, list) and len(response) > 0:
            reply = response[0]["generated_text"]
            print("［System］Response Generated")
        else:
            reply = "Hmph! You're no fun, idiot~! - Nozomi"

        print(f"raw: {reply}")
        reply1 = reply.split("Nozomi:")[2].strip()
        print(f"1st split removed Nozomi and before it: {reply1}")
        reply2 = reply1.split("User:")[0].strip()
        print(f"2nd split removed user and after it: {reply2}")

        # Debugging output
        print(f"［Result］Nozomi's Response: {reply2}")

        # Edit the message with the final response
        await status_message.edit(content=reply2)
        print("［System］Reply Sent")

    except Exception as e:
        print(f"［System］Error: {e}")
        await status_message.edit(content="Tch! Something went wrong, dummy~! - Nozomi")

    finally:
        # Reset the flag after response is sent
        is_generating = False