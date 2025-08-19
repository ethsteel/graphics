# STEEL Team Graphics

This repo contains:

- graphics and logos,
- scripts to generate plots.

## Prerequisites

### GitHub CLI Setup

Scripts that fetch data require the GitHub CLI (`gh`) for API access:

1. **Install GitHub CLI**: Follow the installation guide at [cli.github.com](https://cli.github.com)

2. **Authenticate with GitHub**:

   ```bash
   gh auth login
   ```

   Follow the prompts to authenticate. This creates a token automatically.

3. **Verify authentication**:

   ```bash
   gh auth status
   ```

**Note**: Authentication is required to avoid GitHub API rate limits (60 requests/hour for unauthenticated vs 5000/hour for authenticated requests).

### System/Python Requirements

- **uv**: Package manager for running the scripts
- Python must not be installed; `uv` will fetch and download the required version, if not present.

### Python3-tk

I'm not 100% sure this is needed tbh.

```bash
sudo apt install python3-tk
```

#### Installing uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See [docs.astral.sh/uv](https://docs.astral.sh/uv/) for more installation options.
