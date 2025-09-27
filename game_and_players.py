import random
from input_utils import input_yesno

# Hanterar omgångar av spelet och resultat
class Match:
    player1_wins = 0
    player2_wins = 0
    total_ties = 0
    total_games_played = 0
    # Antal omgångar per match så att alla spelare spelar lika många omgångar i highscore-listan
    max_games_per_match = 5

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play_game(self):       
        game = Game(self.player1, self.player2)
        game.play()
        self.total_games_played += 1
        if game.is_tie():
            print(f"\nSpelet är oavgjort!")
            self.total_ties += 1
        elif game.player1_won():
            print(f"\n{self.player1.name} har vunnit omgången!")
            self.player1_wins += 1
        else:
            print(f"\n{self.player2.name} har vunnit omgången!")
            self.player2_wins += 1
    
    def can_play_again(self):
        return self.total_games_played < self.max_games_per_match

    def get_score_points(self):
        return self.player1_wins * 10 + self.total_ties * 5
    
    def show_score(self):
        print(f"Ställningen är: {self.player1.name} {self.player1_wins} - {self.player2.name} {self.player2_wins}.")
        if self.total_ties > 0:
            print(f"Oavgjorda spel: {self.total_ties}")
    
    def show_final_score(self):
        print(f"\nSlutresultat för matchen:\n{self.player1.name} - {self.player1_wins} vinster\n{self.player2.name} - {self.player2_wins} vinster\nOavgjort: {self.total_ties} av totalt {self.total_games_played} spelade omgångar.")

# Startar en omgång av spelet       
class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def player_turn(self, player):
        points = 0
        print(f"\nNu spelar {player.name}")
        # Fortsätter spela så länge som spelaren vill
        while True:
            roll = random.randint(1, 6)
            points += roll
            print(f"{player.name} slog {roll} och har {points} poäng!")
            # Avgör om player har förlorat eller har nått blackjack(21)
            if points > 21:
                return -1       #Player som går över 21poäng får värdet -1 för att bestämma om player 2 behöver spela
            elif points == 21:
                print("Blackjack!")
                break
            # Om spelaren inte är 'tjock' eller har uppnått 21 poäng, fortsätt spela
            if not player.will_roll(points):
                break
        return points
    
    def play(self):
        # Player 1 spelar först
        self.player1_points = self.player_turn(self.player1)
        # Player 2 spelar endast on player 1 inte redan har förlorat (fått värde -1)
        if self.player1_points >= 0:
            self.player2_points = self.player_turn(self.player2)
        else:
        # Sätter player 2 värde till 0 - de har inte spelat men har vunnit spelet
            self.player2_points = 0

    def is_tie(self):
        # Returnerar True om omgången är oavgjord
        return self.player1_points == self.player2_points

    def player1_won(self):
        # Returnerar True om player1 har vunnit
        return self.player1_points > self.player2_points

    def player2_won(self):
        # Returnerar True om player2 har vunnit. (i detta programmet är det bara huset som gäller, men kod kan användas för att lägga till fler players)
        return self.player1_points < self.player2_points


class Player:
    def __init__(self, name):
        self.name = name

class Human(Player):
    def will_roll(self, current_points):
        return input_yesno("Vill du slå tärningen eller stanna? (j/n): ")

class House(Player):
    def __init__(self):
        Player.__init__(self, "Huset")

    def will_roll(self, current_points):
        return current_points < 17
