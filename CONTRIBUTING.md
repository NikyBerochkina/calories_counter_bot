# Contributing

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # add your own BOT_TOKEN for local testing
```

## Before opening a PR

```bash
ruff check .
pytest
```

Both run in CI and must pass.

## Style

- Keep functions small and typed where practical.
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages (`feat:`, `fix:`, `chore:`, ...).
- One logical change per PR; describe *why*, not just *what*, in the description.
