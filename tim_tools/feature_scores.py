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
    assert (emb0.shape[0] == emb1.shape[0])
    assert (emb0.shape[1] == emb1.shape[1])
    print(emb0.shape, emb1.shape)
    dot = np.sum(np.multiply(emb0, emb1), axis=1)
    norm = np.linalg.norm(emb0, axis=1) * np.linalg.norm(emb1, axis=1)
    sim = np.clip(dot / norm, -1., 1.)
    return sim


@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--outpath', 'outpathname', required=True)
@click.option('--count', 'comp_count', default=100)
@click.option('--all_impostors', 'all_imps', default=False)
def generate_match(ctx: click.Context, pathname: str, comp_count: int, all_imps: bool, outpathname: str):
    identities = os.listdir(pathname)

    genuine_file = open(os.path.join(outpathname, "genuine.txt"), "w")
    impostor_file = open(os.path.join(outpathname, "impostor.txt"), "w")

    for identity in tqdm(identities):
        id_path = pathname + "/" + identity
        if not os.path.exists(id_path):
            continue
        features = [np.load(x) for x in [id_path + "/" + y for y in os.listdir(id_path) if ".npy" in y]]

        # genuine score
        if len(features) < 2:
            continue
        elif len(features) < 3:
            ref_mul = 1
            gen_score = similarity(features[0], features[1])
        else:
            ref_mul = 2
            probe_count = len(features) - 2
            references = np.vstack(([features[0]] * probe_count, [features[1]] * probe_count))
            probes = np.vstack((features[2:] * 2))
            gen_score = similarity(references, probes)
        genuine_file.write(str(gen_score))
        genuine_file.write('\n')

        # impostor score
        if all_imps:
            impostors = identities
        else:
            impostors = np.random.choice(list(range(0, int(identity))) + list(range(int(identity), 10572)), size=comp_count)
        references = []
        probes = []
        for impostor in impostors:
            impostor_path = pathname + "/" + str(impostor)
            impostor_features = [np.load(x) for x in [id_path + "/" + y for y in os.listdir(impostor_path) if ".npy" in y]]
            if len(impostor_features) < 2:
                continue
            elif len(impostor_features) < 3:
                references.extend(features[:ref_mul])
                probes.extend([impostor_features[1]] * ref_mul)
            else:
                probe_count = len(impostor_features) - 2
                if ref_mul == 1:
                    references.extend([features[0]] * probe_count)
                else:
                    references.extend([features[0]] * probe_count + [features[1]] * probe_count)
                probes.extend(impostor_features[2:] * ref_mul)
        imp_score = similarity(np.vstack(references), np.vstack(probes))
        impostor_file.write(str(imp_score))
        impostor_file.write('\n')

    impostor_file.close()
    genuine_file.close()

if __name__ == "__main__":
    generate_match()
