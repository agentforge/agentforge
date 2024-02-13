### A Resource that is used in the world generation and simulation
class Resource:
    def __init__(self, name, value, req_per_pop=1, gather_per_pop=1, tradeable=False, consumable=False):
        self.name = name
        self.value = value
        self.req_per_pop = req_per_pop
        self.gather_per_pop = gather_per_pop
        self.tradeable = tradeable
        self.consumable = consumable

    def val(self):
        return round(self.value,2)

    ### Returns inventory and economics information about resource
    def inventory(self, population):
        return {
            "supply": self.value,
            "demand": self.req_per_pop * population,
            "surplus": self.value - (self.req_per_pop * population),
            "deficit": (self.req_per_pop * population) - self.value,
            "happiness": min(1.25, round(self.value / (self.req_per_pop * population),2)) # relative to demand
        }

    def determine_trade_value(self, good, population1, population2):
        """
        Determines the relative worth of two goods to one another for trade between two actors.

        Args:
        - good1, good2: Instances of Good, representing the two goods to be traded.
        - population1, population2: The populations of the two actors/entities.

        Returns:
        - A tuple containing the exchange rate from good1 to good2, and vice versa.
        """
        inventory1 = self.inventory(population1)
        inventory2 = good.inventory(population2)

        # Calculate the perceived value of each good based on its surplus or deficit
        perceived_value1 = (inventory1['surplus'] if inventory1['surplus'] > 0 else -inventory1['deficit'])
        perceived_value2 = (inventory2['surplus'] if inventory2['surplus'] > 0 else -inventory2['deficit'])

        # Avoid division by zero and ensure there's a meaningful exchange rate
        if perceived_value2 == 0 or perceived_value1 == 0:
            return (0, 0)  # No trade can occur if one good has no perceived value

        # Calculate the exchange rate based on the ratio of perceived values
        exchange_rate_good1_to_good2 = abs(perceived_value1 / perceived_value2)
        exchange_rate_good2_to_good1 = abs(perceived_value2 / perceived_value1)

        return exchange_rate_good1_to_good2, exchange_rate_good2_to_good1


    def __str__(self):
        return f"{self.name}: {self.val()}"
    
    def __iadd__(self, other):
        # Check if 'other' is an instance of Resource or a numeric type
        if isinstance(other, Resource):
            # Assuming you only want to add the 'value' of two Resources if they have the same name
            if self.name == other.name:
                self.value += other.value
            else:
                raise ValueError("Cannot add resources with different names")
        elif isinstance(other, (int, float)):
            self.value += other
        else:
            raise TypeError(f"Unsupported type for += operation: {type(other)}")
        return self
    
    def __isub__(self, other):
        if isinstance(other, Resource):
            if self.name == other.name:
                self.value -= other.value
            else:
                raise ValueError("Cannot subtract resources with different names")
        elif isinstance(other, (int, float)):
            self.value -= other
        else:
            raise TypeError(f"Unsupported type for -= operation: {type(other)}")
        return self