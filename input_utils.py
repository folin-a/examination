# Interaktion med användaren. Funktionen accepterar endast ja/j eller nej/n.
# Stora bokstäver och tab och mellanslag hanteras av funktionen.
# Alla andra svar accepteras inte utan anses inkorrekta
def input_yesno(message):
  answer = input(message).strip().lower()
  while answer != 'n' and answer != 'j' and answer != 'nej' and answer != 'ja':
    answer = input("Inkorrekt val. Vänligen skriv in ja eller nej (j/n)")
  return answer == 'j' or answer == 'ja'
