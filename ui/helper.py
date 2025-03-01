custom_css = """
    <style>
        body {
            background-color: #f0f2f6;
            color: #333;
        }
        .stTextInput > div > div > input {
            background-color: #fff;
            color: #333;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .chat-message.assistant {
            background-color: #e1f5fe;
            text-align: left;
        }
        .chat-message.user {
            background-color: #c8e6c9;
            text-align: right;
        }
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }
        .link-preview {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
    """

def display_duration(duration):
    return f"""
    <div style='text-align: right; color: grey;'>
        Request completed in {duration} seconds
    </div>
    """
