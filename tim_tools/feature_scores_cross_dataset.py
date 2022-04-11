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
    dot = np.sum(np.multiply(emb0, emb1), axis=1)
    norm = np.linalg.norm(emb0, axis=1) * np.linalg.norm(emb1, axis=1)
    sim = np.clip(dot / norm, -1., 1.)
    return sim


@click.command()
@click.pass_context
@click.option('--refpath', 'refpathname', required=True)
@click.option('--probepath', 'probepathname', required=True)
@click.option('--outpath', 'outpathname', required=True)
@click.option('--count', 'comp_count', default=100)
@click.option('--all_impostors', 'all_imps', default=False)
def generate_match(ctx: click.Context, refpathname: str, probepathname: str, comp_count: int, all_imps: bool, outpathname: str):
    ref_identities = os.listdir(refpathname)

    genuine_file = open(os.path.join(outpathname, "genuine.txt"), "w")
    impostor_file = open(os.path.join(outpathname, "impostor.txt"), "w")

    for ref_identity in tqdm(ref_identities):
        ref_path = refpathname + "/" + ref_identity
        if not os.path.exists(ref_path):
            continue
        ref_features = [np.load(x) for x in [ref_path + "/" + y for y in os.listdir(ref_path) if ".npy" in y]]

        # genuine score
        probe_path = probepathname + "/" + ref_identity
        if not os.path.exists(probe_path):
            continue
        probe_features = [np.load(x) for x in [probe_path + "/" + y for y in os.listdir(probe_path) if ".npy" in y]]

        references = []
        probes = []

        if len(ref_features) < 2 or len(probe_features) < 2:
            continue
        if len(ref_features) < 3:
            ref_mul = 1
        else:
            ref_mul = 2
        if len(probe_features) < 3:
            probe_mul = 1
            probes.extend([probe_features[1]] * ref_mul)
        else:
            probe_mul = len(probe_features) - 2
            probes.extend(probe_features[2:] * ref_mul)

        references.extend([ref_features[0]] * probe_mul)
        if ref_mul > 1:
            references.extend([ref_features[1]] * probe_mul)

        references = np.vstack(references)
        probes = np.vstack(probes)
        gen_score = similarity(references, probes)
        for sim in gen_score:
            genuine_file.write(str(sim))
            genuine_file.write('\n')

        # impostor score
        if all_imps:
            impostors = ref_identities
        else:
            impostors = ["{:0>6d}".format(impostor) for impostor in
                         np.random.choice(list(range(0, int(ref_identity))) + list(range(int(ref_identity)+1, 10572)), size=comp_count)]
        references = []
        probes = []
        for impostor in impostors:
            impostor_path = probepathname + "/" + str(impostor)
            impostor_features = [np.load(x) for x in [impostor_path + "/" + y for y in os.listdir(impostor_path) if ".npy" in y]]

            if len(impostor_features) < 2:
                continue

            if len(impostor_features) < 3:
                probe_mul = 1
                probes.extend([impostor_features[1]] * ref_mul)
            else:
                probe_mul = len(impostor_features) - 2
                probes.extend(impostor_features[2:] * ref_mul)

            references.extend([ref_features[0]] * probe_mul)
            if ref_mul > 1:
                references.extend([ref_features[1]] * probe_mul)

        references = np.vstack(references)
        probes = np.vstack(probes)
        imp_score = similarity(references, probes)
        for sim in imp_score:
            impostor_file.write(str(sim))
            impostor_file.write('\n')

    impostor_file.close()
    genuine_file.close()


if __name__ == "__main__":
    generate_match()
