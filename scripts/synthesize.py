import os
import torch
import pandas as pd
import random
from typing import List, Tuple
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments

### This script is based off of the ORCA
# Step 1: Dataset Construction
class DatasetConstructor:
    def __init__(self, flan_v2_path: str, prompt_distribution: dict):
        self.flan_v2_path = flan_v2_path
        self.prompt_distribution = prompt_distribution

    def convert_system_messages(self, key: str, value: str):
      # Replace underscores with spaces
      main_key = key.replace('_', ' ')
      
      # Check if "an" should be used instead of "a"
      prefix = "You are an " if main_key.split()[0].lower()[0] in 'aeiou' else "You are a "
      
      original_string = f"{prefix}{main_key}. {value}"
      return original_string

    def load_dataset(self) -> Tuple[List[str], List[str]]:
        # Load the queries from the Parquet file
        data = pd.read_parquet(os.path.join(self.data_path, "user_inputs.parquet"))
        queries = data["inputs"].tolist()  # Assuming the column name is 'query'

        # Load system messages - in practice these would be loaded from a file or database
        system_messages = {
            'AI_assistant': 'Provide a detailed answer so the user doesn’t need to search outside to understand the answer.',
            'teacher': 'Given a task, you explain in simple steps what the task is asking, any guidelines it provides and how to use those guidelines to find the answer.',
            'concise_AI_assistant': 'Provide a concise response that directly answers the user query.',
            'historian': 'Provide historical context and insights when answering the user query.',
            'scientist': 'Give a response grounded in scientific evidence and reasoning.',
            'storyteller': 'Craft a creative and engaging story relevant to the user query.',
            'AI_ethicist': 'Ensure your response is ethical and considers societal impacts.',
            'news_reporter': 'Your response should be factual and unbiased.',
            'critic': 'Provide a critical analysis in response to the user query.',
            'coach': 'Motivate and inspire through your response.',
            'technical support agent': 'Give a step-by-step guide to resolve an issue in the user query.',
            'language tutor': 'Correct any language mistakes and explain grammar rules in your response.',
            'financial advisor': 'Give advice grounded in economic theory and data.',
            'physician': 'Provide medical information based on current guidelines and research.',
            'lawyer': 'Provide legal information in your response.',
            'customer_service_representative': 'Your response should be polite and focused on solving the user’s issue.'
        }

        return system_messages, queries
    
    def input_generator(self, factual_texts: List[str], output_parquet_file: str) -> None:
        questions = []
        for factual_text in factual_texts:
            # Generating a prompt to instruct the language model to create 5 unique questions
            prompt = f"{factual_text}\nProvide 5 unique questions based on the factual text provided."
            
            # Using SyntheticDataGenerator to generate text
            system_message = "You are an AI assistant."
            generated_text = self.data_generator.generate_responses(system_message, prompt)
            
            # Split the generated text into individual questions
            questions = generated_text.split('\nsystem_message')[1:]  # The first line will be the prompt
            
            # Save questions and ratios to lists
            questions.extend(questions)

        # Convert lists to DataFrame
        questions_df = pd.DataFrame(questions)

        # Save DataFrame to Parquet file
        questions_df.to_parquet(output_parquet_file)

    # Construct data triplets (minus response)
    def construct_data_triplets(self, system_messages: List[str], queries: List[str]) -> List[Tuple[str, str]]:
        # Combine system messages and user queries to form data pairs
        data_pairs = []
        for query in queries:
            system_message = random.choice(system_messages)
            data_pairs.append((system_message, query))

        return data_pairs

# Step 2: Synthetic Data Generation
class SyntheticDataGenerator:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate_responses(self, system_message: str, user_query: str) -> str:
        # Combine system_message and user_query to form the prompt
        prompt = system_message + " " + user_query
        
        # Encode the prompt and generate the response
        inputs = self.tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
        outputs = self.model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4)

        # Decode the outputs and return the result
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response


# Step 3: Orca Model Training
class OrcaModelTrainer:
    def __init__(self, train_data: List[Tuple[str, str, str]], eval_data: List[Tuple[str, str, str]]):
        # Initialize model, tokenizer, and other training setup
        # (Here I'm using BART as a placeholder, replace it with the Orca model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")
        self.train_data = train_data
        self.eval_data = eval_data

    def train(self):
        # Define the training arguments
        training_args = Seq2SeqTrainingArguments(
            output_dir="./results",
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            num_train_epochs=3,
            logging_dir="./logs",
        )

        # Create a Seq2Seq Trainer
        self.trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=self.train_data,
            eval_dataset=self.eval_data,
            tokenizer=self.tokenizer,
        )

        # Train the model
        self.trainer.train()

    def evaluate(self):
        # Evaluate the model
        # (assuming self.eval_data is properly formatted and tokenized)
        results = self.trainer.evaluate(self.eval_data)
        print(results)


if __name__ == "__main__":
    # Configuration for the prompt distribution
    prompt_distribution = {
        "zero_shot": 0.4,  # 40% zero-shot prompts
        "few_shot": 0.3,   # 30% few-shot prompts
        "chain_of_thought": 0.3  # 30% chain-of-thought prompts
    }

    # Example factual texts from a textbook
    ## TODO: Bring in factual texts from data uploading pipeline
    factual_texts = [
        "The Earth is the third planet from the Sun and the only astronomical object known to harbor life. It has a single natural satellite, the Moon.",
        "Photosynthesis is the process by which plants, algae, and some bacteria use sunlight, carbon dioxide, and water to produce carbohydrates and oxygen."
    ]

    # Step 1: Generate questions based on the factual texts and save to a Parquet file
    dataset_constructor = DatasetConstructor("<path_to_flan_v2>")
    dataset_constructor.input_generator(factual_texts, "output.parquet", n_zero_shot=0.3, n_few_shot=0.5, n_chain_of_thought=0.2)

    # Step 2: Construct the dataset
    dataset_constructor = DatasetConstructor("<path_to_flan_v2>", prompt_distribution)
    system_messages, queries = dataset_constructor.load_dataset()
    data_pairs = dataset_constructor.construct_data_triplets(system_messages, queries)

    # Step 3: Generate synthetic data
    synthetic_data_generator = SyntheticDataGenerator()
    synthetic_data = []
    for system_message, user_query in data_pairs:
        response = synthetic_data_generator.generate_responses(system_message, user_query)
        synthetic_data.append((system_message, user_query, response))

    # Step 4: Train Orca model (split synthetic_data into train and eval sets)
    train_data = synthetic_data[:-100]  # All but last 100 samples for training
    eval_data = synthetic_data[-100:]  # Last 100 samples for evaluation

    orca_trainer = OrcaModelTrainer(train_data, eval_data)
    orca_trainer.train()
    orca_trainer.evaluate()
