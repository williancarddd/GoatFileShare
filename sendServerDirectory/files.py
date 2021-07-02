import os

caminhoImagens = []
for x, y, z in os.walk('.'):
    for k in z:
        if k.split('.')[-1] == 'png':
            caminhoImagens.append(os.path.join(x, k))

for x in caminhoImagens:
    print(x)


