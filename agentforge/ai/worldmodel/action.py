class ActionHistoryManager:
    def __init__(self):
        self.action_histories = {}

    def add(self, action, reward, year, season, effect):
        if action not in self.action_histories:
            self.action_histories[action] = ActionHistory()
        self.action_histories[action].add(reward, year, season, effect)

# Stores actions and rewards for a society -- use for introspection and debugging
class ActionHistory:
    def __init__(self):
        self.rewards = []
        self.years = []
        self.seasons = []
        self.effects = []

    def add(self, reward, year, season, effect):
        # Use list form for easy windowed indexing lookup/summation
        self.rewards.append(reward)
        self.years.append(year)
        self.seasons.append(season)
        self.effects.append(effect)

    def get(self, index):
        if index < 0 or index >= len(self.rewards): # validation
            return None
        return {
            "reward": self.rewards[index],
            "year": self.years[index],
            "season": self.seasons[index],
            "effect": self.effects[index]
        }

    def get_window(self, past_n_actions):
        if past_n_actions < 0:
            return None
        return {
            "rewards": self.rewards[-past_n_actions:],
            "years": self.years[-past_n_actions:],
            "seasons": self.seasons[-past_n_actions:],
            "effects": self.effects[-past_n_actions:]
        }
    
    def get_windowed_sum(self, past_n_actions):
        if past_n_actions < 0:
            return None
        return {
            "reward": sum(self.rewards[-past_n_actions:]),
        }

    def get_stats(self):
        return {
            "sum": sum(self.rewards),
            "count": len(self.rewards),
            "mean": sum(self.rewards) / len(self.rewards),
            "max": max(self.rewards),
            "min": min(self.rewards)
        }
