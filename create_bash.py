import os 

frames = '../../../shared/shark_frames'

pre = [f for f in os.listdir(frames) if os.path.isdir(f'{frames}/{f}')]

script_format = """#!/bin/bash
#SBATCH -N 1
#SBATCH -t 3:00:00

#SBATCH -p GPU-shared
#SBATCH --gpus=4
#SBATCH --mail-type=ALL

module purge
module load AI/anaconda3-tf1.2020.11
source activate $AI_ENV

cd /ocean/projects/cis220010p/wzhangk/cv_project/py-MDNet
for f in mdnet_input/%s/*
do
        echo "Dealing with $f";
        python3 tracking/run_tracker.py -j "$f"
done
"""

for p in pre:
    curr_script = script_format % p 
    script_fn = f'bash_scripts/{p}.sh'
    # os.system(f'mkdir -p results/{p}')
    with open(script_fn, 'w') as f:
        f.write(curr_script)
