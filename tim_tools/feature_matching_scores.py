import os
import itertools
import click
import numpy as np
import random
from scipy import spatial
from tqdm import tqdm

@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--count', 'comp_count', default=10)
def generate_match(pathname: str, comp_count: int):
    identities = os.listdir(pathname)
    with open("genuine.txt", "w") as file:
        for identity in tqdm(identities):
            id_path = pathname + "/" + identity
            if not os.path.exists(id_path):
                continue
            features = [np.load(x) for x in os.listdir(id_path)]
            combinations = random.sample(list(itertools.combinations([i for i in range(len(features))], 2)), comp_count)
            for c1, c2 in combinations:
                sim = 1 - spatial.distance.cosine(features[c1], features[c2])
                file.write(sim)
                file.write('\n')
        file.close()
    with open("impostor.txt", "w") as file:
        for identity in tqdm(identities):
            id_path = pathname + "/" + identity
            if not os.path.exists(id_path):
                continue
            features = random.sample([np.load(x) for x in os.listdir(id_path)], comp_count)
            impostors = np.random.randint(low=0, high=len(identities), size=comp_count)
            for feature, impostor in zip(features, impostors):
                if identity == identities[impostor]:
                    continue
                imp_feature = np.load(os.listdir(pathname + "/" + identities[impostor])[0])
                sim = 1 - spatial.distance.cosine(feature, imp_feature)
                file.write(sim)
                file.write('\n')
        file.close()


if __name__ == "__main__":
    generate_match()