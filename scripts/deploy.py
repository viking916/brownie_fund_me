from brownie import FundMe, network, config, MockV3Aggregator
from scripts.supplement import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENT


def deploy_fund_me():
    account = get_account()

    print("Checking if Mocks will be needed...")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        print("Skipping Mocks as deployment will be on test or main net.")
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    print("Begun deployment of FundMe contract...")
    # pass the price feed address to our fundme contract
    # if we are on a presistent network like rinkeby, use the associated address
    # otherwise, deploy mock
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract FundMe deploy successfully!")
    return fund_me


def main():
    deploy_fund_me()
