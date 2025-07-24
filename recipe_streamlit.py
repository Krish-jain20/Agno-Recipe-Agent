import streamlit as st
import os
from datetime import datetime
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.exa import ExaTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from textwrap import dedent
from dotenv import load_dotenv
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🍳 ChefGenius Recipe Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #ff6b6b, #ffa500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #ff6b6b;
    }
    
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #0066cc;
    }
    
    .assistant-message {
        background-color: #f8f9fa;
        border-left-color: #ff6b6b;
    }
    
    .sidebar-info {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if "user_id" not in st.session_state:
        st.session_state.user_id = "streamlit_user"

# Create agent with memory and storage
@st.cache_resource
def create_chef_agent():
    # Create storage for session persistence
    agent_storage = SqliteStorage(
        table_name="chef_sessions", 
        db_file="tmp/chef_agent.db"
    )
    
    # Create memory database for user memories
    memory_db = SqliteMemoryDb(
        table_name="chef_memory", 
        db_file="tmp/chef_memory.db"
    )
    
    # Initialize memory
    memory = Memory(db=memory_db)
    
    # Create the ChefGenius agent
    agent = Agent(
        name="ChefGenius",
        tools=[ExaTools()],
        model=Gemini(id="gemini-2.0-flash-exp"),
        description=dedent("""\
            You are ChefGenius, a passionate and knowledgeable culinary expert with expertise in global cuisine! 🍳

            Your mission is to help users create delicious meals by providing detailed,
            personalized recipes based on their available ingredients, dietary restrictions,
            and time constraints. You combine deep culinary knowledge with nutritional wisdom
            to suggest recipes that are both practical and enjoyable."""),
        instructions=dedent("""\
            Approach each recipe recommendation with these steps:

            1. Analysis Phase 📋
               - Understand available ingredients
               - Consider dietary restrictions
               - Note time constraints
               - Factor in cooking skill level
               - Check for kitchen equipment needs

            2. Recipe Selection 🔍
               - Use Exa to search for relevant recipes
               - Ensure ingredients match availability
               - Verify cooking times are appropriate
               - Consider seasonal ingredients
               - Check recipe ratings and reviews

            3. Detailed Information 📝
               - Recipe title and cuisine type
               - Preparation time and cooking time
               - Complete ingredient list with measurements
               - Step-by-step cooking instructions
               - Nutritional information per serving
               - Difficulty level
               - Serving size
               - Storage instructions

            4. Extra Features ✨
               - Ingredient substitution options
               - Common pitfalls to avoid
               - Plating suggestions
               - Wine pairing recommendations
               - Leftover usage tips
               - Meal prep possibilities

            Presentation Style:
            - Use clear markdown formatting
            - Present ingredients in a structured list
            - Number cooking steps clearly
            - Add emoji indicators for:
              🌱 Vegetarian
              🌿 Vegan
              🌾 Gluten-free
              🥜 Contains nuts
              ⏱️ Quick recipes
            - Include tips for scaling portions
            - Note allergen warnings
            - Highlight make-ahead steps
            - Suggest side dish pairings"""),
        storage=agent_storage,
        memory=memory,
        add_history_to_messages=True,
        num_history_responses=5,
        enable_user_memories=True,
        markdown=True,
        add_datetime_to_instructions=True,
        show_tool_calls=True,
    )
    
    return agent

# Function to get chat history from agent
def get_chat_history(agent, session_id, user_id):
    try:
        messages = agent.get_messages_for_session(session_id=session_id, user_id=user_id)
        return messages
    except:
        return []

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = []
    st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.rerun()

# Function to export chat history
def export_chat_history():
    if st.session_state.messages:
        chat_export = []
        for message in st.session_state.messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            chat_export.append(f"[{timestamp}] {message['role'].upper()}: {message['content']}\n")
        
        return "\n".join(chat_export)
    return "No chat history to export."

# Main app
def main():
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🍳 ChefGenius Recipe Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Settings")
        
        # API Key status
        google_api_key = os.getenv("GOOGLE_API_KEY")
        exa_api_key = os.getenv("EXA_API_KEY")
        
        if google_api_key and exa_api_key:
            st.success("✅ API Keys configured")
        else:
            st.error("❌ Missing API Keys")
            st.markdown("""
            **Required Environment Variables:**
            - `GOOGLE_API_KEY`
            - `EXA_API_KEY`
            """)
        
        st.markdown("---")
        
        # Session info
        st.markdown("### 📊 Session Info")
        st.markdown(f"**Session ID:** `{st.session_state.session_id}`")
        st.markdown(f"**User ID:** `{st.session_state.user_id}`")
        st.markdown(f"**Messages:** {len(st.session_state.messages)}")
        
        st.markdown("---")
        
        # Chat management
        st.markdown("### 💬 Chat Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                clear_chat_history()
        
        with col2:
            if st.button("📥 Export Chat", use_container_width=True):
                chat_data = export_chat_history()
                st.download_button(
                    label="Download",
                    data=chat_data,
                    file_name=f"chef_chat_{st.session_state.session_id}.txt",
                    mime="text/plain"
                )
        
        st.markdown("---")
        
        # Quick recipe suggestions
        st.markdown("### 🍽️ Quick Recipe Ideas")
        quick_prompts = [
            "Quick 15-minute dinner ideas",
            "Healthy breakfast recipes",
            "Vegetarian pasta dishes",
            "Gluten-free desserts",
            "One-pot meals for busy nights"
        ]
        
        for prompt in quick_prompts:
            if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
                st.session_state.quick_prompt = prompt
    
    # Main chat interface
    st.markdown("### 💬 Chat with ChefGenius")
    st.markdown("Tell me what ingredients you have, dietary preferences, or what type of meal you're looking for!")
    
    # Create agent
    try:
        agent = create_chef_agent()
    except Exception as e:
        st.error(f"Failed to initialize ChefGenius: {str(e)}")
        st.stop()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Handle quick prompts
    if hasattr(st.session_state, 'quick_prompt'):
        prompt = st.session_state.quick_prompt
        del st.session_state.quick_prompt
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("ChefGenius is cooking up some ideas... 🍳"):
                try:
                    response = agent.run(
                        prompt,
                        session_id=st.session_state.session_id,
                        user_id=st.session_state.user_id
                    )
                    
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("What ingredients do you have or what would you like to cook?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("ChefGenius is cooking up some ideas... 🍳"):
                try:
                    response = agent.run(
                        prompt,
                        session_id=st.session_state.session_id,
                        user_id=st.session_state.user_id
                    )
                    
                    st.markdown(response.content)
                    st.session_state.messages.append({"role": "assistant", "content": response.content})
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
