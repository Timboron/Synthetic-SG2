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
        id_path = os.path.join(inpath, identity)
        images = os.listdir(id_path)
        for idx, image in enumerate(images):
            if identity == "000000":
                print("in:", os.path.join(id_path, image), "    out:", os.path.join(outpath, identity, image))
            if int(before) < idx <= int(after):
                shutil.copyfile(os.path.join(id_path, image), os.path.join(outpath, identity, image))


if __name__ == "__main__":
    generate_match()