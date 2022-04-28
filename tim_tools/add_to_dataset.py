import shutil
from tqdm import tqdm
import os

import click

@click.command()
@click.pass_context
@click.option('--inpath', 'inpath', required=True)
@click.option('--outpath', 'outpath', required=True)
@click.option('--before', 'before', default=-1)
@click.option('--after', 'after', required=True)
def generate_match(ctx: click.Context, inpath: str, outpath: str, before: int, after: int):
    identities = os.listdir(inpath)
    print(identities)
    for identity in tqdm(identities):
        images = os.listdir(os.path.join(inpath, identity))
        for idx, image in enumerate(images):
            if int(before) < idx <= int(after):
                print(idx)
                shutil.copyfile(os.path.join(inpath, identity, image), os.path.join(outpath, identity, image))


if __name__ == "__main__":
    generate_match()