from ontology import kitchenware, food
print('ontology initialised')
import numpy as np
# from random import sample

np.random.seed(42)
# np.random.default_rng(42)

def set_sample(s, size):
    return set(np.random.choice(list(s), size, replace=False))

question = 'lorem ipsum'
answers = set_sample(food, 3)

answer = set_sample(food, 1)
n_nanswers = answers.difference(answer)
answer = answer.pop()
noise = set_sample(kitchenware, 2)
noise_onto = set_sample(food.difference(answers), 4)

print('question')
print(question)
print('answers')
print(answers)
print(f'selected object {answer=}, {answer.name=}')
print(f'dropped objects {n_nanswers}')

print('randomly added noise objects')
print(noise_onto)
print(noise)

all_objects = list({answer}.union(noise).union(noise_onto))
names = [o.name for o in all_objects]  # todo: different name variants: glass of milk, pack of milk, etc
np.random.shuffle(names)
print(names)

base_prompt = 'A kitchen scene with'
objects_prompt = ', '.join(names)

final_prompt = f'{base_prompt}: {objects_prompt}'

print(final_prompt)
