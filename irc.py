import logging
import socket
import time


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Irc:
    def __init__(
        self, host, port, nick, password, conn_password, user_name, real_name, channel
    ):
        self.host = host
        self.port = port
        self.nick = nick
        self.password = password
        self.conn_password = conn_password
        self.user_name = user_name
        self.real_name = real_name
        self.channel = channel
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_ip = ""

    def connect(self):
        log.debug("socket created")
        remote_ip = socket.gethostbyname(self.host)
        log.info(f"ip of irc server is: {remote_ip}")
        self.socket.connect((self.host, self.port))
        log.info(f"connected to: {self.host}:{self.port}")
        self.authenticate()

    def authenticate(self):
        time.sleep(0.1)
        self.send("PASS", self.conn_password)
        _ = self.recv()
        time.sleep(0.1)
        self.send("NICK", self.nick)
        _ = self.recv()
        time.sleep(0.1)
        self.send("USER", f"{self.user_name} 0 * :{self.real_name}")
        _ = self.recv()
        time.sleep(0.1)
        self.send("JOIN", f"{self.channel}")
        _ = self.recv()
        time.sleep(0.1)
        self.send("PRIVMSG", f"NickServ :IDENTIFY {self.nick} {self.password}")
        _ = self.recv()

    def send(self, command, data):
        log.debug(f"Sending message: {command} {data}")
        self.socket.send(f"{command} {data}\r\n".encode("utf-8"))

    def recv(self):
        d = self.socket.recv(4096).decode("utf-8")
        if d:
            if "\n" in d:
                log.debug(f"\n{d}")
            else:
                log.debug(d)
        return d

    def reconnect(self):
        time.sleep(2)
        self.socket.close()
        time.sleep(2)
        self.connect()
