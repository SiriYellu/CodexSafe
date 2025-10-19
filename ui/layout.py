"""
Streamlit Page Layout Module

Contains main page layout and flow control
"""

import streamlit as st

from .components import (
    display_header,
    display_features,
    display_main_header,
    display_feature_badges,
    display_pro_tip,
    display_choose_your_mode,
    display_challenge_mode,
    display_analyze_mode,
    display_simple_generate_interface,
    sidebar_control_panel,
    input_method_selector,
    results_display_component,
    footer_component,
)
from .handlers import (
    initialize_session_state,
    handle_start_processing_button,
    handle_error_display,
    handle_guided_mode_processing,
)
from .styles import get_main_styles


def setup_page_config():
    """Setup optimized page configuration"""
    st.set_page_config(
        page_title="CodexSafe - Explainable Security",
        page_icon="🔒",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/SiriYellu/CodexSafe",
            "Report a bug": "https://github.com/SiriYellu/CodexSafe/issues",
            "About": "# CodexSafe - Turning Code Into Confidence\nExplainable AI Security Platform",
        },
    )


def apply_custom_styles():
    """Apply custom styles"""
    st.markdown(get_main_styles(), unsafe_allow_html=True)


def render_main_content():
    """Render main content area with improved layout"""
    # Display CodexSafe header and interface
    display_main_header()
    display_feature_badges()
    display_pro_tip()
    display_choose_your_mode()
    
    # Show different interfaces based on mode
    current_mode = st.session_state.get('current_mode', 'home')
    
    if current_mode == 'home':
        # Show CodexSafe welcome page with information
        st.markdown("## 👋 Welcome to CodexSafe!")
        st.markdown("### 🔒 Turning Code Into Confidence")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 What is CodexSafe?
            
            CodexSafe is an explainable AI security platform that helps you:
            
            - **🔍 Analyze** existing code for security vulnerabilities
            - **🎮 Practice** secure coding through interactive challenges  
            - **🚀 Generate** secure code with built-in vulnerability scanning
            - **📊 Score** your security knowledge with AI-powered feedback
            
            ### 🛡️ Security Features
            
            - OWASP Top 10 compliant scanning
            - Real-world vulnerability detection
            - Interactive challenge mode with scoring
            - AI-powered explanations for security issues
            """)
            
        with col2:
            st.markdown("""
            ### 🚀 Getting Started
            
            1. **🎯 Challenge Mode** - Test your security skills
            2. **🔍 Analyze Code** - Scan your code for vulnerabilities  
            3. **🚀 Generate Code** - Create secure code from requirements
            
            ### 🎮 Recommended First Steps
            
            Try **Challenge Mode** to get familiar with common security vulnerabilities and learn how to fix them!
            """)
        
    elif current_mode == 'challenge':
        display_challenge_mode()
        
    elif current_mode == 'analyze':
        display_analyze_mode()
        
    elif current_mode == 'generate':
        # Show simplified CodexSafe generate interface
        display_simple_generate_interface()

    # Display results if available
    if st.session_state.show_results and st.session_state.last_result:
        results_display_component(
            st.session_state.last_result, st.session_state.task_counter
        )
        st.markdown("---")
        return

    # Input interface is now handled within each mode section above

    # Display error messages if any
    handle_error_display()


def render_input_interface():
    """Render input interface"""
    # 处理引导模式的异步操作
    handle_guided_mode_processing()

    # Check if user is in guided analysis workflow
    if st.session_state.get(
        "requirement_analysis_mode"
    ) == "guided" and st.session_state.get("requirement_analysis_step") in [
        "questions",
        "summary",
        "editing",
    ]:
        # User is in guided analysis workflow, show chat input directly
        from .components import chat_input_component

        input_source = chat_input_component(st.session_state.task_counter)
        input_type = "chat" if input_source else None
    else:
        # Normal flow: show input method selector
        input_source, input_type = input_method_selector(st.session_state.task_counter)

    # Processing button - Check if requirements are confirmed for guided mode
    requirements_confirmed = st.session_state.get("requirements_confirmed", False)

    # For guided mode, if requirements are confirmed, automatically start processing
    if (
        st.session_state.get("requirement_analysis_mode") == "guided"
        and requirements_confirmed
        and input_source
        and not st.session_state.processing
    ):
        # Automatically start processing for confirmed requirements
        st.session_state.requirements_confirmed = (
            False  # Clear flag to prevent re-processing
        )
        handle_start_processing_button(input_source, input_type)
    elif (
        input_source and not st.session_state.processing and not requirements_confirmed
    ):
        # Only show Start Processing button if requirements are not already confirmed
        if st.button("🚀 Start Processing", type="primary", use_container_width=True):
            handle_start_processing_button(input_source, input_type)

    elif st.session_state.processing:
        st.info("🔄 Processing in progress... Please wait.")
        st.warning("⚠️ Do not refresh the page or close the browser during processing.")

    elif not input_source:
        st.info(
            "👆 Please upload a file, enter a URL, or describe your coding requirements to start processing."
        )


def render_sidebar():
    """Render sidebar"""
    return sidebar_control_panel()


def main_layout():
    """Main layout function"""
    # Initialize session state
    initialize_session_state()

    # Setup page configuration
    setup_page_config()

    # Apply custom styles
    apply_custom_styles()

    # Render sidebar
    sidebar_info = render_sidebar()

    # Render main content
    render_main_content()

    # Display footer
    footer_component()

    return sidebar_info
