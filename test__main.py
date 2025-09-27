#Pytest
import pytest
from highscores import HighScores
from input_utils import input_yesno
from unittest.mock import patch, mock_open, call

# Mockar testerna som gäller filhantering och input för att jag vill testa funktionen med kontrollbar data utan externa beroenden
# Jag har valt att testa filfunktionen då den är viktig för highscore delen
# Jag har valt att testa input funktionen för det gäller interaktion med användaren
# Definitivt kan fler tester göras/borde göras, för att täcka in allt

# Testet nedan kontrollerar tre saker: 
# Att klassen HighScore kan öppna och läsa från en fil (mock fil så att vi inte behöver vara beroende av riktig fil)
# Det betyder att jag kan testa logiken i HighScores istället för att testa filsystemet
# Att innehållet kan tolkas korrekt (tuples) och att resultatet sorteras korrekt (högsta poäng först)

# Testar att en fil kan läsas och sorteras genom att anropa klassen för filen
def test_HighScores_class_open_read_and_sort_file_success(): 
    # Simulerar filinnehåll med personer och poäng osorterat
    mock_data = "Person1\t100\nPerson2\t300\n"
    # Mockar öppning och läsning av filen genom att skapa ett HighScore-objekt med ett filnamn
    with patch("builtins.open", mock_open(read_data = mock_data)):
        hs = HighScores("test_highscores.txt")

    # Kontrollerar att filnamnet har sparats korrekt
    assert hs.filename == "test_highscores.txt"
    # Kontrollerar att poäng och personer har tolkats och sorterats korrekt
    assert hs.scores == [("Person2",300),("Person1",100)]

# Testet nedan säkerhetsställer att HighScore klassen kan hantera om filen inte finns, inte krasha
# Testet mockar öppning av filen så att vi kan få ett specifikt fel, vi simulerar att filen inte finns
# Vi instansierar klassen med filnamnet och objekt ska skapas även om vi får det specifika felet
# Vi kontrollerar sen att filnamnet ändå sparas även om det inte gick att läsa filen

# Testar att när fil inte hittas så returneras en tom lista (så att programmet kan fortsätta)
def test_HighScore_class_when_file_not_found():
    # Mockar öppning av filen och triggar ett FileNotFoundError specifikt. Testen säkerhetsställer att det är ok att filen inte finns från början.
    with patch("builtins.open", side_effects = FileNotFoundError):
        # Skapar ett HighScore-objekt som försöker öppna filen
        hs = HighScores("test_highscores.txt")

    # Förväntas att filnamnet har sparats
    assert hs.filename == "test_highscores.txt"
    # Förväntas en tom lista tillbaka om fil inte finns
    assert hs.scores == []

# Testet nedan kontrollerar att ny person och poäng kan läggas till highscore-listan

def test_add_score_to_highscore_list():
    # Simulerar filinnehåll med personer och poäng osorterat
    mock_data = "Person1\t100\nPerson2\t300\n"
    mock = mock_open(read_data = mock_data)

    with patch("builtins.open", mock):
        # Skapar ett HighScore-objekt som laddar in den fejkade datan
        hs = HighScores("test_highscores.txt")
        # Försöker lägga till en ny spelare
        result =hs.add_score("Person3", 200)

    # Kontrollerar att filen öppnats både för läsning och skrivning
    # HighScores måste först läsa befintlig poäng och sen skriva tillbaka i listan med nya poängen
    mock.assert_has_calls([call("test_highscores.txt", "r", encoding="utf-8"), call("test_highscores.txt", "w", encoding="utf-8")],any_order=True)
    # Result blir True om player får highscore
    assert result == True
    # Kontrollera fejkat data uppdateras i filen (i rätt ordning)
    assert hs.scores == [("Person2",300),("Person3",200),("Person1",100)]

# Testet nedan kontrollerar att ny poäng inte läggs till i Highscore-listan om inte bland de (just nu) 5 topp
# Existerande lista av highscore kommer inte att påverkas av poäng som är lägre än i listan

# Observera att ändring av max_highscores kommer att invalidera detta test
def test_add_score_does_not_add_to_highscore_list_when_not_top5():
    # Simulerar filinnehåll med personer och poäng
    mock_data = "Person1\t100\nPerson2\t300\nPerson3\t150\nPerson4\t250\nPerson5\t75\n"
    mock = mock_open(read_data = mock_data)
    with patch("builtins.open", mock):
        hs = HighScores("test_highscores.txt")
        # Lägger till poäng som fåtts till listan 
        result = hs.add_score("Person6", 50)

    # Ser till att anropet görs en gång eftersom listan inte ska uppdatera och spara till fil
    mock.assert_called_once_with("test_highscores.txt", "r", encoding="utf-8")
    # Förväntat resultat är false eftersom nytt matchresultat inte har uppnått nytt highscore
    assert result == False
    assert hs.scores == [("Person2",300),("Person4",250),("Person3",150),("Person1",100),("Person5",75)]

 #Test nedan kontrollerear att ny highscore-poäng kan läggas till om högre än i highscore-listans top-poäng 

# Observera att ändring av max_highscores kommer att invalidera detta test
def test_add_score_adds_new_highscore_when_new_top5():
    #Simulerar filinnehåll med personer och poäng
    mock_data = "Person1\t100\nPerson2\t300\nPerson3\t150\nPerson4\t250\nPerson5\t75\n"
    mock = mock_open(read_data = mock_data)
    with patch("builtins.open", mock):
        hs = HighScores("test_highscores.txt")
        # Lägger till poäng som fåtts till listan 
        result = hs.add_score("Person6", 200)

    # Mock_anropar läsning av filen och sen sparning av filen
    mock.assert_has_calls([call("test_highscores.txt", "r", encoding="utf-8"), call("test_highscores.txt", "w", encoding="utf-8")],any_order=True)
    # Making sure the call is called once since list should not update and not be saved to a file
    assert result == True
    assert hs.scores == [("Person2",300),("Person4",250),("Person6",200),("Person3",150),("Person1",100)]

# Detta test kontrollerar att funktionen input_yesno() fungerar korrekt när användaren svarar 'ja'/'j' på en fråga
# Viktig funktion att testa då den används i interaktionen med användaren
# Viktigt att olika variationer av svaret hanteras konsekvent
# Testet hanterar att olika input av användaren kan hanteras (mellanslag, indentering, stora/små bokstäver)

def test_input_yesno_yes():
    # Testar att du får förväntat resultat när du skriver ja eller j. Viktig interaktions del av programmet, därav test
    with patch("builtins.input", return_value = "j"):   
        result1 = input_yesno("hello")
    # Testar att strip och lower fungerar för funktionen        
    with patch("builtins.input", return_value = " JA"): 
        result2 = input_yesno("hello")

    # Både 'j' och 'ja' ska retunera True
    assert result1 == True
    assert result2 == True

# Detta test kontrollerar att funktionen input_yesno() fungerar korrekt när användaren svarar 'nej'/'n' på en fråga
# Viktigt att olika variationer av svaret hanteras konsekvent
# Testet hanterar att olika input av användaren kan hanteras (mellanslag, indentering, stora/små bokstäver)

def test_input_yesno_no():
    # Testar att du får förväntat resultat (False) när du skriver nej eller n. Viktig interaktions del av programmet, därav test
    with patch("builtins.input", return_value = "n"):
        result1 = input_yesno("hello")
    # Testar att strip och lower fungerar för funktionen
    with patch("builtins.input", return_value = " NeJ"):
        result2 = input_yesno("hello")

    # Både 'n' och 'nej' ska returnera False
    assert result1 == False
    assert result2 == False

# Detta test kontrollerar att funktionen input_yesno() inte avslutas förrän användaren skriver ett giltigt svar och
# att funktionen avslutas när giltigt svar inkommer ('y' efter 'j' ignoreras i nedan fall)

def test_input_yesno_other():
    # Testar att funktionen endast avslutas när förväntat värde skrivs in, ja/j (eller nej/n)
    with patch("builtins.input", side_effect = [ "q", "x", "j", "y" ]) as mock_input:
        result = input_yesno("hello")

    # Testar att funktionen anropas så många gånger som vi ger input till
    assert mock_input.call_count == 3
    assert result == True

