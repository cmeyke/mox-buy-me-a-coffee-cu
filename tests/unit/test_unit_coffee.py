from eth_utils import to_wei, address
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non_owner")

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fund_with_money(coffee_funded, account):
    # Assert
    funder = coffee_funded.funders(0)
    assert funder == account.address
    assert coffee_funded.funder_to_amount_funded(funder) == SEND_VALUE
    assert boa.env.get_balance(coffee_funded.address) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act and Assert
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded, account):
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0

def test_fund_and_withdraw(coffee, account):
    # Arrange
    for i in range(10):
        funder = boa.env.generate_address(f"funder_{i}")
        boa.env.set_balance(funder, SEND_VALUE)
        with boa.env.prank(funder):
            coffee.fund(value=SEND_VALUE)

    # Act
    initial_balance = boa.env.get_balance(account.address)
    coffee.withdraw()

    # Assert
    assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(account.address) - initial_balance == SEND_VALUE * 10

def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0