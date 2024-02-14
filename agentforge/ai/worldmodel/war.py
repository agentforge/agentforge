class War:
    def __init__(self, society):
        """
        Initializes the war tracker for a society.
        
        Args:
            society (SocioPoliticalFramework): The society for which to track war weariness.
        """
        self.society = society
        self.war_weariness = 0  # Initial war weariness

    def update_weariness(self, event_impact):
        """
        Updates the war weariness based on a war event's impact, considering societal factors.
        
        Args:
            event_impact (float): The base impact of the war event on weariness.
        """
        # Calculate dampening effect based on societal factors
        dampening_factors = self.calculate_dampening()
        # Update war weariness, ensuring it doesn't decrease (negative weariness doesn't make sense)
        self.war_weariness += max(event_impact * (1 - dampening_factors), 0)

    def calculate_dampening(self):
        """
        Calculates the dampening effect on war weariness increase based on societal factors.
        
        Returns:
            float: The dampening effect as a decimal between 0 and 1.
        """
        factors = self.society.dimensions
        # Example calculation (simplified for demonstration purposes)
        dampening = (
            factors['Militaristic'] +
            factors['Technological Integration'] +
            factors['Compulsory Military Service'] +
            self.society.wealth() +  # Assuming wealth is normalized between 0 and 1
            factors['Nationalism'] +
            factors['Security']
        ) / 6  # Average the contributions of the factors
        return min(dampening, 1)  # Ensure dampening does not exceed 1

    def tick(self):
        """
        Simulates the passage of time, decreasing war weariness to model recovery.
        """
        # Decrease weariness over time, with a minimum of 0
        self.war_weariness = max(self.war_weariness - 0.01, 0)  # Example decrement

    def get_weariness(self):
        """
        Returns the current war weariness of the society.
        
        Returns:
            float: The current war weariness.
        """
        return self.war_weariness