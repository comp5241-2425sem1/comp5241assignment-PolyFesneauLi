# The app allows the user upload the FAQ Excel spreadsheet
# The app displays the uploaded FAQ as a dataframe.

import streamlit as st
import pandas as pd

st.title('FAQ App')
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
            answer = df[(df['Question'] == question) & (df['Category'].isin(categories))]['Answer'].values
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
            for cate in categories[1:]:
                st.markdown(f"```text\n{cate}\n```")
            st.success(f"Reference: ")
            Reference = df[(df['Question'] == question) & (df['Category'].isin(categories))].values
            st.markdown(f"```text\n{Reference}\n```")
        else:
            st.warning("Sorry, no answer found.Contact the customer representative for more information.")
            st.warning(f"Categories: ")
            st.markdown(f"N/A")
            
        
        
    

# Before providing the AI response, 
# you should first show an “expander” where when expanded, it will show the prompt that you have used.

# iterate through the rows of the xlsx file 
# and get every question

