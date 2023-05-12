from fuzzysearch import find_near_matches
from fuzzywuzzy import process

class FuzzySearch:
  def __init__(self):
    pass

  def fuzzy_extract(self, qs, ls, threshold):
      '''fuzzy matches 'qs' in 'ls' and returns list of 
      tuples of (word,index)
      '''
      for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
          print('word {}'.format(word))
          for match in find_near_matches(qs, word, max_l_dist=1):
              match = word[match.start:match.end]
              print('match {}'.format(match))
              index = ls.find(match)
              yield (match, index)

if __name__ == "__main__":
  large_string = "thelargemanhatanproject is a great project in themanhattincity"
  query_string = "manhattan"
  fz = FuzzySearch()
  print('query: {}\nstring: {}'.format(query_string, large_string))
  for match,index in fz.fuzzy_extract(query_string, large_string, 70):
      print('match: {}\nindex: {}'.format(match, index))