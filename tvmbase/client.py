from typing import Any, TYPE_CHECKING

from tonclient.client import TonClient
from tonclient.types import (
    ClientConfig,
    NetworkConfig,
    AbiContract,
    Abi,
    CallSet,
    ParamsOfEncodeMessage,
    Signer,
    ParamsOfRunTvm,
)

from models.network import Network
from utils.singleton import SingletonMeta

if TYPE_CHECKING:
    from models.tvm.account import Account


class Client(TonClient, metaclass=SingletonMeta):

    def __init__(self, network: Network):
        config = self.create_config(network)
        super().__init__(config, is_async=True)

    @staticmethod
    def create_config(network: Network) -> ClientConfig:
        network_config = NetworkConfig(endpoints=network.endpoints)
        return ClientConfig(network=network_config)

    async def run_local(
            self,
            account: 'Account',
            abi: AbiContract,
            method: str,
            params: dict = None,
            parse: bool = False,
    ) -> dict | Any:
        """
        :return: dict in case of `parse` is False, otherwise parse response and return Any type
        """
        abi = Abi.Contract(abi)
        call_set = CallSet(function_name=method, input=params)
        message_params = ParamsOfEncodeMessage(
            abi=abi,
            address=account.address,
            signer=Signer.NoSigner(),
            call_set=call_set,
        )
        message = await self.abi.encode_message(params=message_params)

        run_params = ParamsOfRunTvm(message=message.message, account=account.data.boc, abi=abi)
        result = await self.tvm.run_tvm(params=run_params)
        decoded = result.decoded.output

        if parse:
            if len(decoded) != 1:
                raise Exception('Must be exact one output param for automatic parse')
            return decoded.popitem()[1]
        else:
            return decoded

    # todo
    # async def emulate_local(
    #         self,
    #         account: 'Account',
    #         abi: str,
    #         method: str,
    #         params: dict,
    #         value: int,
    #         bounce: bool = None,
    #         sender: str = None,  # todo jenkins
    # ) -> ResultOfRunTvm:
    #     # print(value / 1e9)
    #     if sender is None:
    #         sender = '0:' + '12' * 32  # todo
    #     abi = Abi.Json(abi)
    #     call_set = CallSet(function_name=method, input=params)
    #     message_params = ParamsOfEncodeInternalMessage(
    #         value=str(value),
    #         abi=abi,
    #         address=account.address,
    #         call_set=call_set,
    #         bounce=bounce,
    #         src_address=sender,
    #     )
    #     message = await self.abi.encode_internal_message(params=message_params)
    #     # run_params = ParamsOfRunTvm(
    #     #     message=message.message,
    #     #     account=account.data.boc,
    #     #     abi=abi,
    #     #     return_updated_account=True
    #     # )
    #     # return await self.tvm.run_tvm(params=run_params)
    #     account = AccountForExecutor.Account(boc=account.data.boc)
    #     run_params = ParamsOfRunExecutor(
    #         message=message.message,
    #         account=account,
    #         abi=abi,
    #         skip_transaction_check=True,
    #         return_updated_account=True,
    #     )
    #     return await self.tvm.run_executor(params=run_params)