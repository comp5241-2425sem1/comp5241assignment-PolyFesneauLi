# The app allows the user upload the FAQ Excel spreadsheet
# The app displays the uploaded FAQ as a dataframe.

import streamlit as st
import pandas as pd
import requests, json, os, toml


file_path = 'credentials.txt'
file_path1 = 'credentials3.txt'
if os.path.exists(file_path):
    with open (file_path1 , ' r') as f:
        secrets = toml.load(f)
if os.path.exists(file_path1):
    with open(file_path,'r') as f:
        # read the file the firstline is the API key
        OPENROUTER_API_KEY = f.readline().strip()
# secrets = st.secrets

st.success(f"this is{secrets}")
# OPENROUTER_API_KEY = secrets['OPENROUTER']['Key2']

# OPENROUTER_API_KEY  = 
def SynonymTransform(L,question)-> str:
    # L = ["How do I sign up for membership?",
    #      "What are the membership benefits?",
    #      "How do I cancel my membership?",
    #      "Is my membership auto-renewed?",
    #      "What if I forget my membership ID?",
    #      "What are the delivery options?",
    #      "How do I track my order?",
    #      "Can I change my delivery address?",
    #      "What payment methods are accepted?",
    #      "Can I use multiple payment methods for one order?",
    #      "Is my payment information secure?",
    #      "What should I do if my payment is declined?",
    #      "Can I save my payment information for future purchases?",
    #      "Are there any additional fees for using certain payment methods?",
    #      "How can I get a receipt for my purchase?",
    #      "Can I get a refund if I overpaid?",
    #      "Do you offer payment plans or financing options?",
    #      "What currency do you accept?",
    #      "Can I use a discount code?"]
    print(L)
    msg =[
            {"role": "system", "content": "SynonymTransform"},
            {"role": "user", "content": f"for input{question},match the questions stored in {L} and output the most similiar question,if all canditates are less than 50% similar with input, output 'No similar question found', just output a string, the original question in the list, do not add any other words or space, keep the uppercase and lowercase letters the same."}
        ]
    response = requests.post(
        url = "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
            data=json.dumps({ 
                "messages": msg,
                "model": "openai/gpt-4o-mini-2024-07-18"
                # "model": "openchat/openchat-7b:free"
                # "model": "google/gemma-2-9b-it:free"
                # "model": "meta-llama/llama-3.2-11b-vision-instruct:free"
            })
    )
    if response.status_code == 200:
        try:
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                resp = response_json['choices'][0]['message']['content']
                return resp
            else:
                return "Error: 'choices' key not found or empty in the response."
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return f"Error in response format: {e}"
    else:
        return f"Error: {response.status_code} - {response.text}"

st.title('FAQ App')
# input_str = " I'd like to know whether i can get a refund if overpay "
# question = st.text_input("Inter a question:")
# st.success(SynonymTransform(question))

# upload FAQ xlsx
uploaded_file = st.file_uploader("Choose a file",type=['xlsx'])

if uploaded_file is not None:
    # fetch FAQ xlsx from path
    df = pd.read_excel(uploaded_file, converters={'Question': str, 'Category': str, 'Answer': str})
    st.info("Uploaded FAQ DataFrame:")
    # keep original strings in blocks
    st.write(df)

    # fetch a question from input
    question = st.text_input("Inter a question:")

    with st.expander("Prompt", expanded=True):
        # st.write("Choose a category:")
        ## add a dropdown to choose a category
        # multiple categories
        categories = st.multiselect("Choose categories:", df['Category'].unique())
        #category = st.selectbox("Choose a category:", df['Category'].unique())
        # st.success(f"Category: {category}")

    # fetch the answer from the FAQ xlsx
    if st.button("Get Answer"):
        st.markdown("## **Response:**")
        if question == "Who is the author of this app?":
            answer = ["Tianye Li 24063117g"]
        else:
            q = SynonymTransform(df['Question'].values,question)
            st.success(q)
            answer = df[(df['Question'] == q) & (df['Category'].isin(categories))]['Answer'].values
        if len(answer) >= 1:
            if len(answer)>1:
                st.warning("Multiple answers found.")
                st.success(f"Answer: ")
                st.markdown(f"```text\n{answer[0]}\n```")
                for ans in answer[1:]:
                    st.markdown(f"```text\n{ans}\n```")
            elif len(answer)==1:
                st.success(f"Answer:")
                st.code(answer,language='text')
            st.success(f"Categories: ")
            for cate in categories:
                if(df[(df['Question'] == q) & (df['Category']==cate)]['Answer'].values == answer):
                    st.markdown(f"```text\n{cate}\n```")
            st.success(f"Reference: ")
            Reference = df[(df['Question'] == q) & (df['Category'].isin(categories))].values
            st.markdown(f"```text\n{Reference}\n```")
        else:
            st.warning("Sorry, no answer found.Contact the customer representative for more information.")
            st.warning(f"Categories: ")
            st.markdown(f"N/A")
            
        
        
    

# Before providing the AI response, 
# you should first show an “expander” where when expanded, it will show the prompt that you have used.

# iterate through the rows of the xlsx file 
# and get every question

