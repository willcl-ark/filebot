import configparser
import logging
import time
import re
from irc import Irc
from urlre import URL_REGEX
from parser import parse_url

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
)

c.connect()

while True:
    time.sleep(0.1)
    try:
        data = c.recv()
        if data:
            # log.debug(data)
            urls = re.findall(URL_REGEX, data)
            if urls:
                for url in urls:
                    res = parse_url(url, config.get("github_token"))
                    if res:
                        c.send("PRIVMSG", f'{config.get("channel")} {res}')
    except OSError as e:
        log.exception(e)
        log.warning("Trying to reconnect")
        c.reconnect()
    except Exception as e:
        log.exception(e)
