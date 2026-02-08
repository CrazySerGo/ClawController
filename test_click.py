import click
import sys

@click.command()
@click.option("--message")
@click.option("--agent")
@click.option("--dangerous", is_flag=True)
def main(message, agent, dangerous):
    print(f"message: {message}")
    print(f"agent: {agent}")
    print(f"dangerous: {dangerous}")

if __name__ == "__main__":
    main()
