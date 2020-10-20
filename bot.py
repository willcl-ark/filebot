import configparser
import logging
import trio

from irc import Irc

logging.basicConfig(filename="log", level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("bot")
log.setLevel(logging.INFO)
logging.getLogger("github.Requester").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

# Rename "sample_config" to "config" and fill details

config = configparser.ConfigParser()
config.read("config")
config = config["settings"]

c = Irc(
    config.get("host"),
    int(config.get("port")),
    config.get("nick"),
    config.get("password"),
    config.get("conn_password"),
    config.get("username"),
    config.get("realname"),
    config.get("channel"),
    config.get("github_token"),
)


async def main():
    await c.connect()
    async with trio.open_nursery() as nursery:
        log.debug("parent: spawning sender...")
        nursery.start_soon(c.sender)

        log.debug("parent: spawning receiver...")
        nursery.start_soon(c.receiver)

trio.run(main)
