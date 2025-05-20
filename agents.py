from typing import Dict, List, TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
import json
from PIL import Image
import base64
from io import BytesIO
import configparser
import os

# Load API key from config file
config = configparser.ConfigParser()
config.read('api.cfg')
os.environ["OPENAI_API_KEY"] = config['openai']['api_key']

# State definition
class DebateState(TypedDict):
    messages: List[Dict]
    ticket_info: Dict
    current_turn: str  # "pro" or "anti"
    pro_messages: int
    anti_messages: int
    pro_gave_up: bool
    anti_gave_up: bool

# Initialize LLMs
gpt4_vision = ChatOpenAI(model="gpt-4o", max_tokens=1000)
gpt4_mini = ChatOpenAI(model="gpt-4o", max_tokens=1000)

def encode_image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def info_gather(state: DebateState) -> DebateState:
    """Extract information from the ticket image using GPT-4 Vision"""
    image = state["ticket_info"]["image"]
    base64_image = encode_image_to_base64(image)
    
    prompt = """Analyze this ticket image and extract the following information:
    1. Address where the ticket was issued
    2. Whether the ticket appears valid
    3. Timestamp of the violation
    4. Whether there's a signature
    5. Any car information (license plate, make, model)
    
    Format the response as a JSON object with these fields."""
    
    response = gpt4_vision.invoke([
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }
        ])
    ])
    
    # Parse the response and update state
    try:
        info = json.loads(response.content)
        state["ticket_info"].update(info)
    except:
        state["ticket_info"]["raw_text"] = response.content
    
    return state

def should_end(state: DebateState) -> bool:
    """Check if the debate should end"""
    return (state["pro_messages"] >= 5 and state["anti_messages"] >= 5) or state["pro_gave_up"] or state["anti_gave_up"]

def is_pro_turn(state: DebateState) -> bool:
    """Check if it's pro's turn"""
    return state["current_turn"] == "pro" and not should_end(state)

def is_anti_turn(state: DebateState) -> bool:
    """Check if it's anti's turn"""
    return state["current_turn"] == "anti" and not should_end(state)

def router(state: DebateState) -> str:
    """Determine the next step in the debate"""
    if should_end(state):
        return "end"
    
    return state["current_turn"]

def pro_payment(state: DebateState) -> DebateState:
    """Pro-payment agent's turn"""
    messages = state["messages"]
    ticket_info = state["ticket_info"]
    
    prompt = f"""You are arguing in favor of paying the ticket. Here's the ticket information:
    {json.dumps(ticket_info, indent=2)}
    
    Previous debate:
    {json.dumps(messages, indent=2)}
    
    Make your argument. If you want to give up, respond with "GIVE_UP"."""
    
    response = gpt4_mini.invoke([HumanMessage(content=prompt)])
    
    if "GIVE_UP" in response.content:
        state["pro_gave_up"] = True
    else:
        state["messages"].append({"role": "pro", "content": response.content})
        state["pro_messages"] += 1
    
    state["current_turn"] = "anti"
    return state

def anti_payment(state: DebateState) -> DebateState:
    """Anti-payment agent's turn"""
    messages = state["messages"]
    ticket_info = state["ticket_info"]
    
    prompt = f"""You are arguing against paying the ticket. Here's the ticket information:
    {json.dumps(ticket_info, indent=2)}
    
    Previous debate:
    {json.dumps(messages, indent=2)}
    
    Make your argument. If you want to give up, respond with "GIVE_UP"."""
    
    response = gpt4_mini.invoke([HumanMessage(content=prompt)])
    
    if "GIVE_UP" in response.content:
        state["anti_gave_up"] = True
    else:
        state["messages"].append({"role": "anti", "content": response.content})
        state["anti_messages"] += 1
    
    state["current_turn"] = "pro"
    return state

def create_debate_workflow() -> StateGraph:
    """Create the debate workflow graph"""
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("info_gather", info_gather)
    workflow.add_node("router", router)
    workflow.add_node("pro_payment", pro_payment)
    workflow.add_node("anti_payment", anti_payment)
    
    # Add edges
    workflow.add_edge(START, "info_gather")
    workflow.add_edge("info_gather", "router")
    
    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        {
            "pro_payment": is_pro_turn,
            "anti_payment": is_anti_turn,
            END: should_end
        }
    )
    
    # Add edges back to router
    workflow.add_edge("pro_payment", "router")
    workflow.add_edge("anti_payment", "router")
    
    return workflow.compile() 