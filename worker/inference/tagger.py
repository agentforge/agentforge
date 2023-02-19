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
    idx = min(self.kmp.indexes)
    test_str = "".join(t[int(idx):int(idx)+2])
    return prompt.index(test_str)

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
  thought_index = tag.test_third_person(TEST_1)
  if thought_index == None:
    print("NO THOUGHT INDEX")
  phrase = TEST_1[0:thought_index]
  thought = TEST_1[thought_index:len(TEST_1)]
  print(f"PHRASE: {phrase}")
  print(f"THOUGHT: {thought}")

