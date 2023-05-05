import random
import string
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

with open('names.txt', 'r') as f:
    names = f.read().splitlines()


bgrm_count = {}

for name in names:
    name = '^' + name.lower() + '$'
    for i in range(len(name)- 1):
        bgrm = name[i:i+2]

        if bgrm in bgrm_count:
            bgrm_count[bgrm] += 1

        else:
            bgrm_count[bgrm] =1


total_bgrms = sum(bgrm_count.values())
bgrm_probs = {bgrm: count/total_bgrms for bgrm, count in bgrm_count.items()}


class Generator_Name(nn.Module):
    def __init__(self, bgrm_probs):
        super(Generator_Name, self).__init__()
        self.bgrm_probs = bgrm_probs
        self.first_choice= list(set([bgrm[0] for bgrm in self.bgrm_probs.keys()]))
        
    def forward(self):
        name = random.choice(self.first_choice) 

        while name[-1] != '$':
            possible_bgrms = [bgrm for bgrm in self.bgrm_probs.keys() if bgrm.startswith(name[-1])]
            bgrm_probs = [self.bgrm_probs[bgrm] for bgrm in possible_bgrms]
            new_bgrm = random.choices(possible_bgrms, weights=bgrm_probs)[0]
            name += new_bgrm[1]
        return name[1:-1].capitalize()
        
 
generate_name = Generator_Name(bgrm_probs)
new_name = ''

while len(new_name) < 3:
    generate_name = Generator_Name(bgrm_probs)
    new_name = generate_name()
print(new_name)


bigrams = list(bgrm_probs.keys())
probabilities = list(bgrm_probs.values())

plt.figure(figsize=(17, 7))
plt.bar(bigrams,probabilities)
plt.title('Вероятность Биграмм')
plt.xlabel('Биграммы')
plt.ylabel('Вероятности')
plt.show()