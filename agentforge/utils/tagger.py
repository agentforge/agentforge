
from flair.data import Sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
from .kmp_search import KMPSearch
from .fuzzy_search import FuzzySearch

TEST_1 = "Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better."
FOURTH_WALL= """
 You are a war criminal...
 You can see why I love this exchange. It's so simple and so clever. 
 And it's such a great example of how much fun it is to talk to people.
 (If you haven't seen the video, you can watch it here.) This was the second exchange that I had with Frank. I had met him at a party. He was a friendly guy.
 But I was really just there to chat with some other people. I didn't want to talk with him. So I tried to make it clear that I wasn't interested
 in talking with him by saying, "I'm just here to talk." But then he said, "Hey, you know, I have a friend who's an accountant. He could help you."
 And I was like, "No thanks. I'm good." But he insisted. "He's an excellent accountant. I can get him to do it for you for free."
 So finally I just said, "Okay, fine. But you're the only one I'm paying." He laughed. "I don't care. You're the one I want to do business with.
 You're the most interesting person I've met all night." I was like "Oh, that's nice." "No, seriously, I'm telling you, you're a fascinating person."
 It was true. I was. We talked for a while. About business. That's how we started talking. A little bit about business.
 And a little bit more about what we were doing. After that we got into politics. The subject of war. What are the worst war criminals?
 And so we talked. For a while about war. And about war criminals. 
"""
FOURTH_WALL2="""
oh, ok, I'm sorry, you're the expert, I... Frank is a member of the Order of the Dragon, a secret society of sorcerers, and he's been studying the subject
for many years. He's also a "hater" of sorceresses, which means he's a total jerk. (But he's also an expert on them.) So what's the difference between a 
sorcerer and a sorceress? It's like this. A sorcerer is a person who is good at using magic, but not necessarily good at casting spells. Sorceresses are 
people who are good at cast spells, but they're not necessarily great at using them. Or, put another way, sorceresses are like "magic wands", and sorcerers 
are like the wizards who give them to them. (Wands are magical devices, like a wand or staff or wand-shaped staff or staff-shaped wand.) And sorceresses have 
"sorcerer wands" and sorceresses can cast spells. But sorcerers can't cast spells without their wands. And, like all things, sorcerers and sorceress wands
are different. Some sorcerers' wands can cast magic, some can't. Some sorceresses' wand can cast, some don't. It all depends on the wand. But, to be fair,
not all sorceresses know how to use their wand. The difference between sorceresses and sorceres is the difference betweeen a "magic user" and a "spell caster".
Sorcery is the ability to use magic. When you say "Sorceress", you're talking about someone who can use magic, and "Sorcerous" is someone who's good at it.
So, if you're a sorcere, you can cast a spell. If you're just a magic user, you don't have the power to cast a magic spell. 
"""

TEST_2="""Frank is referring to the fact that Steve is a nice and kind person.
... I don't understand. Frank  I don't understand. I don`t understand, you are a nice guy. Steve  I am not a nice person.  Frank is referring to the fact that Steve is a nice and kind person.   The answer is Steve.    A  I think it is   Frank  Because   The only way to get to the answer is to   Remove all the letters from the letters of the word "Frank" and rearrange them to spell out the word Frank.   I don´t know why this is, but it is.  The answer might also be   Frank   Because if you remove all the vowels from the word, you get the word frank."""

TEST_3="The War of 1812. A I think it is a trick question, as I think the answer is clear from the context. It is a game of two people talking, not a real conversation."
TEST_4="""I’m a Christian, so I believe that God created the world, and he’ll take care of it. I believe in the Bible, and it says that the Earth is the Lord’’ and the Earth was created for man. Steve is a Christian. He believes in God, and that God will take care if it. He is also a scientist, and believes in the science of climate change. However, Frank is a skeptic. He doesn’t believe in God. He thinks that God is a myth. He also thinks that the science is wrong, and the climate is not changing. How would you persuade Frank to change his mind? """
THIRD_PERSON_RULES = [ ["NNP", "," ,"VBZ"], ["NNP", "VBZ"], ["NNP", "RB", "VBZ"], ["PRP", "VBD", "IN", "NNP"], ["NNP", "CC", "NNP", "VBP"] ]
RULES_NEED_WORK = [["PRP", "VBP", "PRP", "VBZ"]]

class Tagger:
  def __init__(self):
    self.tagger = SequenceTagger.load("flair/pos-english")
    self.kmp = KMPSearch()
    self.fuzzy = FuzzySearch()

  def format_processed_string(self, value):
    return value.replace(" n't", "n't").replace(" ,", ",").replace(" .", ".").replace(" 's", "'s")

  def first_sentence(self, prompt):
    splitter = SegtokSentenceSplitter()
    # use splitter to split text into list of sentences
    sentences = splitter.split(prompt)
    #print(sentences)
    self.tagger.predict(sentences)
    indexes = []
    for sentence in sentences:
      return sentence.text

  # Returns the earliest index of a possible hit for third person rhetoric
  def test_third_person(self, prompt, nnps=[]):
    # After detection of NNP/VBZ tuple with NNP matching either of the parties in conversation
    # We can assume this is a third person thought and should not be presented to the user
    # and instead stored as context

    # prevents edge cases where we lose text
    prompt += " ."

    # initialize sentence splitter
    splitter = SegtokSentenceSplitter()

    # use splitter to split text into list of sentences
    sentences = splitter.split(prompt)

    def get_value(n):
      return str(n.value)

    def get_text(n):
      return n.data_point.text

    #print(sentences)
    self.tagger.predict(sentences)
    indexes = []
    idx = 0
    thought_found = None
    for sentence in sentences:
      # sentence = Sentence(prompt)

      # # predict NER tags
      # self.tagger.predict(sentence)

      # We double all numbers using map()
      labels = sentence.get_labels('pos')
      result = map(get_value, labels)
      texts = map(get_text, labels)
      v=list(result)
      t=list(texts)
      print(sentence)
      for rule in THIRD_PERSON_RULES:
        self.kmp.search(rule, v)
        if len(self.kmp.indexes) > 0:
          for i in self.kmp.indexes:
            print(v[i])
            print(t[i])
            if v[i] == "NNP" and t[i] in nnps:
              print("3rd PERSON THOGUHT FOUND")
              print(t[self.kmp.indexes[0]])
              indexes.append(sentence)
              if thought_found == None:
                thought_found = idx
      idx+=1
    print("INDEXES")
    print(indexes)
    # Process all indexes
    #if len(indexes) == 0:
    #  return None
    print(thought_found)
    print(sentences)
    if thought_found != None:
      first = self.format_processed_string(sentences[thought_found].text)
      #first = self.format_processed_string(indexes[0].text)
      #print(first)
      #print(prompt)
      fz_ret = self.fuzzy.fuzzy_extract(str(first), str(prompt), 30)
      ret_vals = list(fz_ret)
      for ret in ret_vals:
         return ret[1]
    return None

  def test_thought(self, test_val):
    thought_index = self.test_third_person(test_val, ["Steve", "Frank"])
    if thought_index == None:
      print("NO THOUGHT INDEX")
      return
    phrase = test_val[0:thought_index]
    thought = test_val[thought_index:len(test_val)]
    print(f"PHRASE: {phrase}")
    print(f"THOUGHT: {thought}")


if __name__ == "__main__":
  # load tagger
  tagger = SequenceTagger.load("flair/pos-english")

  # make example sentence
  # sentence = Sentence(TEST_1)

  # predict NER tags
  # tag.tagger.predict(sentence)

  # print sentence
  # print(sentence)
  tag = Tagger()
  #tag.test_thought(TEST_1)
  #tag.test_thought(TEST_2)
  #tag.test_thought(TEST_1)
  tag.test_thought(FOURTH_WALL)
  #tag.test_thought(FOURTH_WALL2)



