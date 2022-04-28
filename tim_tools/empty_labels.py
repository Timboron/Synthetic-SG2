import os
import click


@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
def generate_match(ctx: click.Context, pathname: str):

    identities = os.listdir(pathname)
    empty_labels = []
    one_labels = []

    for identity in identities:
        images = os.listdir(os.path.join(pathname, identity))
        if len(images) == 0:
            empty_labels.append(identity)
        if len(images) == 1:
            one_labels.append(identity)
        if len(images) < 200:
            print(len(images))

    print("empty:",len(empty_labels))
    print("one:", len(one_labels))

if __name__ == "__main__":
    generate_match()