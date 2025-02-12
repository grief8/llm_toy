"""
This module simulates OP-TEE Trusted Application (TA) operations.
In a production design, this code would run within an OP-TEE secure environment,
handling sensitive operations (e.g., processing and redacting chat history, 
encryption/decryption, and secure key management).

For this simulation, the secure function simply extracts the last part of the chat history
to serve as the inference prompt.
"""

def process_chat_history(chat_history: str) -> str:
    """
    Simulate secure processing of chat history within a TEE.
    
    In a full OP-TEE design, this function would run in the secure world,
    performing sensitive data processing, redaction, and (if necessary) encryption.
    
    For simulation, we simply return the last 100 characters of the chat history.
    """
    return chat_history[-100:] if len(chat_history) > 100 else chat_history
