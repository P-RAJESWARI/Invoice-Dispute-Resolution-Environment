"""
Gradio UI for Invoice Dispute Resolution Environment
Run this locally: python ui.py
Or deploy to Hugging Face Spaces
"""

import gradio as gr
import requests
import json

# Base URL for API
BASE_URL = "http://localhost:7860"

# Global state
current_state = None
current_difficulty = "medium"


def reset_environment(difficulty):
    """Reset the environment with selected difficulty"""
    global current_state, current_difficulty
    current_difficulty = difficulty
    
    try:
        response = requests.post(
            f"{BASE_URL}/reset",
            json={"difficulty": difficulty},
            timeout=10
        )
        response.raise_for_status()
        obs = response.json()
        
        # Get initial state
        state_response = requests.get(f"{BASE_URL}/state", timeout=10)
        current_state = state_response.json()
        
        return json.dumps(obs, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def submit_decision(decision, response_text, refund_amount):
    """Submit a decision to the environment"""
    try:
        action = {
            "decision": decision,
            "response_text": response_text,
            "refund_amount": float(refund_amount) if decision == "partial_refund" and refund_amount else None
        }
        
        response = requests.post(
            f"{BASE_URL}/step",
            json=action,
            timeout=10
        )
        response.raise_for_status()
        obs = response.json()
        
        return json.dumps(obs, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_current_state():
    """Get current dispute state"""
    try:
        response = requests.get(f"{BASE_URL}/state", timeout=10)
        response.raise_for_status()
        state = response.json()
        return json.dumps(state, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Gradio Interface
with gr.Blocks(title="Invoice Dispute Resolution") as demo:
    gr.Markdown("# 🏦 Invoice Dispute Resolution Environment")
    gr.Markdown("An AI-powered system for resolving billing disputes using reinforcement learning.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 📋 Episode Control")
            
            difficulty = gr.Radio(
                choices=["easy", "medium", "hard"],
                value="medium",
                label="Select Difficulty Level"
            )
            
            reset_btn = gr.Button("🚀 Start New Episode", variant="primary")
            
            state_output = gr.Textbox(
                label="Current State",
                interactive=False,
                lines=10
            )
        
        with gr.Column():
            gr.Markdown("## 🎯 Make a Decision")
            
            decision = gr.Radio(
                choices=[
                    ("✅ Full Refund", "full_refund"),
                    ("📊 Partial Refund", "partial_refund"),
                    ("❌ Reject Dispute", "reject"),
                    ("🔔 Escalate to Manager", "escalate"),
                    ("❓ Request More Info", "request_info")
                ],
                label="Decision",
                value="full_refund"
            )
            
            response_text = gr.Textbox(
                label="Customer Response Message",
                placeholder="Draft your professional response...",
                lines=5
            )
            
            refund_amount = gr.Number(
                label="Refund Amount (if partial refund)",
                value=0,
                visible=True
            )
            
            submit_btn = gr.Button("📤 Submit Decision", variant="primary")
            
            feedback_output = gr.Textbox(
                label="Feedback & Reward",
                interactive=False,
                lines=10
            )
    
    # Connect buttons
    reset_btn.click(
        fn=reset_environment,
        inputs=[difficulty],
        outputs=[state_output]
    )
    
    submit_btn.click(
        fn=submit_decision,
        inputs=[decision, response_text, refund_amount],
        outputs=[feedback_output]
    )
    
    # Load state on demand
    gr.Markdown("---")
    gr.Markdown("## 📊 Full API Response")
    
    load_state_btn = gr.Button("🔄 Refresh State")
    full_state_output = gr.Textbox(
        label="Full Environment State",
        interactive=False,
        lines=15
    )
    
    load_state_btn.click(
        fn=get_current_state,
        outputs=[full_state_output]
    )


if __name__ == "__main__":
    demo.launch(share=True)
