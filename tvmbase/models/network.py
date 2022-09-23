from dataclasses import dataclass

from tvmbase.exceptions import NetworkException
from tvmbase.utils.singleton import SingletonMeta


@dataclass(frozen=True, slots=True)
class Network:
    name: str
    endpoints: list[str]
    everlive_domain: str
    everscan_domain: str


class NetworkFactory(metaclass=SingletonMeta):
    custom_networks: dict[str, Network] = dict()

    def __init__(self, evercloud_key: str):
        self.evercloud_key = evercloud_key

    def mainnet(self) -> Network:
        return Network(
            name='main',
            endpoints=[f'https://mainnet.evercloud.dev/{self.evercloud_key}/graphql'],
            everlive_domain='ever.live',
            everscan_domain='everscan.io',
        )

    def devnet(self) -> Network:
        return Network(
            name='dev',
            endpoints=[f'https://devnet.evercloud.dev/{self.evercloud_key}/graphql'],
            everlive_domain='ever.live',
            everscan_domain='everscan.io',
        )

    def from_name(self, name: str) -> Network:
        name = name.lower()
        match name:
            case 'main' | 'mainnet':
                return self.mainnet()
            case 'dev' | 'devnet':
                return self.devnet()
        if name in self.custom_networks:
            return self.custom_networks.get(name)
        raise NetworkException(f'Unknown network "{name}"')

    @staticmethod
    def add_custom(network: Network):
        NetworkFactory.custom_networks[network.name] = network

    def get_all(self) -> list[Network]:
        return [self.mainnet(), self.devnet()] + list(self.custom_networks.values())
