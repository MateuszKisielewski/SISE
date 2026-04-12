with open('wyniki2.csv', encoding='utf-16') as f:
    content = f.read()

with open('wyniki2.csv', 'w', encoding='utf-8') as f:
    f.write(content)