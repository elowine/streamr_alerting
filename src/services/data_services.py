import json
from typing import Optional

from src.common import config
import requests as rq
from datetime import datetime

from src.services.util_services import UtilServices


class DataServices:
    def __init__(self, Currency: Optional[str] = "USD", UrlBrubeckStreamr: Optional[str] = None
                 ):
        self.util = UtilServices()
        self.currency = Currency or config.currency
        self.url_brubeck1_streamr = UrlBrubeckStreamr or config.url_brubeck1_streamr

    def price_token_data(self) -> int:
        try:
            pricevalue_url = config.url_api_price + self.currency
            response = rq.get(pricevalue_url)
            return response.json()[self.currency]
        except Exception as e:
            print(e)

    def data_reward(self, node: str):
        try:
            resp = rq.get(self.url_brubeck1_streamr + config.stats + node)

            if resp.status_code != 200:
                raise ValueError("Error call api in data_reward")

            json_data = json.loads(resp.text)
            if not json_data["claimedRewardCodes"]:
                raise ValueError("Error no data claimedRewardCode")

            return json_data
        except Exception as e:
            print(e)

    def data_apy(self):
        try:
            resp = rq.get(self.url_brubeck1_streamr + config.apy)

            if resp.status_code != 200:
                raise ValueError("Error call api in data_apy")

            json_data = json.loads(resp.text)
            if not json_data["24h-APY"] or not json_data["24h-APR"]:
                raise ValueError("Error missing data APY")

            return json_data
        except Exception as e:
            print(e)

    def percent_data(self, data_reward: dict):
        try:
            if ((data_reward["claimPercentage"]), 5) == 1:
                return "100%"
            elif ((data_reward["claimPercentage"]), 5) == 0:
                return "0%"
            else:
                return str(round(float(data_reward["claimPercentage"]) * 100, 2)) + "%"
        except Exception as e:
            print(e)

    def first_date_reward(self, data_reward: dict):
        try:
            if data_reward["claimedRewardCodes"]:
                result = datetime.strptime(data_reward["claimedRewardCodes"][0]["claimTime"][:-5].replace("T", " "),
                                           "%Y-%m-%d %H:%M:%S")
                return result
        except Exception as e:
            print(e)

    def status_node(self, data_reward: dict):
        try:
            if data_reward["claimedRewardCodes"]:

                last_claimed_reward = data_reward["claimedRewardCodes"][len(data_reward["claimedRewardCodes"]) - 1][
                    "claimTime"]
                last_claimed_reward = datetime.strptime(last_claimed_reward[:-5].replace("T", " "), "%Y-%m-%d %H:%M:%S")

                if ((datetime.utcnow() - last_claimed_reward).seconds < 4500):
                    return config.online
                elif ((datetime.utcnow() - last_claimed_reward).seconds > 4500 and (
                        datetime.utcnow() - last_claimed_reward).seconds < 9000):
                    return f"possible {config.offline}"
                else:
                    return config.offline
        except Exception as e:
            print(e)

    def reward(self, node: str):
        try:
            resp = rq.get(self.url_brubeck1_streamr + config.datarewards + node)

            if resp.status_code != 200:
                raise ValueError("Error call api in reward")

            json_data = json.loads(resp.text)
            if json_data["DATA"]:
                result = json_data["DATA"]
                return result
            else:
                print("Reward : no data found")
        except Exception as e:
            print(e)

    def paid_data(self, node: str):
        try:
            paid_data = 0
            json_data = {
                'query': '{\n  erc20Transfers(\n    where: {\n      from: "0x3979f7d6b5c5bfa4bcd441b4f35bfa0731ccfaef"\n      to: "' + node.lower() + '"\n      timestamp_gt: "1646065752"\n    }\n  ) {\n    timestamp\n    value\n  }\n}\n',
            }

            response = rq.post('https://api.thegraph.com/subgraphs/name/streamr-dev/data-on-polygon', json=json_data)
            json_data = json.loads(response.text)

            for index, data in enumerate(json_data["data"]["erc20Transfers"]):
                paid_data += round(float(json_data["data"]["erc20Transfers"][index]["value"]), 2)

            return paid_data
        except Exception as e:
            print(e)

    def staked_data(self, node: str):
        try:
            staked_data = 0
            json_data = {
                'query': '{\n  erc20Balances(where: {account: "' + node.lower() + '", contract:"0x3a9a81d576d83ff21f26f325066054540720fc34"}) {\n    value \n  }\n}',
            }

            response = rq.post('https://api.thegraph.com/subgraphs/name/streamr-dev/data-on-polygon', json=json_data)
            json_data = json.loads(response.text)

            staked_data += round(float(json_data["data"]["erc20Balances"][0]["value"]), 2)
            return staked_data
        except Exception as e:
            print(e)

    def apy(self, data_reward: dict) -> float:
        return round(float(data_reward["24h-APY"]), 2)

    def apr(self, data_reward: dict) -> float:
        return round(float(data_reward["24h-APR"]), 2)

    def estimate_reward(self, date_first_reward, reward):
        try:
            mining_days, mining_hours = self.util.date_diff(date_first_reward)
            reward_month = round(reward / (mining_days * 24 + mining_hours) * 732, 2)
            reward_year = round(reward / (mining_days * 24 + mining_hours) * 8772, 2)

            return reward_month, reward_year
        except Exception as e:
            print(e)
