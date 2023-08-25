from transformers import pipeline

### Uses Named Entity Recognition to map entities to subject and objects
### TODO: Needs some work to evaluate results and improve them
class EntityLinker:
    def __init__(self):
        self.nlp = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

    def link_entities(self, text):
        ner_results = self.nlp(text)
        merged_entities = [(entity_group['word'], entity_group['entity_group'])
                           for entity_group in ner_results]
        return merged_entities
    
    def link_relations(self, text):
        entities = self.link_entities(text)
        # replace first two entities in the text with special tokens
        if len(entities) >= 2:
            modified_text = text.replace(entities[0][0], "[ENT] [R1]", 1)
            modified_text = modified_text.replace(entities[1][0], "[ENT] [R2]", 1)

            # Split the modified text at "[ENT] [R2]" and keep everything to the left
            modified_text = modified_text.split("[ENT] [R2]", 1)[0] + "[ENT] [R2]"
            return entities[0][0], modified_text, entities[1][0]
        else:
            return None, None, None
