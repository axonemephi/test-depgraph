"""Entry point for running depgraph as a module: python -m depgraph"""

from .cli import DepGraphCLI

if __name__ == '__main__':
    DepGraphCLI.main()

