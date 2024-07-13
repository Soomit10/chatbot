import json
from difflib import get_close_matches

right_arrow = '\u2192'
file_path = '/home/soomit/Downloads/chatbot/knowledge_base.json'

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q.get("answer", None)  # Use get to avoid KeyError
    return None

def greeting():
    greetings = [
        "Hello! I'm your friendly chatbot. How can I assist you today?",
        "Hi there! How can I help you?",
        "Greetings! What would you like to know today?"
    ]
    print(f'Bot: {random.choice(greetings)}')

def farewell():
    farewells = [
        "Goodbye! Have a great day!",
        "Bye! Feel free to come back if you have more questions.",
        "Take care! See you next time!"
    ]
    print(f'Bot: {random.choice(farewells)}')

def help_message():
    help_text = (
        "You can ask me any question and I'll try to answer it based on what I've learned.\n"
        "If I don't know the answer, you can teach me by typing the answer after my prompt.\n"
        "Type 'quit' to exit the chat, or 'help' to see this message again."
    )
    print(f'Bot: {help_text}')


def chat_bot():
    knowledge_base: dict = load_knowledge_base(file_path)

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        questions_list = [q.get("question", "") for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions_list)

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            if answer:
                print(f'Bot: {answer}')
            else:
                print("Bot: I don't know the answer. Can you teach me:")
                new_answer: str = input('Type the answer or "skip" to skip: ')
                if new_answer.lower() != 'skip':
                    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                    save_knowledge_base(file_path, knowledge_base)
                    print('Bot: Thank you! I learned a new response!')
        else:
            print("Bot: I don't know the answer. Can you teach me:")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(file_path, knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()

