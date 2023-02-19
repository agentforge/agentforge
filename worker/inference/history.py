import sqlite3
import datetime
import re

# Stores History of the relationship between man and machine
class History:
  def __init__(self, robot_name="Robot"):
    self.history = []
    self.user_id = None
    self.robot_name = robot_name

  def get(self):
    return self.history

  def append(self, value):
    self.history.append(value)

  def relevant_history(self, historical_length):
    return self.history[-historical_length:]

  def reset_history(self):
    self.history = []
    print(self.history)

  # human_name: non-unique tag for human
  # sender: unique id for human, i.e. email address
  def add_message(self, human_name, sender, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.history.append((human_name, sender, message, timestamp))

  # identify new_phrase in gpt output based on existing history
  def find_new_phrase(self, new_phrase, context, human_name):
    # Remove the context
    new_phrase = new_phrase.replace(context, "")
    print(f"new_phrase: {new_phrase}")
    # Split the strings into a list of strings separated by [human] and [robot]
    new_phrases = re.split(f"{self.robot_name}\:|{human_name}\:|{human_name}\;|{self.robot_name}\;", new_phrase)
    new_phrases = filter(lambda x: not (x.isspace() or len(x) == 0), new_phrases)
    new_phrases = list(new_phrases)
    print(f"new_phrases: {new_phrases}")
    print(f"self.history: {self.history}")
    # Loop through the phrases in the new string
    for phrase in new_phrases:
      fixed = phrase.replace(":", "").replace("[n]", " ").strip()
      print(f"fixed {fixed}")
      print(f"{self.robot_name}: {fixed}" not in self.history and f"{human_name}: {fixed}" not in self.history)
      # Check if the phrase exists in the previous string
      if f"{self.robot_name}: {fixed}" not in self.history and f"{human_name}: {fixed}" not in self.history:
        # Return the phrase if it is not in the previous string
        return fixed
    # Return default if no new phrase was found
    return "..."

  def create_tables(self, cursor):
    cursor.execute(
      '''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        human_name TEXT
      )'''
    )
    cursor.execute(
      '''CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        sender TEXT,
        message TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
      )'''
    )
  
  def save_to_database(self, cursor, conn):
    self.create_tables(cursor)
    for human_name, sender, message, timestamp in self.history:
      cursor.execute(
          '''SELECT id FROM users WHERE human_name=?''',
          (human_name,)
      )
      result = cursor.fetchone()
      if result is None:
        cursor.execute(
            '''INSERT INTO users (human_name) VALUES (?)''',
            (human_name,)
        )
        user_id = cursor.lastrowid
      else:
        user_id = result[0]
      cursor.execute(
          '''INSERT INTO user_history (user_id, sender, message, timestamp)
              VALUES (?,?,?,?)''',
          (user_id, sender, message, timestamp)
      )
    conn.commit()
    self.history = []

# Example usage
history = History()
history.add_message('John', 'ChatGPT', 'Hello! How can I help you today?')
history.add_message('John', 'John', 'I have a question about Python.')
history.add_message('John', 'ChatGPT', 'Sure, what do you want to know?')

conn = sqlite3.connect('chat_history.db')
cursor = conn.cursor()
history.save_to_database(cursor, conn)
