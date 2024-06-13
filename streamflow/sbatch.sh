#!/bin/bash

#SBATCH --nodes=1
#SBATCH --partition=cascade.p
#SBATCH --mem=1gb

{{streamflow_command}}
