## Getting Started

There are two main ways to set up a development environment for Plutus: using Nix or using a standard Python virtual environment.

### Local Development (with Nix)

The project uses [Nix Flakes](https://nixos.wiki/wiki/Flakes) to manage the development environment. To activate the environment, run:

```bash
nix develop
```

This will install all the necessary dependencies and create a virtual environment.

### Local Development (without Nix)

If you are not using Nix, you can set up a local development environment using Python's built-in `venv` module.

1.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    ```

2.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Bot

### Local Environment

To run the bot using a local Python environment, first create a `.env.development` file with the following content:

```
DISCORD_TOKEN=<your-discord-token>
ENVIRONMENT=dev
COMMAND_PREFIX="#"
TEST_GUILD_ID=<your-test-guild-id>
```

Then, activate your virtual environment and run the following command:

```bash
ENVIRONMENT=dev python main.py
```

This will start the bot in development mode.

### Docker (for Production)

Docker is used for production deployments. To run the bot using Docker, you first need to create a `.env.production` file with the following content:

```
DISCORD_TOKEN=<your-discord-token>
ENVIRONMENT=prod
COMMAND_PREFIX="#"
```

Then, you can build and run the Docker container using the following commands:

```bash
docker-compose build
docker-compose up -d
```

**Note:** It is recommended that developers use a local environment for development and testing, and use Docker only for production deployments.

## Project Structure

-   `main.py`: The main entry point of the bot.
-   `client.py`: The Discord client.
-   `cogs/`: Contains the cogs for the bot.
-   `utils/`: Contains utility functions.
-   `data/`: Contains the data structures for the bot.
-   `deployment/`: Contains the deployment scripts.
-   `requirements.txt`: The Python dependencies.
-   `Dockerfile`: The Dockerfile for the bot.
-   `docker-compose.yml`: The Docker Compose configuration.

## Contributing

1.  **Create a new branch:** `git checkout -b my-new-feature`
2.  **Make your changes.**
3.  **Commit your changes:** `git commit -am 'Add some feature'`
4.  **Push to the branch:** `git push origin my-new-feature`
5.  **Submit a pull request.**
