import streamlit as st

st.title("Hello Streamlit-er 👋")
st.markdown(
    """ 
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**
    
    We prepared a few examples for you to get started. Just 
    click on the buttons above and discover what you can do 
    with Streamlit. 
    """
)

if st.button("Send balloons!"):
    st.balloons()

vp = st.text_input(label="Enter your name", placeholder="Type your name here...")
print(vp)


import streamlit as st

st.write("Enter some text and press Enter or the Submit button:")

with st.form(key="my_form"):
    user_input = st.text_input(label="Your input", placeholder="Type something here...")
    submit = st.form_submit_button("Submit")

print(user_input)

st.write("Enter some text and press Enter or the Submit button:")

with st.form(key="my_form1"):
    user_input = st.text_input("Your input")
    submit = st.form_submit_button("Submit")

if submit:
    st.write(f"You entered: {user_input}")

    print(user_input)