#!/bin/sh
#SBATCH -A ACD111031        # Account name/project number
#SBATCH -J dat_parse        # Job name
#SBATCH -p ct56             # Partition name
#SBATCH -n 56               # Number of MPI tasks (i.e. processes)
#SBATCH -N 1                # Maximum number of nodes to be allocated
#SBATCH -o ./parse_log/%j.out           # Path to the standard output file
#SBATCH -e ./parse_log/%j.err           # Path to the standard error ouput file

module load biology/Python/3.9
module load compiler/gcc/9.4.0
python3 parse_data.py no

# to upload to slurm, run the following command:
# sbatch parse_data.sh
