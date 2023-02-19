# Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better. 

from flair.data import Sentence
from flair.models import SequenceTagger
from kmp_search import KMPSearch

TEST_1 = "Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better."

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
    print(list(result))
    idx = self.kmp.search(["NNP", ",", "VBZ"], list(result))
    print(idx)

if __name__ == "__main__":
  # load tagger
  tagger = SequenceTagger.load("flair/pos-english")

  # make example sentence
  sentence = Sentence(TEST_1)

  # predict NER tags
  tagger.predict(sentence)

  # print sentence
  print(sentence)

  tag = Tagger()
  tag.test_third_person(TEST_1)

