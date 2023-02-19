# Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better. 

from flair.data import Sentence
from flair.models import SequenceTagger
from kmp_search import KMPSearch

TEST_1 = "Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better."

class Tagger:
  def __init__(self):
    self.tagger = SequenceTagger.load("flair/pos-english")
    self.kmp = KMPSearch()

  # Returns the earliest index of a possible hit for third person rhetoric
  def test_third_person(self, prompt):
    # After detection of NNP/VBZ tuple with NNP matching either of the parties in conversation
    # We can assume this is a third person thought and should not be presented to the user
    # and instead stored as context
    sentence = Sentence(prompt)

    # predict NER tags
    tagger.predict(sentence)

    def get_value(n):
      return str(n.value)

    def get_text(n):
      return n.data_point.text

    # We double all numbers using map()
    labels = sentence.get_labels('pos')
    result = map(get_value, labels)
    texts = map(get_text, labels)

    v=list(result)
    t=list(texts)
    self.kmp.search(["NNP", "," ,"VBZ"], v)
    #print(v)
    #print(t)
    #print(self.kmp.indexes)
    #print(len(t))
    #print(min(self.kmp.indexes))
    #for i in self.kmp.indexes:
    #  print(t[int(i)-1:int(i)+3])
    return min(self.kmp.indexes)


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

