from unittest.mock import Mock, patch

import pytest
from discord.ext import commands

# This is a mock import; replace it with actual module import in real testing environment
from app import (
    SAVE_DIRECTORY,
    Dalle,
    bot,
    clear,
    generate,
    generate_error,
    ping,
    setdir,
)


# Mock the Discord context
@pytest.fixture()
def mock_ctx():
    return Mock(spec=commands.Context, autospec=True)

# Mock the Dalle instance
@pytest.fixture()
def mock_dalle():
    return Mock(spec=Dalle, autospec=True)

# ------- Basic Tests --------

def test_bot_running():
    assert bot is not None

def test_generate_command(mock_ctx, mock_dalle):
    prompt = "Test Prompt"
    with patch("app.Dalle", mock_dalle):
        bot.loop.run_until_complete(generate(mock_ctx, prompt=prompt))
    mock_dalle.run.assert_called_once_with(prompt)

def test_ping_command(mock_ctx):
    bot.loop.run_until_complete(ping(mock_ctx))
    mock_ctx.send.assert_called_once_with("Pong!")

def test_setdir_command(mock_ctx):
    directory = "test_directory/"
    bot.loop.run_until_complete(setdir(mock_ctx, directory=directory))
    assert SAVE_DIRECTORY == directory
    mock_ctx.send.assert_called_once_with(f"Directory set to: {directory}")

# ------- Parameterized Testing --------

@pytest.mark.parametrize(
    "amount, expected_limit",
    [
        (5, 5),
        (None, 10),
        (20, 20),
    ]
)
def test_clear_command(mock_ctx, amount, expected_limit):
    bot.loop.run_until_complete(clear(mock_ctx, amount))
    mock_ctx.channel.purge.assert_called_once_with(limit=expected_limit)

# ------- Mocks and Monkeypatching --------

def test_dalle_run_called_during_generate(mock_ctx, monkeypatch):
    prompt = "Test Prompt"

    def mock_run(*args, **kwargs):
        return True

    monkeypatch.setattr(Dalle, "run", mock_run)
    bot.loop.run_until_complete(generate(mock_ctx, prompt=prompt))

# ------- Exception Testing --------

def test_generate_command_without_prompt(mock_ctx):
    with pytest.raises(commands.MissingRequiredArgument):
        bot.loop.run_until_complete(generate(mock_ctx))

def test_generate_error_command_missing_arg(mock_ctx):
    error = commands.MissingRequiredArgument(param=Mock())
    bot.loop.run_until_complete(generate_error(mock_ctx, error))
    mock_ctx.send.assert_called_once_with("You must provide a prompt for image generation!")

def test_generate_error_command_general_error(mock_ctx):
    error = Exception("Some random error")
    bot.loop.run_until_complete(generate_error(mock_ctx, error))
    mock_ctx.send.assert_called_once_with(f"An error occurred: {error}")

