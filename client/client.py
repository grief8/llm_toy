#!/usr/bin/env python3
import json
import logging
import requests

# Import the simulated secure operation from the OP-TEE trusted world simulation.
from tee_operations import secure_ops

logging.basicConfig(level=logging.INFO)

def main():
    # Simulated complete chat history.
    chat_history = (
        "User: Hi, how are you?\n"
        "Assistant: I'm fine, thank you! How can I help you today?\n"
        "User: Could you please summarize our previous conversation about the project design?\n"
        "Assistant: Sure, let me recall the details... [detailed conversation follows]"
    )
    
    # Securely process the chat history using simulated OP-TEE operations.
    prompt = secure_ops.process_chat_history(chat_history)
    logging.info("Processed prompt (from secure world): %s", prompt)
    
    # Prepare the JSON payload with the processed prompt.
    # Note: Since our server uses TLS for secure communication,
    # we do not need additional application-layer encryption.
    payload = {"message": prompt}
    
    # URL of the inference server (running with TLS)
    url = "https://localhost:5000/inference"
    
    try:
        response = requests.post(url, json=payload, verify=False)
        response.raise_for_status()
        result = response.json()
        logging.info("Inference response received: %s", result)
        print("Inference Result:", result.get("response"))
    except requests.exceptions.SSLError as e:
        logging.error("SSL verification failed: %s", e)
        print("SSL verification failed:", e)
    except requests.exceptions.RequestException as e:
        logging.error("Error communicating with the inference server: %s", e)
        print("Failed to get inference result:", e)

if __name__ == '__main__':
    main()
