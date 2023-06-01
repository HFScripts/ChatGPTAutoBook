import re
import openai

# Read the API key from key.txt
with open('../key.txt', 'r') as file:
    api_key = file.read().strip()

openai.api_key = api_key

valid_options = ["fiction", "non-fiction", "sci-fi", "children's book", "teen fantasy", "educational", "scientific", "romance", "mystery", "biography", "historical fiction", "self-help", "horror", "poetry", "adventure"]

while True:
    chatGPT_author_type = input("Chat GPT is a ________ author\nChoice:\n1. fiction\n2. non-fiction\n3. sci-fi\n4. children's book\n5. teen fantasy\n6. educational\n7. scientific\n8. romance\n9. mystery\n10. biography\n11. historical fiction\n12. self-help\n13. horror\n14. poetry\n15. adventure\n")
    
    if chatGPT_author_type.isdigit() and int(chatGPT_author_type) in range(1, len(valid_options) + 1):
        chatGPT_author_type = valid_options[int(chatGPT_author_type) - 1]
        break
    else:
        print("Invalid choice. Please enter a valid option number.")

user_input = input("Chat GPT is a " + chatGPT_author_type + " author writing a book about: ")

def generate_gpt_response(messages, max_retries=5):
    retry_count = 0
    while retry_count <= max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=3000,
                n=1,
                stop=None,
                temperature=0.5,
            )
            return response.choices[0].message['content'].strip()
        except openai.error.RateLimitError:
            retry_count += 1
            if retry_count <= max_retries:
                print(f"Rate limit error, retrying ({retry_count}/{max_retries})...")
                continue
            else:
                raise
question = [
    {
        "role": "system",
        "content": f"You are an {chatGPT_author_type} author writing a book about {user_input}"
    },
    {
        "role": "user",
        "content": "Write the chapter index and the details to be covered in each chapter. Each Chapter must contain a sub menu.\n\nExample:\n"
                   "Chapter 1. Introduction to Penetration Testing\n"
                   "Definition and purpose of penetration testing\n"
                   "Types of penetration testing\n"
                   "The importance of penetration testing in cybersecurity"
    }
]

response = generate_gpt_response(question)

question = [
    {
        "role": "system",
        "content": f"You are an {chatGPT_author_type} author writing a book about {user_input}"
    },
    {
        "role": "user",
        "content": f"1. Here is your chapter list, it seems it is not as indepth as it should be. "
                   f"2. Make sure the list has ALL (at least 10 where possible) tools not just a few for each chapter. \n{response}"
    }
]

response = generate_gpt_response(question)
pattern = r'Chapter \d+\..*?(?=Chapter \d+\.|\Z)'  # Updated regex pattern
chapters = re.findall(pattern, response, re.MULTILINE | re.DOTALL)  # Find all matches in the response text
with open('Chapters.md', 'w') as file:
    file.write('\n'.join(chapters))

for chapter_number, chapter in enumerate(chapters, start=1):
    chapter_question = [
        {
            "role": "system",
            "content": f"You are an {chatGPT_author_type} author writing a book about {user_input}"
        },
        {
            "role": "user",
            "content": f"The current chapter you are writing: {chapter}"
        }
    ]
    print(f"Chapter and its subchapters: {chapter}")
    chapter_responses = generate_gpt_response(chapter_question)

    # Generate the file name for the current chapter
    chapter_file_name = f"Chapter{chapter_number}.md"

    with open(chapter_file_name, 'w') as file:
        file.write(chapter_responses)

    # Split the response into separate lines
    lines = chapter_responses.split("\n")

    # Regular expression pattern to match lines starting with a number
    pattern = r'^\d+\.'

    # Iterate over each line and process lines starting with a number
    for line in lines:
        if line.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')) and re.match(pattern, line):
            # Extract the number and content after the number
            split_result = re.split(r'\.\s', line, maxsplit=1)
            if len(split_result) == 2:
                number, content = split_result
                explain_info = f"You should give in-depth examples, use multiple examples for each to help with understandingr:\n ```{content}```"
                chapter_explanations = [
                    {
                        "role": "system",
                        "content": f"You are an {chatGPT_author_type} author writing a book about {user_input}."
                    },
                    {
                        "role": "user",
                        "content": f"{explain_info}"
                    }
                ]
                explain_info_response = generate_gpt_response(chapter_explanations)
                print(explain_info_response)

                # Append the explanations to the current chapter file
                with open(chapter_file_name, 'a') as file:
                    file.write(explain_info_response)
            else:
                # Handle the case where the line does not match the expected pattern
                print(f"Invalid line format: {line}")
