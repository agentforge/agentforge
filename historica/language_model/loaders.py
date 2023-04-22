import torch, logging
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer
logger = logging.getLogger("llm")

## Loaders for different models
class Loader:
    def __init__(self, device_map="auto", multi_gpu=False, device="cuda"):
        self.config = None
        self.device_map = device_map
        self.multi_gpu = multi_gpu
        self.device = device
        self.model = None
        self.model = None

    def load(self, config, device="cuda"):
        self.config = config
        if config["model_type"] == "llama":
            self.llama(device)
        elif config["model_type"] == "huggingface":
            self.huggingface(device)
        else:
            raise ValueError(f"Unknown model type {config['model_type']}")
        return self.model, self.tokenizer

    def llama(self, device="cuda"):
        logger.info("Loading llama...")
        # self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"], decode_with_prefix_space=True, clean_up_tokenization_spaces=True)
        self.tokenizer = LlamaTokenizer.from_pretrained(self.config["model_name"], decode_with_prefix_space=True, clean_up_tokenization_spaces=True)
        self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = "left"

        self.model = LlamaForCausalLM.from_pretrained(
            self.config["model_name"],
            # load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map=self.device_map,
        )
        if "peft_model" in self.config:
            self.model = PeftModel.from_pretrained(
                self.model, self.config["peft_model"],
                torch_dtype=torch.float16,
                # device_map=device_map
            )

        #LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1 and self.multi_gpu:
            logger.info(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)
        
        if not self.multi_gpu:
            self.model.half()

    def huggingface(self, device="cuda"):
        logger.info("Loading huggingface...")
        if self.config["model_name"] == None:
            raise ValueError("model_name must be defined")

        revision = self.config.get("revision", "main")
        load_in_8bit = self.config.get("load_in_8bit", False)
        torch_dtype = self.config.get("torch_dtype", torch.float16)
        padding_side = self.config.get("padding_side", "left")
        cfg = self.config["model_name"]

        logger.info(f"Loading model... {cfg}")
        self.model = AutoModelForCausalLM.from_pretrained(
            cfg,
            load_in_8bit=load_in_8bit,
            torch_dtype=torch_dtype,
            device_map=self.device_map,
            revision=revision,
            trust_remote_code=True
        )
        logger.info("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config["tokenizer_name"], padding_side=padding_side)

        # if self.config["tokenizer_name"] == "OpenAssistant/oasst-sft-1-pythia-12b":
        #     special_tokens_dict = {'additional_special_tokens': ['<|prompter|>', '<|assistant|>']}
        #     num_added_toks = self.tokenizer.add_special_tokens(special_tokens_dict)
        #     print('We have added', num_added_toks, 'tokens')
        #     self.model.resize_token_embeddings(len(self.tokenizer))  # Notice: resize_token_embeddings expect to receive the full size of the new vocabulary, i.e. the length of the tokenizer.

        # # LLM Models need GPU
        device = torch.device(device)
        if torch.cuda.device_count() > 1 and self.multi_gpu:
            logger.info(f"Using {torch.cuda.device_count()} GPUs")
            self.model = torch.nn.DataParallel(self.model)
    
        self.model = self.model.to(self.device)
        self.model.eval()  # Set the model to evaluation mode
        logger.info(f"Model loaded and online...")
