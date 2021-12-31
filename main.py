from random import randint
import argparse
from typing import Optional, List, Iterable, Tuple

from icmplib import ICMPv4Socket, ICMPRequest, TimeoutExceeded, ICMPSocketError, SocketUnavailableError, traceroute

IpAddr = str

U16_MAX = 65535


class Traceroute:
    def __init__(self, sock: ICMPv4Socket, destination: str, max_ttl: int, timeout: int):
        assert timeout > 0
        assert 0 < max_ttl < 256
        self.sock = sock
        self.destination = destination
        self.max_ttl = max_ttl
        self.timeout = timeout
        self.__id = randint(0, U16_MAX)
        self.__seq = 0

    def __ping(self, cur_ttl: int) -> IpAddr:
        req = ICMPRequest(self.destination, id=1, sequence=cur_ttl, ttl=cur_ttl)
        self.sock.send(req)
        try:
            reply = self.sock.receive(req, timeout=self.timeout)
            return reply.source
        except TimeoutExceeded:
            return "*** (Timeout)"
        except (SocketUnavailableError, ICMPSocketError) as e:
            return f"Socket Error: {e}"

    def trace(self) -> Iterable[IpAddr]:
        for ttl in range(1, self.max_ttl):
            cur_ip = self.__ping(ttl)
            yield cur_ip
            if cur_ip == self.destination:
                break


def parse_args() -> Tuple[str, int, int]:
    """
    :return: (destination, max_ttl, timeout)
    """
    parser = argparse.ArgumentParser(description="Tracert program")
    parser.add_argument("destination", type=str, help="Destination IPv4 address")
    parser.add_argument("--max-ttl", "-m", type=int, help="Max TTL (Max hops)", default=30)
    parser.add_argument("--timeout", type=int, help="Timeout (in seconds)", default=2)
    args = parser.parse_args()
    return args.destination, args.max_ttl, args.timeout


def main():
    destination, max_ttl, timeout = parse_args()
    print(f"Max TTL = {max_ttl}, timeout = {timeout}")

    sock = ICMPv4Socket(privileged=True)

    print(f"Path to {destination}:")

    last_ip = None
    for i, ip in enumerate(Traceroute(sock, destination, max_ttl, timeout).trace()):
        last_ip = ip
        print(f"\t{i + 1}) {ip}")

    if last_ip != destination:
        print("Could not reach the destination. Try increasing the Max TTL (-m)")


if __name__ == "__main__":
    main()
