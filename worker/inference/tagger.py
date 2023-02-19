# Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better. 

from flair.data import Sentence
from flair.models import SequenceTagger

class Tagger:
  def __init__(self):
    self.tagger = SequenceTagger.load("flair/pos-english")

# TODO: Start a conversation if the module is run directly
if __name__ == "__main__":
  # load tagger
  tagger = SequenceTagger.load("flair/pos-english")

  # make example sentence
  sentence = Sentence("Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better.")

  # predict NER tags
  tagger.predict(sentence)

  # print sentence
  print(sentence)

  # print predicted NER spans
  print('The following NER tags are found:')
  # iterate over entities and print
  for entity in sentence.get_spans('pos'):
      print(entity)

