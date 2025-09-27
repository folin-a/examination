#Min uppfattning av Highscore-funktionen är att det finns flera olika spelare som spelar mot dealern efter varandra
#Dealern/huset är alltså inte medräknad i highscore-listan - den består endast av spelare per ny match

class HighScores:
    max_highscores = 5

    def __init__(self, filename):
        self.filename = filename
        self.scores = list()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    entry = line.strip().split('\t')
                    self.scores.append((entry[0], int(entry[1])))
            # Sorterar informationen i filen innan highscore visas - högsta poäng överst
            self.scores.sort(reverse = True, key = lambda entry: entry[1])     
        except ValueError:
            print("Fel vid filläsandet. Highscore-listans data kan vara korrupt")
        except FileNotFoundError:
            print("Filen kunde inte hittas, ny fil skapas automatiskt.")
        except IOError:
            print("Filen kunde inte öppnas.")

    def add_score(self, player, score):
        # Lägger till highscore i listan om poäng är högre än de max 5 highscore på listan.
        if len(self.scores) < self.max_highscores or score > min(entry[1] for entry in self.scores):
            self.scores.append((player, score))
            # Sorterar listan så att mest poäng visas i topp
            self.scores.sort(reverse = True, key = lambda entry: entry[1])
            # Tar bort de highscore poäng som inte längre är top för max antal highscores.
            del self.scores[self.max_highscores:]                        
            self.save(self.filename)
            # Returnerar true om nytt highscore har nåtts och ska sparas
            return True
        # Returnerar false om ingen nytt highscore har uppnåtts
        return False

    def save(self, filename):
        try:
            # Öppna en fil för att skriva till
            with open(filename, "w", encoding="utf-8") as file:
                #Konverterar varje rad i highscore-listan till en (formaterad) rad vi kan skriva till filen
                file.writelines(map(lambda entry: f"{entry[0]}\t{entry[1]}\n", self.scores))
        except IOError:
            print("Highscore-filen kunde inte sparas.")

    def show(self):
        print("\n-----Hall of fame-----")
        #Numrerar informationen för highscore innan vi skriver ut listan för användaren. Formaterar så det ser bra ut för användaren.
        for index, entry in enumerate(self.scores):                      
            print(f"{index +1}. {entry[0]}{(15-len(entry[0]))*" "} {entry[1]} poäng")
