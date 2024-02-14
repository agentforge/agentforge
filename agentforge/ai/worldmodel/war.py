class War:
    def __init__(self):
        """
        Initializes the war tracker for a society.
        
        Args:
            society (SocioPoliticalFramework): The society for which to track war weariness.
        """
        self.war_weariness = 0  # Initial war weariness

    def update_weariness(self, event_impact, factors, wealth):
        """
        Updates the war weariness based on a war event's impact, considering societal factors.
        
        Args:
            event_impact (float): The base impact of the war event on weariness.
        """
        # Calculate dampening effect based on societal factors
        dampening_factors = self.calculate_dampening(factors, wealth)
        # Update war weariness, ensuring it doesn't decrease (negative weariness doesn't make sense)
        print(f"event_impact: {event_impact}, dampening_factors: {dampening_factors}")
        self.war_weariness += max(event_impact * (1 - dampening_factors), 0)
        print(f"war_weariness: {self.war_weariness}")

    # factors: (dict) sociopolitical.dimension_values
    # wealth: (float) wealth
    def calculate_dampening(self, factors, wealth):
        """
        Calculates the dampening effect on war weariness increase based on societal factors.
        
        Returns:
            float: The dampening effect as a decimal between 0 and 1.
        """
        # Example calculation (simplified for demonstration purposes)
        dampening = (
            factors['Militaristic'] +
            factors['Technological Integration'] +
            factors['Compulsory Military Service'] +
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
    
    def calculate_war_probabilities(self, us, society):
        # Less militaristic societies only engage in wars of necessity
        if us.sociopolitical.get_dimension_value("Militaristic") < 0.25:
            return 0

        return us.sociopolitical.calculate_war_potential(
            society.sociopolitical,
            us.wealth(),
            us.war_manager.get_weariness(),
            society.wealth(),
            society.war_manager.get_weariness()
        )
    
    def calculate_war_impact(self, victor, relative_war_power):
        """
        Calculates the war impact based on the victor's dimensions and relative war power.
        
        Args:
            victor (SocioPoliticalFramework): The victorious society.
            relative_war_power (float): The relative power of the victor compared to the opponent.
            
        Returns:
            float: The impact of the war, considering weariness and casualties.
        """
        # Extract dimensions for easier access
        if victor is None:
            return 0.0

        dimensions = victor.sociopolitical.dimension_values
        cultural_dimensions = victor.culture.dimension_values

        # Base impact calculation
        base_impact = dimensions['Militaristic'] + dimensions['Technological Integration'] * 0.8 \
                      + dimensions['Compulsory Military Service'] * 0.5 - dimensions['Diplomatic'] * 0.5 \
                      + dimensions['Nationalism'] * 0.7 + dimensions['Security'] * 0.3 \
                      + cultural_dimensions['Zealotry'] * 0.6 - cultural_dimensions['Diversity'] * 0.4 \
                      - dimensions['Isolationism'] * 0.4 + dimensions['Innovation and Research'] * 0.9
        
        # Adjust base impact by relative war power
        adjusted_impact = base_impact * relative_war_power
        
        # Normalize impact to a scale of 0 to 1 for consistency
        normalized_impact = min(max(adjusted_impact / 10, 0), 1)
        
        # Consider societal resilience and adaptability
        resilience_factors = dimensions['Social Welfare'] + dimensions['Public Commons'] + dimensions['Global Solidarity']
        adaptability = dimensions['Innovation and Research'] + dimensions['Technological Integration']
        
        # Final impact considering resilience and adaptability
        final_impact = normalized_impact * (1 - resilience_factors / 3 * 0.2) * (1 + adaptability / 2 * 0.1)
        
        return final_impact