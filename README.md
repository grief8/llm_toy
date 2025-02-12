# LLM Toy Project

This project is a simple client-server application that demonstrates the use of a Language Model (LLM) in a secure environment using Occlum, a secure enclave for running applications. The project is divided into two main components: the `client` and the `server`.

## Project Structure

```
.
├── client
│   ├── client.py               # Client-side code to interact with the server.
│   └── tee_operations
│       └── secure_ops.py        # Secure operations for the client, simulating TEE-like functionality.
├── README.md                   # This documentation.
└── server
    ├── llm.yaml                # Occlum configuration file defining files to include in the secure enclave.
    ├── scripts
    │   ├── gen-cert.sh         # Script to generate self-signed TLS certificates.
    │   ├── install_python_with_conda.sh  # Script to install Python and set up a Conda environment.
    │   └── run_server_on_occlum.sh       # Script to run the server inside the Occlum secure enclave.
    └── server.py               # Server-side code implementing the LLM inference service.
```

## Prerequisites

- Docker
- Python 3.x
- Conda (installed via the provided script)

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/grief8/llm_toy.git
```

### 2. Run the Server

To run the server, you need to use Docker with Occlum. Follow these steps:

1. Start the Docker container with Occlum:

    ```bash
    docker run --rm -it --network host \
        --device /dev/sgx_enclave --device /dev/sgx_provision \
        -v ./llm_toy:/root \
        occlum/occlum:latest-ubuntu20.04 bash
    ```

2. Inside the Docker container, navigate to the `server` directory:

    ```bash
    cd server
    ```

3. Run the installation script to set up Python with Conda:

    ```bash
    ./scripts/install_python_with_conda.sh
    ```

4. Generate the necessary certificates:

    ```bash
    ./scripts/gen-cert.sh
    ```

5. Finally, run the server using the provided script:

    ```bash
    ./scripts/run_server_on_occlum.sh
    ```

### 3. Run the Client

Once the server is up and running, open a new terminal window and navigate to the `client` directory:

```bash
cd llm_toy/client
```

Run the client script:

```bash
python3 client.py
```

The client will connect to the server and start interacting with the LLM.
