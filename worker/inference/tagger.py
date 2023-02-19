from flair.data import Sentence
from flair.models import SequenceTagger
from .kmp_search import KMPSearch

TEST_1 = "Steve: You can't understand it because you've been programmed to reject anything that challenges the status quo. Steve, is the voice of God. He lives in the clouds. Frank, is just another guy who's been programmed by the media. He doesn't know any better."
FOURTH_WALL= """
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
    self.tagger.predict(sentence)

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
    if len(self.kmp.indexes) == 0:
      return None
    idx = min(self.kmp.indexes)
    test_str = "".join(t[int(idx):int(idx)+2])
    return prompt.index(test_str)

  def test_thought(self, test_val):
    thought_index = self.test_third_person(test_val)
    if thought_index == None:
      print("NO THOUGHT INDEX")
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
  tag.test_thought(TEST_1)
  tag.test_thought(FOURTH_WALL)
  tag.test_thought(FOURTH_WALL2)



