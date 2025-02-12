#!/usr/bin/env python3
import os
import json
import logging
from flask import Flask, request, jsonify

# Try to import vLLM for actual inference
try:
    from vllm import LLMEngine, SamplingParams
    vllm_available = True
except ImportError:
    vllm_available = False
    logging.warning("vLLM module not available. Using dummy inference instead.")


app = Flask(__name__)

cert = os.path.join(app.root_path, 'flask.crt')
cert_key = os.path.join(app.root_path, 'flask.key')

# Initialize vLLM engine if available
if vllm_available:
    logging.info("Initializing vLLM engine with model deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    engine = LLMEngine(model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
    def vllm_inference(prompt: str) -> str:
        # Configure sampling parameters (adjust max_tokens, temperature, etc. as needed)
        sampling_params = SamplingParams(max_tokens=50, temperature=0.7)
        result = engine.generate(prompt, sampling_params)
        return result
else:
    def vllm_inference(prompt: str) -> str:
        # Fallback dummy inference: simply return a truncated summary
        if len(prompt) > 50:
            return f"Summary: {prompt[:50]}..."
        else:
            return f"Summary: {prompt}"

@app.route('/inference', methods=['POST'])
def infer():
    """
    Inference API endpoint.
    
    Accepts a JSON payload with a "message" field, processes the message using vLLM inference,
    and returns a JSON response containing the inference result.
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing "message" field in request'}), 400

        user_message = data['message']
        logging.info("Received message: %s", user_message)

        # Perform inference using vLLM (or fallback dummy implementation)
        inference_result = vllm_inference(user_message)
        logging.info("Inference result: %s", inference_result)

        return jsonify({'response': inference_result}), 200

    except Exception as e:
        logging.exception("Error during inference processing")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Run the Flask app with TLS using self-signed certificates
    ssl_context = (cert, cert_key)
    print('-----server ready-----')
    app.run(host='0.0.0.0', port=5000, threaded=True, ssl_context=ssl_context)
