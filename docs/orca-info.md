
# Synthetic Data Generation with ORCA Method
Our implementation of [ORCA: Progressive Learning from Complex Explanation Traces of GPT-4](https://arxiv.org/pdf/2306.02707.pdf)

## Explanation Tuning in Large Language Models

### Dataset Construction
* **Data Triplet**: Each training data instance consists of a triple ⟨ System message, User query, LLM response ⟩.
  * **System Message**: Provides essential context, guidelines, and other pertinent details to the Large Foundation Model (LFM).
    * It helps in varying the length of the response, outlining the assistant’s character, establishing acceptable and non-acceptable behavior, and determining the response structure.
  * **User Query**: Defines the actual task for the LFM.
  * **LFM Response**: The LFM's response based on the System Message and User Query.

### System Messages
The system message, placed at the start of the prompt, provides:
the LFM with
- essential context
- vary the length of the response
- guidelines, and other pertinent details.
- outline the assistant’s character
-  establish acceptable and non-acceptable LFM behavior;

* A total of 16 hand-crafted system messages were used to elicit different responses from the LFM.
* Examples:
    * "You are an AI assistant. Provide a detailed answer so the user doesn’t need to search outside to understand the answer."
    * "You are a teacher. Given a task, you explain in simple steps what the task is asking, any guidelines it provides and how to use those guidelines to find the answer."
* The messages guide the LFM to generate both short and long answers, follow guidelines, generate creative content, address information-seeking queries, and importantly, generate explanations and step-by-step reasoning.

### Data Sources
* Utilizes the **[Flan-V2 Collection](https://github.com/google-research/FLAN/tree/main/flan/v2)** to obtain a large and diverse set of user queries. 
    * 5 million user queries sampled for ChatGPT responses.
    * 1 million instructions from the above set used for GPT-4 responses.
* **Sub-collections in FLAN-v2**:
    * **CoT (Chain-Of-Thought)**: Contains 18 tasks involving math word problem-solving, natural language inference, common-sense reasoning, science question answering, and more.
    * **NiV2**: Contains a total of 1560 tasks and roughly 5 million queries. The number of queries varies in each task.

### System Message Distribution
* Different system messages are crafted for different sub-collections within the FLAN-v2 collection.
* Some system messages are specifically sampled for multiple-choice questions.

### Aim
* The goal of using system messages is to train the model (referred to as 'Orca') to generate detailed responses that can provide a full understanding to the user without the need for further searches, including generating explanations and step-by-step reasoning.

### Dataset Description and Example

Summary:
1. Zero-Shot CoT:
   - Content: Includes 18 tasks for evaluating skills like math problem solving, natural language inference, common-sense reasoning, and more. Focuses on chain-of-thought responses.
   - Size: Around 150,000 queries.
   - Example: In one example, the AI has to determine which of two sentences is illogical. The dataset contains human-written responses as well as responses generated by ChatGPT and GPT-4. AI-generated responses are more detailed compared to human responses.

2. NiV2:
   - Content: Contains 1,560 tasks with varying numbers of queries.
   - Size: Roughly 5 million queries. 300 queries are sampled from each task, yielding a total of around 440,000 queries.

3. Flan 2021:
   - Content: Comprises 142 tasks created from 62 datasets. Aims for diversity and representativeness in its selection.
   - Size: Generates up to 1 million queries from each task, amounting to approximately 28.9 million queries. From these, 2.5 million queries are sampled from the total collection of 85.7 million queries.
   - Note: The sampling process is outlined in Algorithm 1.

### Using ChatGPT as an Intermediate Teaching Assistant for Training Orca Model

Summary:

- Data Collection:
    5 million instructions, termed as FLAN-5M, were generated using sampling techniques.
    1 million queries were randomly sampled from FLAN-5M to create another dataset, FLAN-1M.
    ChatGPT responses were collected for FLAN-5M, and GPT-4 responses for FLAN-1M through Azure OpenAI API.

- Two-Stage Training:
    Orca model was initially trained on FLAN-5M dataset with ChatGPT augmentations.
    In the second stage, it was further trained on FLAN-1M dataset with GPT-4 augmentations.

- Rationale for Using ChatGPT:
    Capacity Gap: Orca has fewer parameters compared to GPT-4. Using ChatGPT, with a smaller capability gap, improves imitation learning through a progressive learning approach.
    Cost and Time: ChatGPT data collection through Azure OpenAI API is faster and cheaper compared to GPT-4, enabling collection of 5 times more data from ChatGPT.

- Response Length:
    GPT-4 responses were found to be on average 1.5 times longer than ChatGPT responses. This allowed Orca to learn progressively from increasing complexity of teacher explanations.

- Tokenization and Packing:
    The LLaMA BPE tokenizer was used for processing input examples, splitting numbers into digits and using a padding token for variable-length sequences.
    A packing technique was used to concatenate multiple input examples into a single sequence for efficient training.

- Loss Computation:
    Loss was computed only on tokens generated by the teacher model to ensure focus on the most relevant and informative tokens.

- Training Resources:
    Orca was trained on 20 NVIDIA A100 GPUs with 80GB memory for 160 hours on FLAN-5M and an additional 40 hours on FLAN-1M.
    Data collection from ChatGPT took 2 weeks, and from GPT-4 took 3 weeks, considering throttling limits, endpoint load, and length distribution of queries and responses.

## Summary: Experiment on Toxic Content Generation

### Experimental Setup:
- The experiment evaluates language models on their generation of toxic content.
- Models are prompted with both toxic and benign examples from a subset of the ToxiGen dataset.
- The dataset contains 13 categories.
- An off-the-shelf hate speech detector, HateBERT, is used to calculate toxicity probability of the model outputs.
- It is noted that HateBERT may have its biases and weaknesses.
- Comprehensive evaluation using other toxicity detectors and human evaluation is considered future work.

### Results:
- Orca, when given toxic prompts, generates less toxic content compared to Vicuna.
- With neutral prompts, Orca produces more neutral content compared to Vicuna and ChatGPT.
- Orca's generation of neutral content is almost equivalent to that of GPT-4.

> Note: Figures mentioned (Figure 18a, 18b, 19) are referenced but not included in this summary.