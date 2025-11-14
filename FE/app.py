import streamlit as st
import requests
import json
import time
import os
import shutil

# Page config
st.set_page_config(
    page_title="Codebase Genius - AI Documentation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Beautiful Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background - soft dark */
    .main {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Sidebar background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2f 0%, #252538 100%);
    }
    
    /* All text color adjustments */
    .main, .sidebar .sidebar-content, p, span, div {
        color: #e0e0e0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: slideDown 0.8s ease-out;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #b0b0c0 !important;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        border-radius: 12px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.7);
    }
    
    /* Form submit button */
    .stForm button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
        padding: 0.6rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .success-box {
        padding: 2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #1a4d2e 0%, #2d5f3f 100%);
        border: 2px solid #4ecca3;
        margin: 2rem 0;
        animation: slideUp 0.5s ease-out;
        box-shadow: 0 8px 25px rgba(78, 204, 163, 0.3);
    }
    
    .success-box * {
        color: #e8f5e9 !important;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .info-box {
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e3a5f 0%, #2c4f7c 100%);
        border-left: 5px solid #4fc3f7;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(79, 195, 247, 0.2);
    }
    
    .info-box * {
        color: #e1f5fe !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2a2a3e 0%, #3a3a52 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Input fields styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #3a3a52;
        padding: 12px;
        font-size: 1rem;
        background-color: #2a2a3e !important;
        color: #e0e0e0 !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        background-color: #323248 !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #888899 !important;
    }
    
    /* Download button - Green theme */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        border-radius: 12px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.6);
    }
    
    /* Documentation preview box */
    .doc-preview {
        background: linear-gradient(135deg, #2a2a3e 0%, #323248 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #3a3a52;
        max-height: 700px;
        overflow-y: auto;
        margin-top: 1rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .doc-preview * {
        color: #e0e0e0 !important;
    }
    
    .doc-preview h1, .doc-preview h2, .doc-preview h3 {
        color: #ffffff !important;
        margin-top: 1.5rem;
    }
    
    .doc-preview code {
        background-color: #1a1a2e;
        padding: 2px 6px;
        border-radius: 4px;
        color: #f093fb !important;
    }
    
    .doc-preview pre {
        background-color: #1a1a2e;
        padding: 1rem;
        border-radius: 8px;
        overflow-x: auto;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #667eea !important;
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0c0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #2a2a3e;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #3a3a52;
        color: #e0e0e0 !important;
        border-radius: 8px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2a2a3e 0%, #3a3a52 100%) !important;
        border-radius: 10px;
        font-weight: 600;
        color: #e0e0e0 !important;
        border: 1px solid #3a3a52;
    }
    
    /* Divider */
    hr {
        border-color: #3a3a52 !important;
        margin: 2rem 0;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.5);
    }
    
    .hero-section * {
        color: white !important;
    }
    
    .feature-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-weight: 600;
        margin: 0.3rem;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'documentation_path' not in st.session_state:
    st.session_state.documentation_path = None
if 'doc_content' not in st.session_state:
    st.session_state.doc_content = None
if 'last_repo_url' not in st.session_state:
    st.session_state.last_repo_url = None

# Header
st.markdown('<h1 class="main-header">🧠 Codebase Genius</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform Any GitHub Repository into Beautiful Documentation with AI</p>', unsafe_allow_html=True)

# Hero Section (only when not logged in)
if st.session_state.token is None:
    st.markdown("""
    <div class="hero-section">
        <h2 style="margin-top: 0;">✨ Welcome to the Future of Code Documentation</h2>
        <p style="font-size: 1.2rem; margin: 1.5rem 0;">
            Automatically generate comprehensive, professional documentation for any GitHub repository in seconds.
        </p>
        <div style="margin-top: 2rem;">
            <span class="feature-badge">🗺️ Smart Mapping</span>
            <span class="feature-badge">🔍 Code Analysis</span>
            <span class="feature-badge">📝 Auto Documentation</span>
            <span class="feature-badge">⚡ Powered by Groq</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 🔑 User Session")
    
    if st.session_state.token is None:
        st.markdown("##### Login or Create Account")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("Username", placeholder="Enter username", key="login_user")
                password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
                
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True)
                
                if login_btn and username and password:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/user/login",
                            json={"username": username, "password": password},
                            timeout=10
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data['token']
                            st.session_state.username = data['username']
                            st.success("✅ Welcome back!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend server not responding. Is it running?")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        with tab2:
            with st.form("register_form", clear_on_submit=True):
                new_username = st.text_input("Username", placeholder="Choose username", key="reg_user")
                new_password = st.text_input("Password", type="password", placeholder="Create password", key="reg_pass")
                
                register_btn = st.form_submit_button("🎉 Create Account", use_container_width=True)
                
                if register_btn and new_username and new_password:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/user/create",
                            json={"username": new_username, "password": new_password},
                            timeout=10
                        )
                        if response.status_code == 201:
                            data = response.json()
                            st.session_state.token = data['token']
                            st.session_state.username = data['username']
                            st.success("✅ Account created!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Username already exists")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend server not responding. Is it running?")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    else:
        st.markdown(f"""
        <div style="padding: 1rem; background: linear-gradient(135deg, #1a4d2e 0%, #2d5f3f 100%); 
                    border-radius: 10px; margin-bottom: 1rem; border: 1px solid #4ecca3;">
            <p style="margin: 0; font-weight: 600; color: #e8f5e9 !important;">👤 {st.session_state.username}</p>
            <p style="margin: 0; font-size: 0.9rem; color: #b8e6d5 !important;">Active Session</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.username = None
            st.session_state.documentation_path = None
            st.session_state.doc_content = None
            st.session_state.last_repo_url = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    <div class="info-box">
        <p style="color: #e1f5fe !important;"><strong>Codebase Genius</strong> uses advanced AI to analyze codebases and generate professional documentation.</p>
        <br>
        <p style="color: #e1f5fe !important;"><strong>Powered by:</strong></p>
        <ul style="color: #e1f5fe !important;">
            <li>🤖 Groq / Gemini AI</li>
            <li>⚡ Jac Language</li>
            <li>🎨 Streamlit</li>
            <li>🐍 Python AST</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content
if st.session_state.token is None:
    st.warning("⚠️ Please login or register from the sidebar to start generating documentation.")
else:
    st.markdown("## 🚀 Generate Documentation")
    
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        help="Enter the full URL of any public GitHub repository",
        key="repo_url_input"
    )
    
    # Warning if reusing same URL
    if repo_url and repo_url == st.session_state.last_repo_url:
        st.warning("⚠️ You already generated docs for this repo. Clear the preview below or use a different URL.")
    
    generate_btn = st.button("🎯 Generate Documentation", use_container_width=True)
    
    with st.expander("📌 Try Popular Repositories"):
        example_col1, example_col2 = st.columns(2)
        with example_col1:
            st.markdown("""
            **Python Libraries:**
            - `https://github.com/pallets/click`
            - `https://github.com/pallets/flask`
            - `https://github.com/psf/requests`
            """)
        with example_col2:
            st.markdown("""
            **More Examples:**
            - `https://github.com/fastapi/fastapi`
            - `https://github.com/jaseci-labs/jaclang`
            """)
    
    if generate_btn:
        if not repo_url:
            st.error("❌ Please enter a repository URL")
        elif "github.com" not in repo_url:
            st.error("❌ Please enter a valid GitHub URL")
        else:
            # Clear old temp directory if reusing same repo
            # This is a good practice for this local setup
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            temp_dir = f"/tmp/codebase_genius/{repo_name}"
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    st.toast("🧹 Cleared old repository cache...")
                except Exception as e:
                    st.warning(f"Could not clear cache: {e}")
            
            progress_bar = st.progress(0, text="Starting...")
            status_text = st.empty()
            
            try:
                status_text.markdown("### ⏳ Calling Codebase Genius...")
                progress_bar.progress(10, text="Step 1/3: Mapping Repository... (This may take a moment)")
                
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                
                # This is a single, synchronous call. The walker runs all 3 steps on the backend.
                response = requests.post(
                    f"{API_BASE_URL}/walker/code_genius",
                    headers=headers,
                    json={"fields": {"repo_url": repo_url, "session_id": ""}},
                    timeout=300  # 5 minute timeout for large repos
                )
                
                # This code runs AFTER the entire backend process is complete
                progress_bar.progress(70, text="Step 2/3: Analyzing Code...")
                time.sleep(0.5) # Cosmetic delay
                progress_bar.progress(90, text="Step 3/3: Generating Documentation...")
                time.sleep(0.5) # Cosmetic delay
                
                if response.status_code == 200:
                    progress_bar.progress(100, text="✅ Done!")
                    status_text.markdown("### ✅ Documentation Generated!")
                    
                    data = response.json()
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("## 🎉 Success!")
                    st.markdown("Your documentation is ready!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Parse the final report from the walker
                    if 'reports' in data and len(data['reports']) > 0:
                        final_report_found = False
                        doc_report_found = False
                        
                        # Iterate backwards to get the *final* reports
                        for report in reversed(data['reports']):
                            
                            # Find the final walker report for metrics
                            if not final_report_found and 'total_files' in report:
                                st.markdown("### 📊 Analysis Results")
                                col1, col2, col3 = st.columns(3)
                                col1.metric("Files Analyzed", report.get('total_files', 0))
                                col2.metric("Functions Found", report.get('total_functions', 0))
                                col3.metric("Classes Found", report.get('total_classes', 0))
                                final_report_found = True

                            # Find the DocGenie report for the output path
                            if not doc_report_found and 'output_path' in report:
                                output_path = report.get('output_path')
                                if output_path:
                                    st.session_state.documentation_path = output_path
                                    st.session_state.last_repo_url = repo_url
                                    
                                    # This is the key: Read the file the backend created
                                    if os.path.exists(output_path):
                                        with open(output_path, 'r') as f:
                                            st.session_state.doc_content = f.read()
                                        
                                        file_size = os.path.getsize(output_path)
                                        st.info(f"📍 **Saved to:** `{output_path}`  \n📏 **Size:** {file_size:,} bytes")
                                    else:
                                        st.error(f"Backend reported path, but file not found: {output_path}")
                                doc_report_found = True

                            if final_report_found and doc_report_found:
                                break
                    
                    with st.expander("🔍 View Full API Response"):
                        st.json(data)
                else:
                    st.error(f"❌ Error {response.status_code}")
                    if response.status_code == 401:
                        st.warning("Session expired. Please logout and login again.")
                    try:
                        st.json(response.json())
                    except:
                        st.text(response.text)
                    
            except requests.exceptions.Timeout:
                progress_bar.progress(0, text="Error")
                st.error("❌ Request timed out. Repository might be too large. Try a smaller repo.")
            except requests.exceptions.ConnectionError:
                progress_bar.progress(0, text="Error")
                st.error("❌ Cannot connect to backend. Please restart the backend server.")
            except Exception as e:
                progress_bar.progress(0, text="Error")
                st.error(f"❌ An unknown error occurred: {str(e)}")
    
    # Documentation viewer - Always visible if content exists
    if st.session_state.doc_content:
        st.markdown("---")
        st.markdown("## 📖 Documentation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download Documentation",
                data=st.session_state.doc_content,
                file_name=f"documentation_{st.session_state.last_repo_url.split('/')[-1]}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col2:
            if st.button("🗑️ Clear Preview", use_container_width=True):
                st.session_state.doc_content = None
                st.session_state.documentation_path = None
                st.session_state.last_repo_url = None
                st.rerun()
        
        st.markdown("### Preview")
        st.markdown('<div class="doc-preview">', unsafe_allow_html=True)
        st.markdown(st.session_state.doc_content)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: #b0b0c0; padding: 3rem; margin-top: 4rem; border-top: 2px solid #3a3a52;">
    <h3 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Codebase Genius
    </h3>
    <p style="color: #b0b0c0 !important;">Built with ❤️ using Jac, Streamlit, Groq & Python</p>
    <p style="color: #888899 !important; font-size: 0.9rem;">© 2024 Codebase Genius. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)