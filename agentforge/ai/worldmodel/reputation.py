class ReputationManager:
    def __init__(self, reputation_scores={}):
        """Initialize the reputation scores dictionary."""
        self.reputation_scores = reputation_scores

    def serialize(self):
        """Serialize the reputation scores dictionary."""
        return self.reputation_scores

    @classmethod
    def deserialize(cls, data):
        """Deserialize the reputation scores dictionary."""
        return cls(data)

    def update_reputation(self, society_name, event, impact):
        """Update the reputation score based on an event.
        
        Args:
            society_name (str): The name of the other society.
            event (str): The type of event (e.g., 'war', 'trade', 'festival').
            impact (float): The impact on reputation (-1.0 to 1.0).
        """
        if society_name not in self.reputation_scores:
            self.reputation_scores[society_name] = 0  # Initialize with neutral reputation

        # Update the reputation score within bounds [-1, 1]
        self.reputation_scores[society_name] = min(max(self.reputation_scores[society_name] + impact, -1), 1)

    def get_reputation(self, society_name):
        """Retrieve the current reputation score with another society.
        
        Args:
            society_name (str): The name of the other society.
        
        Returns:
            float: The reputation score.
        """
        return self.reputation_scores.get(society_name, 0)  # Default to neutral if not found

    def list_all_reputations(self):
        """List all current reputation scores with other societies.
        
        Returns:
            dict: A copy of the reputation scores dictionary.
        """
        return self.reputation_scores.copy()
    

    def tick(self, decay_factor=0.01):
        """
        Adjusts all reputation scores slightly towards zero, simulating the natural decay or improvement over time.
        
        Args:
            decay_factor (float): The rate at which reputations decay towards neutral. Default is 0.01.
        """
        for society, score in self.reputation_scores.items():
            if score > 0:
                self.reputation_scores[society] = max(score - decay_factor, 0)
            elif score < 0:
                self.reputation_scores[society] = min(score + decay_factor, 0)

# # Example usage
# reputation_manager = ReputationManager()
# reputation_manager.update_reputation('SocietyB', 'trade', 0.2)
# reputation_manager.update_reputation('SocietyC', 'war', -0.5)
# print(reputation_manager.get_reputation('SocietyB'))  # Expected output: 0.2
# print(reputation_manager.list_all_reputations())  # Expected output: {'SocietyB': 0.2, 'SocietyC': -0.5}
