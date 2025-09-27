import streamlit as st
import datetime
import re
import random
from typing import Dict

class RuleBasedChatbot:
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict[str, Dict]:
        """Initialize all chatbot rules and responses"""
        return {
            'greetings': {
                'patterns': [
                    r'hi|hello|hey|howdy',
                    r'good morning|good afternoon|good evening',
                    r'what\'?s up|wassup|sup',
                    r'nice to meet you|pleased to meet you'
                ],
                'responses': [
                    "Hello! 👋 How can I help you today?",
                    "Hi there! What can I do for you?",
                    "Hey! Nice to see you. How can I assist?",
                    "Greetings! I'm here to help. What's on your mind?"
                ]
            },
            'farewells': {
                'patterns': [
                    r'bye|goodbye|see you|farewell',
                    r'have a nice day|take care',
                    r'quit|exit|stop'
                ],
                'responses': [
                    "Goodbye! 👋 Hope to see you again soon!",
                    "Take care! Come back anytime!",
                    "Bye! Feel free to chat again whenever you want!",
                    "See you later! Have a great day!"
                ]
            },
            'name': {
                'patterns': [
                    r'what is your name|who are you',
                    r'your name|identify yourself'
                ],
                'responses': [
                    "I'm an AI chatbot! 🤖 You can call me ChatBot.",
                    "I'm your friendly neighborhood chatbot assistant!",
                    "I'm a rule-based chatbot designed to help you with simple queries."
                ]
            },
            'weather': {
                'patterns': [
                    r'weather|temperature|forecast',
                    r'is it hot|cold|raining',
                    r'what\'?s the weather'
                ],
                'responses': [
                    "I don't have real-time weather data, but I can tell you it's always sunny in chatbot land! ☀️",
                    "Weather updates aren't my specialty, but I hope you're having a great day regardless!",
                    "I'm a simple chatbot without weather access. Maybe check your local weather app?"
                ]
            },
            'time': {
                'patterns': [
                    r'what time|current time',
                    r'what is the time|time now',
                    r'tell me the time'
                ],
                'responses': [
                    f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}",
                    f"Right now it's {datetime.datetime.now().strftime('%H:%M')}",
                    f"The time is {datetime.datetime.now().strftime('%I:%M %p on %A, %B %d')}"
                ]
            },
            'math': {
                'patterns': [
                    r'calculate|what is (\d+[\+\-\*\/]\d+)',
                    r'add|subtract|multiply|divide',
                    r'solve (\d+[\+\-\*\/]\d+)'
                ],
                'responses': [
                    "I can help with basic math! Try asking like 'what is 5+3' or 'calculate 10*2'",
                    "I'm ready for some calculations! Give me a simple math problem.",
                    "Math mode activated! 🔢 What would you like me to calculate?"
                ]
            },
            'help': {
                'patterns': [
                    r'help|what can you do',
                    r'commands|options',
                    r'how to use'
                ],
                'responses': [
                    "I can help with: greetings, time, basic math, weather info, and casual conversation!",
                    "Try asking me about: time, simple math, or just say hello!",
                    "I'm here for simple chats, time checks, and basic calculations. What would you like to try?"
                ]
            },
            'default': {
                'patterns': [],
                'responses': [
                    "I'm not sure I understand. Can you try rephrasing that?",
                    "That's interesting! Could you tell me more?",
                    "I'm still learning. Maybe try asking about time, math, or just say hello!",
                    "Hmm, I don't have a specific response for that. Try asking about something else?"
                ]
            }
        }
    
    def process_math_expression(self, message: str) -> str:
        """Extract and calculate simple math expressions"""
        # Look for patterns like "5+3", "10*2", etc.
        math_pattern = r'(\d+)\s*([\+\-\*\/])\s*(\d+)'
        match = re.search(math_pattern, message)
        
        if match:
            num1 = int(match.group(1))
            operator = match.group(2)
            num2 = int(match.group(3))
            
            try:
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "I can't divide by zero! That's mathematically undefined."
                    result = num1 / num2
                else:
                    return "I only handle basic operations: +, -, *, /"
                
                return f"The answer is: {num1} {operator} {num2} = {result}"
            except Exception as e:
                return "I encountered an error with that calculation."
        
        return None
    
    def get_response(self, message: str) -> str:
        """Generate response based on user input and predefined rules"""
        message_lower = message.lower().strip()
        
        # First, check for math expressions
        math_result = self.process_math_expression(message_lower)
        if math_result:
            return math_result
        
        # Check all rule categories
        for category, rule_data in self.rules.items():
            if category == 'default':
                continue
                
            for pattern in rule_data['patterns']:
                if re.search(pattern, message_lower):
                    return random.choice(rule_data['responses'])
        
        # Default response if no patterns match
        return random.choice(self.rules['default']['responses'])

def initialize_session_state():
    """Initialize all session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = 'Light'
    if 'bot' not in st.session_state:
        st.session_state.bot = RuleBasedChatbot()
    if 'message_sent' not in st.session_state:
        st.session_state.message_sent = False

def apply_theme(theme: str):
    """Apply selected theme using CSS"""
    if theme == 'Dark':
        st.markdown("""
            <style>
            .main { background-color: #0E1117; color: #FAFAFA; }
            .stTextInput>div>div>input { background-color: #262730; color: white; }
            .stButton>button { background-color: #262730; color: white; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .main { background-color: #FFFFFF; color: #31333F; }
            .stTextInput>div>div>input { background-color: #F0F2F6; color: #31333F; }
            .stButton>button { background-color: #F0F2F6; color: #31333F; }
            </style>
        """, unsafe_allow_html=True)

def render_chat_bubble(message: str, is_user: bool, timestamp: str):
    """Render a chat bubble with appropriate styling"""
    if is_user:
        # User message bubble (right side, different color)
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            color: white; padding: 12px 16px; border-radius: 18px 18px 0 18px; 
                            max-width: 70%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 5px;">You</div>
                    <div>{message}</div>
                    <div style="font-size: 0.8em; opacity: 0.8; text-align: right; margin-top: 5px;">{timestamp}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Bot message bubble (left side, different color)
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            color: white; padding: 12px 16px; border-radius: 18px 18px 18px 0; 
                            max-width: 70%; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <div style="font-weight: bold; margin-bottom: 5px;">🤖 ChatBot</div>
                    <div>{message}</div>
                    <div style="font-size: 0.8em; opacity: 0.8; margin-top: 5px;">{timestamp}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def render_chat_history():
    """Render the entire chat history with scrollable container"""
    # Create a scrollable container for chat history
    chat_container = st.container()
    
    with chat_container:
        # Display all messages in reverse order (newest at bottom)
        for message_data in st.session_state.chat_history:
            render_chat_bubble(
                message_data['message'], 
                message_data['is_user'],
                message_data['timestamp']
            )
        
        # Add some space at the bottom
        st.markdown("<br>", unsafe_allow_html=True)

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []
    st.session_state.chat_history.append({
        'message': "Chat history cleared! Start a new conversation.",
        'is_user': False,
        'timestamp': datetime.datetime.now().strftime("%H:%M")
    })

def add_message_to_history(message: str, is_user: bool):
    """Add a new message to chat history"""
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append({
        'message': message,
        'is_user': is_user,
        'timestamp': timestamp
    })

def main():
    # Initialize session state
    initialize_session_state()
    
    # Apply selected theme
    apply_theme(st.session_state.theme)
    
    # Main title and description
    st.title("AI Chatbot 🤖")
    st.markdown("### A simple AI chatbot that responds based on predefined rules")
    
    # Sidebar with settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Theme selector
        st.session_state.theme = st.radio(
            "Theme:",
            ['Light', 'Dark'],
            index=0
        )
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            clear_chat_history()
            st.rerun()
        
        # Help section
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.markdown("""
        Try asking me about:
        - **Greetings**: hi, hello, goodbye
        - **Time**: what time is it?
        - **Math**: calculate 5+3, 10*2
        - **Weather**: how's the weather?
        - **Help**: what can you do?
        """)
    
    # Main chat area
    st.markdown("---")
    st.markdown("### 💬 Chat")
    
    # Render chat history
    render_chat_history()
    
    # Use a form for better input handling
    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_input(
                "Type your message...",
                placeholder="Ask me anything!",
                key="user_input",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.form_submit_button("Send", use_container_width=True)
    
    # Process user input when send button is clicked
    if send_button and user_input.strip():
        # Add user message to history
        add_message_to_history(user_input, True)
        
        # Get bot response
        bot_response = st.session_state.bot.get_response(user_input)
        
        # Add bot response to history
        add_message_to_history(bot_response, False)
        
        # Set flag to trigger rerun
        st.session_state.message_sent = True
        st.rerun()
    
    # Add some sample questions as buttons for quick testing
    st.markdown("---")
    st.markdown("### 🚀 Quick Questions")
    
    sample_questions = [
        "Hello! 👋",
        "What time is it?",
        "Calculate 8*7",
        "What's the weather like?",
        "What can you do?",
        "Goodbye! 👋"
    ]
    
    # Create buttons for sample questions
    cols = st.columns(3)
    for i, question in enumerate(sample_questions):
        with cols[i % 3]:
            if st.button(question, use_container_width=True, key=f"sample_{i}"):
                # Add user message to history
                add_message_to_history(question, True)
                
                # Get bot response
                bot_response = st.session_state.bot.get_response(question)
                
                # Add bot response to history
                add_message_to_history(bot_response, False)
                
                # Rerun to update display
                st.rerun()

if __name__ == "__main__":
    main()