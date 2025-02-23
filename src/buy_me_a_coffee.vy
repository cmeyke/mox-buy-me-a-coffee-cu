# pragma version 0.4.0
"""
@license MIT
@author Carsten
@notice This contract is for creating a sample funding contract
"""

from interfaces import AggregatorV3Interface
import get_price_module

MINIMUM_USD: public(constant(uint256)) = as_wei_value(5, "ether")
# 0x694AA1769357215DE4FAC081bf1f309aDC325306 Sepolia
# 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 Mainnet
PRICE_FEED: public(immutable(AggregatorV3Interface))
OWNER: public(immutable(address))

funders: public(DynArray[address, 1000])
funder_to_amount_funded: public(HashMap[address, uint256])

@deploy
def __init__(price_feed_address: address):
    OWNER = msg.sender
    PRICE_FEED= AggregatorV3Interface(price_feed_address)

@external
@payable
def fund():
    self._fund()

@internal
@payable
def _fund():
    """
    Allows users to send $ to this contract
    Have a minimum $ amount send
    """
    usd_value_of_eth: uint256 = get_price_module._get_eth_to_usd_rate(PRICE_FEED, msg.value)
    assert usd_value_of_eth >= MINIMUM_USD, "You must spend more ETH!"
    self.funders.append(msg.sender)
    self.funder_to_amount_funded[msg.sender] += msg.value

@external
def withdraw():
    assert msg.sender == OWNER, "Not the contract owner!"
    # send(OWNER, self.balance)
    raw_call(OWNER, b"", value = self.balance)
    for founder: address in self.funders:
        self.funder_to_amount_funded[founder] = 0
    self.funders = []

@external
@view
def get_eth_to_usd_rate(eth_amount: uint256) -> uint256:
    return get_price_module._get_eth_to_usd_rate(PRICE_FEED, eth_amount)

@external
@payable
def __default__():
    self._fund()