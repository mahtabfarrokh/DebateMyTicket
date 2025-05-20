import streamlit as st
from PIL import Image
import json
import io
from debate_my_ticket.backend import OCRProcessor
from debate_my_ticket.backend import InfoScraper
from debate_my_ticket.backend import TicketValidator
from debate_my_ticket.langgraph_runner import DebateRunner
from debate_my_ticket.utils.helpers import load_debate_history

# Initialize components
ocr_processor = OCRProcessor()
info_scraper = InfoScraper()
ticket_validator = TicketValidator()
debate_runner = DebateRunner()

# Configure Streamlit page
st.set_page_config(
    page_title="DebateMyTicket",
    page_icon="🎫",
    layout="wide"
)

# App title and description
st.title("DebateMyTicket")
st.markdown("""
    Upload your ticket image and let our AI agents debate whether you should pay or challenge it.
    The agents will analyze the ticket details, local laws, and social context to provide a balanced perspective.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your ticket image", type=["jpg", "jpeg", "png"])

# Additional context input
st.subheader("Additional Context")
additional_context = st.text_area(
    "Provide any additional context about your ticket (optional)",
    height=100
)

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Ticket", width=400)
    
    # Process button
    if st.button("Analyze Ticket"):
        with st.spinner("Processing your ticket..."):
            try:
                # Convert PIL Image to bytes
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format)
                img_byte_arr = img_byte_arr.getvalue()
                
                # Process image with OCR
                ticket_info = ocr_processor.process_image(img_byte_arr)
                
                # Add additional context if provided
                if additional_context:
                    ticket_info['additional_context'] = additional_context
                
                # Gather legal and social context
                context = info_scraper.gather_context(ticket_info)
                
                # Validate ticket
                validation_issues = ticket_validator.validate_ticket(ticket_info)
                
                # Display validation results
                st.subheader("Ticket Validation")
                if validation_issues:
                    st.warning("The following issues were found with your ticket:")
                    for issue in validation_issues:
                        st.write(f"- {issue}")
                else:
                    st.success("The ticket appears to be legally valid.")
                
                # Run debate
                st.subheader("AI Debate")
                debate_history = debate_runner.run_debate(ticket_info, context)
                
                # Display debate
                for message in debate_history:
                    if message['role'] == 'pro_payment':
                        st.info(f"**Pro-Payment Agent:** {message['content']}")
                    elif message['role'] == 'anti_payment':
                        st.warning(f"**Anti-Payment Agent:** {message['content']}")
                    elif message['role'] == 'summary':
                        st.success(f"**Summary:** {message['content']}")
                
                # Add final summary
                st.subheader("Final Summary")
                summary = debate_runner.get_debate_summary()
                st.success(summary)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and LangGraph") 