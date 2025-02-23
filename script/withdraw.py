from src import buy_me_a_coffee
from moccasin.config import get_active_network

def withdraw():
    active_network = get_active_network()
    coffee = active_network.manifest_named("buy_me_a_coffee")
    # coffee = active_network.get_latest_contract_checked("buy_me_a_coffee")
    print(f"Using coffee contract at: {coffee.address}")
    coffee.withdraw()

def moccasin_main():
    withdraw()