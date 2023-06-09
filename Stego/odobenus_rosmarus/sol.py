s = "Ce soir je Célèbre Le Concert Electro Comme Louis Et Lou. Comme La nuit Commence Et Continue Clairement, Et Clignote Lascivement il Chasse sans Chausser En Clapant Encore Classiquement Les Cerclages du Clergé. Encore Car Encore, Louis Lou Entamant Longuement La Lullabile En Commençant Le Cercle Exhaltant de Club Comique Cannais Et Clermontois."

# Extract uppercase letters (and dots)
out = ""
for c in s:
    if c.isupper() or c == '.':
        out += c
print(out)

# CCLCECLEL.CLCECCECLCCECECLCC.ECELLELLLECLCECCCEC.
# This is Morse: C for 'Court' (short), L for Long
morse = out
morse = morse.replace('.', '/')
morse = morse.replace('C', '.')
morse = morse.replace('L', '-')
morse = morse.replace('E', ' ')
print(morse)

# ..-. .- -/.-. .. .-.. . .-../ . -- --- .-. ... ./
# Decode it with dcode: FACILELEMORSE
