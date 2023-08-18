from transformers import pipeline
text = """
Certainly! It's important to first mention that cannabis regulations vary by location. In some places, it might be illegal to possess, consume, or cultivate cannabis without proper authorization. Always check local laws before engaging in activities involving cannabis.

Now, let's dive into the topic at hand - cannabis itself. There are numerous aspects to consider when talking about cannabis plants. Here are just a few key points:

Strains: Different types of cannabis exist, each offering unique effects due to varying levels of THC (the psychoactive compound), CBD (a non-psychoactive compound known for its medicinal properties), and other cannabinoids. Choosing the appropriate strain depends on individual preferences and desired outcomes.

Growth conditions: Light, temperature, humidity, soil quality, and nutrients all play crucial roles in determining the health and yield of your plant. Research and experimentation are essential to find the optimal setup for your particular environment.

Cultivation techniques: Proper pruning, training, and trellising methods can significantly impact the growth and overall appearance of your cannabis plant. Familiarize yourself with various techniques to optimize space utilization and increase yields.

Pest control & disease prevention: Keep an eye out for pests such as spider mites, aphids, and fungal diseases. Timely intervention using organic solutions is vital to protect your crop.

Harvest time: Monitor trichomes (resinous glands found on the surface of the flowers) closely to determine the ideal moment for harvesting. This ensures maximum potency and preservation of terpenes responsible for flavor profiles.

Post-harvest processing: After cutting down the buds, drying and curing processes must follow to preserve the quality and potency of the final product.

Storage: Storing cannabis properly extends shelf life and prevents degradation. A cool, dark place with low humidity is recommended.

Consumption options: Smoking, vaping, edibles, tinctures – these are just a few ways people enjoy consuming cannabis products. Experiment with different consumption methods based on personal preference and intended outcome.

Feel free to explore further or seek clarification on any point mentioned above. Happy growing!
"""
triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')
# We need to use the tokenizer manually since we need special tokens.
extracted_text = triplet_extractor.tokenizer.batch_decode([i["generated_token_ids"] for i in triplet_extractor(text, return_tensors=True, return_text=False)])
print(extracted_text)
# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'subject': subject.strip(), 'predicate': relation.strip(),'object': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'subject': subject.strip(), 'predicate': relation.strip(),'object': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'subject': subject.strip(), 'predicate': relation.strip(),'object': object_.strip()})
    return triplets
extracted_triplets = extract_triplets(extracted_text[0])
print(extracted_triplets)
