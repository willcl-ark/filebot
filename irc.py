import logging
import re

from urlre import URL_REGEX
from parser import parse_url

import trio

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Irc:
    def __init__(
        self,
        host,
        port,
        nick,
        password,
        conn_password,
        user_name,
        real_name,
        channel,
        github_token,
    ):
        self.host = host
        self.port = port
        self.nick = nick
        self.password = password
        self.conn_password = conn_password
        self.user_name = user_name
        self.real_name = real_name
        self.channel = channel
        self.github_token = github_token
        self.stream = None
        self.remote_ip = ""
        self.send_channel, self.receive_channel = trio.open_memory_channel(50)

    async def connect(self):
        self.stream = await trio.open_tcp_stream(self.host, self.port)
        log.debug("socket created")
        log.info(f"connected to: {self.host}:{self.port}")
        await self.authenticate()

    async def authenticate(self):
        await trio.sleep(1)
        await self.send("PASS", self.conn_password)
        await trio.sleep(1)
        await self.send("NICK", self.nick)
        await trio.sleep(1)
        await self.send("USER", f"{self.user_name} 0 * :{self.real_name}")
        await trio.sleep(1)
        await self.send("JOIN", f"{self.channel}")
        await trio.sleep(1)
        await self.send("PRIVMSG", f"NickServ :IDENTIFY {self.nick} {self.password}")

    async def send(self, command, data):
        log.debug(f"sending:  {command} {data}")
        await self.send_channel.send(f"{command} {data}\r\n".encode("utf-8"))

    async def sender(self):
        log.debug("sender: started!")
        while True:
            async for msg in self.receive_channel:
                await self.stream.send_all(msg)
                await trio.sleep(1)

    async def receiver(self):
        log.debug("receiver: started!")
        async for msg in self.stream:
            msg = msg.decode("utf-8")
            log.debug(f"received:\n{msg}")
            if msg[0:4] == "PING":
                await self.send("PONG", msg.split()[1])
            else:
                urls = re.findall(URL_REGEX, msg)
                if urls:
                    for url in urls:
                        res = parse_url(url, self.github_token)
                        if res:
                            await self.send("PRIVMSG", f"{self.channel} {res}")
        log.error("receiver: connection closed")
