import os
import itertools
import click
import numpy as np
import random
from scipy import spatial
from tqdm import tqdm
from numpy import dot
from numpy.linalg import norm

@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
def generate_match(ctx: click.Context, pathname: str):
    identities = os.listdir(pathname)

    variances = []

    for identity in tqdm(identities):
        id_path = pathname + "/" + identity
        features = [np.load(x) for x in [id_path + "/" + y for y in os.listdir(id_path) if ".npy" in y]]
        variances.append(np.mean(np.var(np.array(features), axis=0)))
    print(sum(variances)/len(variances))





if __name__ == "__main__":
    generate_match()
