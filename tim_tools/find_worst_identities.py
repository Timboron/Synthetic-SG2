import os
import itertools
import click
import numpy as np
import random
from scipy import spatial
from tqdm import tqdm
from numpy import dot
from numpy.linalg import norm


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
def generate_match(ctx: click.Context, pathname: str):
    identities = os.listdir(pathname)

    genuine_scores = {}

    for identity in tqdm(identities):
        id_path = pathname + "/" + identity
        if not os.path.exists(id_path):
            continue
        features = [np.load(x) for x in [id_path + "/" + y for y in os.listdir(id_path) if ".npy" in y]]

        # genuine score
        if len(features) < 2:
            continue
        elif len(features) < 3:
            gen_score = similarity(features[0], features[1])
        else:
            probe_count = len(features) - 2
            references = np.vstack(([features[0]] * probe_count, [features[1]] * probe_count))
            probes = np.vstack((features[2:] * 2))
            gen_score = similarity(references, probes)
        genuine_scores[identity] = gen_score.mean()

    score_sorted = {k: v for k, v in sorted(genuine_scores.items(), key=lambda item: item[1])}
    print(score_sorted)

if __name__ == "__main__":
    generate_match()
