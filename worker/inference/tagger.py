# Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better. 

from flair.data import Sentence
from flair.models import SequenceTagger
from kmp_search import KMPSearch

class Tagger:
  def __init__(self):
    self.tagger = SequenceTagger.load("flair/pos-english")
    self.kmp = KMPSearch()

  def test_third_person(self, prompt):
    # After detection of NNP/VBZ tuple with NNP matching either of the parties in conversation
    # We can assume this is a third person thought and should not be presented to the user
    # and instead stored as context
    sentence = Sentence(prompt)

    # predict NER tags
    tagger.predict(sentence)

    def get_value(n):
      return n.value

    # We double all numbers using map()
    result = map(get_value, sentence.get_labels('pos'))
    print(result)
    # self.kmp.search([])


if __name__ == "__main__":
  # load tagger
  tagger = SequenceTagger.load("flair/pos-english")

  # make example sentence
  sentence = Sentence("Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better.")

  # predict NER tags
  tagger.predict(sentence)

  # print sentence
  # print(sentence)

  # print predicted NER spans
  print('The following NER tags are found:')
  # iterate over entities and print
  for entity in sentence.get_spans('pos'):
      print(entity)
      # go through each token in entity and print its idx
      for token in entity:
          print(token.idx)

