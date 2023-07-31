
# Falcon Tuning

Grab the FalconTune repository and follow the installation instructions. 

You will need an instruction data set in JSON format at `data_cleaned.json`.

```
falcontune finetune \
    --model=falcon-7b-instruct \
    --weights=tiiuae/falcon-7b-instruct \
    --dataset=./data_cleaned.json \
    --data_type=alpaca \
    --lora_out_dir=./our-peft-model/ \
    --mbatch_size=1 \
    --batch_size=2 \
    --epochs=3 \
    --lr=3e-4 \
    --cutoff_len=256 \
    --lora_r=8 \
    --lora_alpha=16 \
    --lora_dropout=0.05 \
    --warmup_steps=5 \
    --save_steps=50 \
    --save_total_limit=3 \
    --logging_steps=5 \
    --target_modules='["query_key_value"]'
``` 