#!/bin/bash
set -e

BLUE='\033[1;34m'
NC='\033[0m'

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" >/dev/null 2>&1 && pwd )"
python_dir="$script_dir/occlum_instance/image/opt/python-occlum"

rm -rf occlum_instance && occlum new occlum_instance
pushd occlum_instance
# Use llm.yaml to copy required files and directories into the Occlum image
copy_bom -f ../llm.yaml --root image --include-dir /opt/occlum/etc/template

new_json="$(jq '.resource_limits.user_space_size = "32GB" |
                .resource_limits.kernel_space_heap_size = "1GB" |
                .resource_limits.max_num_of_threads = 500 |
                .env.default += ["PYTHONHOME=/opt/python-occlum"] |
                .env.default += ["PATH=/bin"] |
                .env.default += ["HOME=/root"] |
                .env.untrusted += ["HF_DATASETS_CACHE", "OMP_NUM_THREADS"]' Occlum.json)" && \
echo "${new_json}" > Occlum.json

occlum build
OMP_NUM_THREADS=16 occlum run /bin/python3 -u /bin/server.py 
popd
