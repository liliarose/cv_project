import os 

tmp = '20210910_SurferTowardsShark' 

mdnet_input = [f for f in os.listdir(f'mdnet_input/{tmp}') if f.endswith('.json')]
res = [f for f in os.listdir(f'results') if f.startswith(tmp) and f.endswith('.json')]

leftover = set(mdnet_input) - set(res)
script_format = """#!/bin/bash
#SBATCH -N 1
#SBATCH -t 3:30:00

#SBATCH -p GPU-shared
#SBATCH --gpus=4
#SBATCH --mail-type=ALL

module purge
module load AI/anaconda3-tf1.2020.11
source activate $AI_ENV

cd /ocean/projects/cis220010p/wzhangk/cv_project/py-MDNet
"""

actual_script = script_format

for f in leftover:
    actual_script += f'echo "Dealing with {f}"\n'
    actual_script += f'python3 tracking/run_tracker.py -j mdnet_input/{tmp}/{f}\n'

with open(f'{tmp}_run3.sh', 'w') as f:
    f.write(actual_script)

