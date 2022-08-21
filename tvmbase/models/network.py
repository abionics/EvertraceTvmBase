from dataclasses import dataclass

from tvmbase.exceptions import UnknownNetworkException


@dataclass(frozen=True, slots=True)
class Network:
    endpoints: list[str]
    everlive_domain: str
    everscan_domain: str

    @classmethod
    def mainnet(cls, evercloud_key: str) -> 'Network':
        return cls(
            [f'https://mainnet.evercloud.dev/{evercloud_key}/graphql'],
            'ever.live',
            'everscan.io',
        )

    @classmethod
    def devnet(cls, evercloud_key: str) -> 'Network':
        return Network(
            [f'https://devnet.evercloud.dev/{evercloud_key}/graphql'],
            'ever.live',
            'everscan.io',
        )

    @classmethod
    def tonred(cls) -> 'Network':
        return Network(
            ['net.ton.red'],
            'ever.live',
            'everscan.io',
        )

    @classmethod
    def from_name(cls, name: str, evercloud_key: str = None) -> 'Network':
        match name.lower():
            case 'main' | 'mainnet':
                return cls.mainnet(evercloud_key)
            case 'dev' | 'devnet':
                return cls.devnet(evercloud_key)
            case 'red' | 'tonred' | 'rednet':
                return cls.tonred()
        raise UnknownNetworkException(name)
