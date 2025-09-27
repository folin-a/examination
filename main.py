
from input_utils import input_yesno
from highscores import HighScores
from game_and_players import Match, Human, House 

# Visar meny för användaren
def show_menu():
    print("\n---Menyalternativ för Blackjack---")
    print("1) Starta spelet")
    print("2) Visa highscore-lista")        
    print("3) Avsluta spelet") 

# Visar instruktioner till BlackJack för användaren när en ny match startar
def show_instructions():
    print("\nVälkommen till Blackjack-spelet! Instruktioner följer nedan.")
    print("----------------------------------------")
    print("- Du spelar mot huset/datorn, 21 poäng är högsta möjliga poäng. Du förlorar omgången om du får mer än 21 poäng.")
    print(f"- Efter någon vunnit/förlorat omgången väljer du om du vill fortsätta med en ny omgång. Max omgångar är satt till {Match.max_games_per_match}.")
    print("- Svara 'n' (nej) för att behålla inskaffade poäng, 'j' (ja) för att fortsätta")
    print("- Vinnaren av en omgång får 10 poäng, förloraren 0 poäng och oavgjort 5 poäng.")
    print("- Värde på tärningen är mellan 1-6 vid varje rullning.")
    print("Lycka till!")
    print("----------------------------------------")

def play_match(player):
    match = Match(player, House())

    play_again = True
    while play_again:
        print("\n-- Spelet startar!")
        # Anropar funktionen för att spela spelet 
        match.play_game()
        # Visar resultat per omgång
        match.show_score()
        # Kontrollerar om användaren kan spela fler omgångar mot max-spel
        if not match.can_play_again():
            print("Matchen är avslutad!")
            break
        # Frågar användaren om de vill spela en ny omgång
        play_again = input_yesno(f"Vill du spela igen? (j/n)")

    # Visar matchens slutresultat
    match.show_final_score()
    # Returnerar värdet av resultatet i matchen
    return match       

# Initierar klassen highscore och läser in highscorelistan i minnet
high_score = HighScores("highscores.txt")

while True:
    show_menu()
    meny_val = input("Välj ett menyalternativ, skriv siffran: ").strip()
    if meny_val == "1":
        # Visar instruktionerna för att spela Blackjack
        show_instructions()
        # Ber användaren om namn, rensar tomma tecken och ersätter tab med tomma tecken pga kan ge korrupt Highscore-fil
        name = input("Skriv in ditt namn: ").title().strip().replace("\t", "")
        match = play_match(Human(name))
        # Lägger till highscore från matchen till highscore listan
        score = match.get_score_points()
        print(f"\nDu fick {score} poäng.")
        if high_score.add_score(name, score):
            print(f"Grattis! Du fick ett nytt highscore!")
    elif meny_val =="2":
        # Visar listan med highscore
        high_score.show()
    elif meny_val =="3":
        print("Tack för att du spelade Blackjack!")
        break
    else:
        # För all annan input some inte är del av menyn visas menyn igen och för att jag inte konverterar input till en int. 
        # Därav tycker inte jag en try...except behövs/är nödvändig för denna input, undviker onödig kod.
        print("Du har valt ett felaktigt menyalternativ, vänligen skriv in siffervalet: ")     

