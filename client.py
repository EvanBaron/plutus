from typing import override, Any
import discord
from discord.ext import commands
import traceback


class PlutusBot(commands.Bot):
    """Custom bot class for the bot."""

    def __init__(
        self,
        command_prefix: str,
        intents: discord.Intents,
        test_guild_id: int | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            command_prefix=command_prefix, intents=intents, help_command=None, **kwargs
        )

        self.test_guild_id: int | None = test_guild_id
        self.initial_extensions: list[str] = []

    @override
    async def setup_hook(self) -> None:
        """Setup hook called when bot is starting up."""

        print("-" * 50)
        print("Starting Plutus...")
        print("-" * 50)

        # Load all cogs
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"✓ Loaded extension: {extension}")
            except Exception:
                print(f"✗ Failed to load extension {extension}")
                traceback.print_exc()

        # Sync commands
        try:
            print("\nSyncing command tree...")

            if self.test_guild_id:
                # Sync to test guild
                guild = discord.Object(id=self.test_guild_id)
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                print(
                    f"✓ Synced {len(synced)} command(s) to test guild (ID: {self.test_guild_id})"
                )
                print("  Commands will be available instantly in the test guild!")
            else:
                # Sync globally
                synced = await self.tree.sync()
                print(f"✓ Synced {len(synced)} command(s) globally")
                print("  ⚠️ Global commands may take up to 1 hour to appear")
        except Exception as exception:
            print(f"✗ Failed to sync commands: {exception}")
            traceback.print_exc()

        print("-" * 50)

    async def on_ready(self) -> None:
        """Called when bot is ready."""

        print(f"\n{'-' * 50}")
        print("Bot is ready!")
        if self.user:
            print(f"Logged in as: {self.user.name} (ID: {self.user.id})")

        print(f"Connected to {len(self.guilds)} guild(s)")

        if self.test_guild_id:
            print(f"Development Mode: Commands synced to guild {self.test_guild_id}")
        else:
            print("Production Mode: Commands synced globally")

        print(f"{'-' * 50}\n")

        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=""),
            status=discord.Status.online,
        )

    @override
    async def on_command_error(
        self, context: commands.Context[Any], error: commands.CommandError
    ) -> None:
        """Global error handler for prefix commands."""

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await context.send(f"❌ Missing required argument: `{error.param.name}`")
        elif isinstance(error, commands.BadArgument):
            await context.send("❌ Invalid argument provided.")
        elif isinstance(error, commands.MissingPermissions):
            await context.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await context.send(
                "❌ I don't have the necessary permissions to execute this command."
            )
        else:
            print(f"Error in command {context.command}: {error}")
            traceback.print_exc()
            await context.send("❌ An error occurred while executing the command.")

    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        """Global error handler for slash commands."""

        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏱️ This command is on cooldown. Try again in {error.retry_after:.1f}s.",
                ephemeral=True,
            )
        elif isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ You don't have permission to use this command.", ephemeral=True
            )
        elif isinstance(error, discord.app_commands.BotMissingPermissions):
            await interaction.response.send_message(
                "❌ I don't have the necessary permissions to execute this command.",
                ephemeral=True,
            )
        elif isinstance(error, discord.app_commands.CheckFailure):
            await interaction.response.send_message(
                "❌ You cannot use this command.", ephemeral=True
            )
        else:
            print(f"Error in slash command: {error}")
            traceback.print_exc()

            try:
                if interaction.response.is_done():
                    await interaction.followup.send(
                        "❌ An error occurred while executing the command.",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        "❌ An error occurred while executing the command.",
                        ephemeral=True,
                    )
            except Exception:
                pass


def create_bot(command_prefix: str, test_guild_id: int | None = None) -> PlutusBot:
    """
    Create and configure the bot instance.

    Args:
        command_prefix: Prefix for text commands
        test_guild_id: Optional guild ID for instant command syncing (development)

    Returns:
        Configured PlutusBot instance
    """

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    intents.guilds = True

    bot = PlutusBot(
        command_prefix=command_prefix,
        intents=intents,
        test_guild_id=test_guild_id,
        case_insensitive=True,
    )

    return bot
