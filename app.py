import streamlit as st, os, time
from google import generativeai as genai
from google.generativeai import types
from pypdf import PdfReader, PdfWriter, PdfMerger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def setup_page():
    st.set_page_config(
        page_title="AI-Powered Chatbot",
        layout="centered"
    )

    st.header("AI-Powered Chatbot", anchor=False, divider="blue")

    st.sidebar.header("Options", divider='rainbow')

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def get_choice():
    choice = st.sidebar.radio("Choose:", ["Chat with AI",
                                          "Chat with a PDF",
                                          "Chat with many PDFs",
                                          "Chat with an image",
                                          "Chat with audio",
                                          "Chat with video"], )
    return choice


def get_clear():
    clear_button = st.sidebar.button("Start new session", key="clear")
    return clear_button


def main():
    choice = get_choice()

    if choice == "Chat with AI":
        st.subheader("Chat with AI")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        if 'chat' not in st.session_state or clear: # Create a new chat object at the begining of session or after "Start New Session" button is clicked
            st.session_state.chat = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])
            st.session_state.system_instruction = "You are a helpful assistant. Your answers need to be positive and accurate."

        prompt = st.chat_input("Enter your question here")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)

            # Add user message to the chat history
            st.session_state.chat.history.append(types.Content(role="user", parts=[prompt]))

            with st.chat_message(
                    "model", avatar="🟦",
            ):
                response = st.session_state.chat.send_message(prompt) # Now using the chat object from session state
                st.markdown(response.text)
                #st.sidebar.markdown(str(response.usage_metadata)) # Usage metadata might not be available directly
                st.session_state.chat.history.append(types.Content(role="model", parts=[response.text]))


    elif choice == "Chat with a PDF":
        st.subheader("Chat with your PDF file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        uploaded_files = st.file_uploader("Choose your pdf file", type=['pdf'], accept_multiple_files=False)
        if uploaded_files:
            try:
                with st.spinner("Extracting text from PDF..."):
                    pdf_reader = PdfReader(uploaded_files)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()

                if 'chat2' not in st.session_state or clear: # Check if chat object exists or if "clear" is pressed
                    st.session_state.chat2 = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])
                    system_instruction = "You are a helpful assistant. Use the context provided to answer the questions."
                    st.session_state.chat2.history.append(types.Content(role="user", parts=[system_instruction + "\nContext: " + text]))

                prompt2 = st.chat_input("Enter your question here")
                if prompt2:
                    with st.chat_message("user"):
                        st.write(prompt2)

                    with st.chat_message(
                        "model", avatar="🟦",
                    ):
                        response2 = st.session_state.chat2.send_message(prompt2)
                        st.markdown(response2.text)
                        #st.sidebar.markdown(str(response2.usage_metadata))
                        st.session_state.chat2.history.append(types.Content(role="user", parts=[prompt2]))
                        st.session_state.chat2.history.append(types.Content(role="model", parts=[response2.text]))

            except Exception as e:
                st.error(f"An error occurred processing the PDF: {e}")


    elif choice == "Chat with many PDFs":
        st.subheader("Chat with your PDF file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        uploaded_files2 = st.file_uploader("Choose 1 or more files", type=['pdf'], accept_multiple_files=True)

        if uploaded_files2:
            try:
                with st.spinner("Merging and extracting text from PDFs..."):
                    text = ""
                    for file in uploaded_files2:
                        pdf_reader = PdfReader(file)
                        for page in pdf_reader.pages:
                            text += page.extract_text()


                if 'chat2b' not in st.session_state or clear:
                    st.session_state.chat2b = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])
                    system_instruction = "You are a helpful assistant. Use the context provided to answer the questions."
                    st.session_state.chat2b.history.append(types.Content(role="user", parts=[system_instruction + "\nContext: " + text]))


                prompt2b = st.chat_input("Enter your question here")
                if prompt2b:
                    with st.chat_message("user"):
                        st.write(prompt2b)

                    with st.chat_message(
                        "model", avatar="🟦",
                    ):
                        response2b = st.session_state.chat2b.send_message(prompt2b)
                        st.markdown(response2b.text)
                        #st.sidebar.markdown(str(response2b.usage_metadata))
                        st.session_state.chat2b.history.append(types.Content(role="user", parts=[prompt2b]))
                        st.session_state.chat2b.history.append(types.Content(role="model", parts=[response2b.text]))

            except Exception as e:
                st.error(f"An error occurred: {e}")


    elif choice == "Chat with an image":
        st.subheader("Chat with an Image")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        uploaded_files2 = st.file_uploader("Choose your PNG or JPEG file", type=['png', 'jpg', 'jpeg'],
                                            accept_multiple_files=False)
        if uploaded_files2:
            try:
                image_data = uploaded_files2.read()  # Read the image data
                image_part = {"mime_type": uploaded_files2.type, "data": image_data} # uploaded_files2.type will give you mime type

                if 'chat3' not in st.session_state or clear:
                    st.session_state.chat3 = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])

                prompt3 = st.chat_input("Enter your question here")
                if prompt3:
                    with st.chat_message("user"):
                        st.write(prompt3)

                    parts = [prompt3, image_part] # Combining prompt with image
                    response3 = st.session_state.chat3.send_message(parts)

                    with st.chat_message(
                        "model", avatar="🟦",
                    ):
                        st.markdown(response3.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")



    elif choice == "Chat with audio":
        st.subheader("Chat with your audio file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        uploaded_files3 = st.file_uploader("Choose your mp3 or wav file", type=['mp3', 'wav'],
                                            accept_multiple_files=False)
        if uploaded_files3:
            try:
                audio_data = uploaded_files3.read() # Read audio file

                if 'chat4' not in st.session_state or clear:
                    st.session_state.chat4 = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])


                prompt5 = st.chat_input("Enter your question here")
                if prompt5:
                    with st.chat_message("user"):
                        st.write(prompt5)

                    parts = [prompt5, {"mime_type": uploaded_files3.type, "data": audio_data}]
                    response4 = st.session_state.chat4.send_message(parts)

                    with st.chat_message(
                        "model", avatar="🟦",
                    ):
                        st.markdown(response4.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")



    elif choice == "Chat with video":
        st.subheader("Chat with your video file")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']

        if 'message' not in st.session_state:
            st.session_state.message = " "

        uploaded_files4 = st.file_uploader("Choose your mp4 or mov file", type=['mp4', 'mov'],
                                            accept_multiple_files=False)

        if uploaded_files4:
            try:
                video_data = uploaded_files4.read()

                if 'chat5' not in st.session_state or clear:
                    st.session_state.chat5 = genai.GenerativeModel(model_name=MODEL_ID).start_chat(history=[])


                prompt4 = st.chat_input("Enter your question here")
                if prompt4:
                    with st.chat_message("user"):
                        st.write(prompt4)

                    parts = [prompt4, {"mime_type": uploaded_files4.type, "data": video_data}]
                    response5 = st.session_state.chat5.send_message(parts)

                    with st.chat_message(
                        "model", avatar="🟦",
                    ):
                        st.markdown(response5.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")


if __name__ == '__main__':
    setup_page()
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        st.error("Please set the GOOGLE_API_KEY environment variable.")
    else:
        genai.configure(api_key=GOOGLE_API_KEY) # Use genai.configure
        MODEL_ID = "gemini-1.5-flash" # Or gemini-1.5-pro
        main()
