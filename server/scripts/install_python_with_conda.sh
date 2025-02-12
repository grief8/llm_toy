#!/bin/bash
# Reference: https://github.com/occlum/occlum/blob/0.31.0-rc/demos/bigdl-llm/install_python_with_conda.sh

set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" >/dev/null 2>&1 && pwd )"

# Install python and dependencies to specified position
[ -f Miniconda3-latest-Linux-x86_64.sh ] || wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
[ -d miniconda ] || bash ./Miniconda3-latest-Linux-x86_64.sh -b -p $script_dir/miniconda
$script_dir/miniconda/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
$script_dir/miniconda/bin/conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
$script_dir/miniconda/bin/conda config --set show_channel_urls yes
$script_dir/miniconda/bin/conda create \
    --prefix $script_dir/python-occlum -y \
    python=3.10.0

# Install vLLM
$script_dir/python-occlum/bin/pip install vllm flask