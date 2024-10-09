from transformers import GPT3LMHeadModel, GPT3Tokenizer, pipeline

# Load the GPT-3 model and tokenizer
model = GPT3LMHeadModel.from_pretrained("openai-gpt-3")
tokenizer = GPT3Tokenizer.from_pretrained("openai-gpt-3")

# Define a pipeline for text generation
text_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Input questions and keywords
input_text = "I would like to know whether I can get a refund if I overpaid"

# Match the input with the given list of questions
input_list = [
    "What payment methods are accepted?",
    "Can I use multiple payment methods for one order?",
    "Is my payment information secure?",
    "What should I do if my payment is declined?",
    "Can I save my payment information for future purchases?",
    "Are there any additional fees for using certain payment methods?",
    "How can I get a receipt for my purchase?",
    "Can I get a refund if I overpaid?",
    "Do you offer payment plans or financing options?",
    "What currency do you accept?",
]

def find_similar_question(input_text, input_list):
    query = input_text + " ? "
    prompt = query + " " + "Match the question above with the following list of questions:\n" + "\n".join(input_list)
    output = text_pipeline(prompt)
    answer = output[0]['generated_text']
    return answer

similar_question = find_similar_question(input_text, input_list)
print(similar_question)