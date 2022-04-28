import numpy as np
import json
from tqdm import tqdm
import os

import click

def similarity(emb0, emb1):
    if emb0.ndim < 2 or emb1.ndim < 2:
        print("ERROR")
        print(emb0, emb1)
        return []
    assert (emb0.shape[0] == emb1.shape[0])
    assert (emb0.shape[1] == emb1.shape[1])
    dot = np.sum(np.multiply(emb0, emb1), axis=1)
    norm = np.linalg.norm(emb0, axis=1) * np.linalg.norm(emb1, axis=1)
    sim = np.clip(dot / norm, -1., 1.)
    return sim


@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--expname', 'expname', required=True)
def generate_match(ctx: click.Context, pathname: str, expname: str):
    with open('/home/trieber/data_cleaning/test.json', 'w') as outfile:
        json.dump({"test": 0}, outfile)

    identities = os.listdir(pathname)
    image_genuine_scores = {}

    for identity in tqdm(identities):
        id_path = os.path.join(pathname, identity)
        if not os.path.exists(id_path):
            print("rip")
            continue
        names = [y[:-4] for y in os.listdir(id_path) if ".npy" in y]
        features = [np.load(id_path + "/" + x) for x in names]

        for name, feature in zip(names, features):
            references = np.vstack(([feature] * len(features)))
            probes = np.vstack(features)
            gen_score = similarity(references, probes)
            image_genuine_scores[str(identity) + "/" + name] = sum(gen_score) / len(gen_score)

    score_sorted = {k: v for k, v in sorted(image_genuine_scores.items(), key=lambda item: item[1])}
    with open('/data/trieber/data_cleaning_scores/' + expname + '.json', 'w') as outfile:
        json.dump(score_sorted, outfile)


if __name__ == "__main__":
    generate_match()