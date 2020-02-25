#!/bin/bash
#SBATCH --job-name=moses-lm
#SBATCH --nodes=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=10GB
#SBATCH --time=2:00:00
#SBATCH --output=/home/staff/haukurpj/%j-%x.out
set -euxo

source $1
# LM creation
LM_DATA=${MODEL_DATA}/lm.${LANG_TO}
cat ${CLEAN_DATA}.${LANG_TO} $LM_EXTRA_DATA >$LM_DATA
run_in_singularity ${MOSESDECODER}/bin/lmplz --order $LM_ORDER --temp_prefix $WORK_DIR/ -S 10G --discount_fallback <${LM_DATA} >${LM}.arpa
run_in_singularity ${MOSESDECODER}/bin/build_binary -S 10G ${LM}.arpa ${LM}

# LM evaluation, we evaluate on 
for test_set in $TEST_PPL; do
  TEST_SET_NAME=$(basename $test_set)
  run_in_singularity ${MOSESDECODER}/bin/query ${LM} <$test_set | tail -n 4 >$MODEL_RESULTS/$TEST_SET_NAME.ppl
done