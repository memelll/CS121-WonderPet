import time

from GameFunctions import display_message


class VirtualPet:
    def __init__(self):
        self.hunger = 100
        self.cleanliness = 100
        self.happiness = 100
        self.thirst = 100
        self.energy = 100
        self.level = 1
        self.exp = 0
        self.exp_bar = 200
        self.coins = 0
        self.exp_counter = 0
        self.last_hunger_decrease = time.time()
        self.last_cleanliness_decrease = time.time()
        self.last_happiness_decrease = time.time()
        self.last_thirst_decrease = time.time()
        self.last_energy_decrease = time.time()

    def feed(self):
        if self.hunger < 100:
            self.hunger = min(100, self.hunger + 2)
            self.update_level()
            self.update_exp(2)
            self.update_exp_counter(2)

    def bath(self):
        if self.cleanliness < 100:
            self.cleanliness = min(100, self.cleanliness + 2)
            self.update_level()
            self.update_exp(2)
            self.update_exp_counter(2)
            display_message(f"You cleaned your pet.")
        else:
            display_message(f"Stats already at maximum!")

    def play(self):
        if self.happiness < 100:
            self.happiness = min(100, self.happiness + 2)
            self.update_level()
            self.update_exp(2)
            self.update_exp_counter(2)
            display_message(f"You played with your pet.")
        else:
            display_message(f"Stats already at maximum!")

    def hydrate(self):
        if self.thirst < 100:
            self.thirst = min(100, self.thirst + 2)
            self.update_level()
            self.update_exp(2)
            self.update_exp_counter(2)

    def rest(self):
        if self.energy < 100:
            self.energy = min(100, self.energy + 2)
            self.update_level()
            self.update_exp(2)
            self.update_exp_counter(2)
            display_message(f"You let your pet rest.")
        else:
            display_message(f"Stats already at maximum!")

    def update_exp_counter(self, exp):
        self.exp_counter += exp
        if self.exp_counter >= 2:
            self.earn_coins()
            self.exp_counter = 0

    def earn_coins(self):
        self.coins += 2

    def update_stats(self):
        current_time = time.time()

        if current_time - self.last_hunger_decrease >= 8.5:
            self.hunger = max(0, self.hunger - 2)
            self.last_hunger_decrease = current_time

        if current_time - self.last_cleanliness_decrease >= 4:
            self.cleanliness = max(0, self.cleanliness - 2)
            self.last_cleanliness_decrease = current_time

        if current_time - self.last_happiness_decrease >= 5.5:
            self.happiness = max(0, self.happiness - 2)
            self.last_happiness_decrease = current_time

        if current_time - self.last_thirst_decrease >= 10:
            self.thirst = max(0, self.thirst - 2)
            self.last_thirst_decrease = current_time

        if current_time - self.last_energy_decrease >= 7:
            self.energy = max(0, self.energy - 2)
            self.last_energy_decrease = current_time

    def update_level(self):
        total = self.hunger + self.cleanliness + self.happiness + self.thirst + self.energy
        gained_exp = total // 5

        while gained_exp >= self.exp_bar:
            self.level += 1
            gained_exp -= self.exp_bar
            self.exp_bar += 200

    def update_exp(self, exp):
        self.exp += exp
        while self.exp >= self.exp_bar:
            self.level += 1
            self.exp -= self.exp_bar
            self.exp_bar += 200


pet = VirtualPet()