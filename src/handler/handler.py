from typing import Optional, List
from currency_symbols import CurrencySymbols

from common import config

from services.data_services import DataServices
from services.discord_services import DiscordServices
from services.telegram_services import TelegramServices
from services.util_services import UtilServices


class Handler:

    def __init__(self, Currency: Optional[str] = "USD", ListNodes: Optional[List] = None):
        self.currency = Currency or config.currency
        self.list_nodes = ListNodes or config.list_nodes
        self.data = DataServices()
        self.discord = DiscordServices()
        self.telegram = TelegramServices()
        self.util = UtilServices()

    def get_info(self):
        try:
            if not self.list_nodes:
                raise ValueError("config list_nodes is empty")

            currency_symbol = CurrencySymbols.get_symbol(self.currency)
            coin_value = self.data.price_token_data()
            sum_paid_data = 0
            sum_reward = 0
            sum_staked_data = 0
            sum_staked_currentcy = 0
            sum_paid_currentcy = 0
            sum_reward_currentcy = 0
            sum_est_month_reward = 0
            sum_est_year_reward = 0
            data_for_message = {}
            sum_status_node = {}
            for node in self.list_nodes:
                data_for_message["currency_symbol"] = currency_symbol
                address_node = node.get('address')
                data_for_message["name"] = node.get('name')
                data_reward = self.data.data_reward(address_node)
                if data_reward:
                    date_first_reward = self.data.first_date_reward(data_reward)
                    reward = self.data.reward(address_node)
                    data_for_message["reward"] = reward
                    paid_data = self.data.paid_data(address_node)
                    data_for_message["paid_data"] = paid_data
                    staked_data = self.data.staked_data(address_node)
                    data_for_message["staked_data"] = staked_data
                    data_for_message["status_node"] = self.data.status_node(data_reward)
                    data_for_message["percent_reward"] = self.data.percent_data(data_reward)
                    data_apy = self.data.data_apy()
                    data_for_message["apy"] = self.data.apy(data_apy)
                    data_for_message["apr"] = self.data.apr(data_apy)

                    data_for_message["reward_currentcy"] = round(coin_value * reward, 2)
                    data_for_message["paid_currentcy"] = round(coin_value * paid_data, 2)
                    data_for_message["staked_currentcy"] = round(coin_value * staked_data, 2)

                    data_for_message["est_month_reward"], data_for_message[
                        "est_year_reward"] = self.data.estimate_reward(date_first_reward, reward)

                    if config.sum_node:
                        sum_paid_data += paid_data
                        sum_reward += reward
                        sum_staked_data += staked_data
                        sum_reward_currentcy = round(coin_value * sum_reward, 2)
                        sum_paid_currentcy = round(coin_value * sum_paid_data, 2)
                        sum_staked_currentcy = round(coin_value * sum_staked_data, 2)
                        sum_est_month_reward += data_for_message["est_month_reward"]
                        sum_est_year_reward += data_for_message["est_year_reward"]
                        sum_status_node[data_for_message["name"]] = data_for_message["status_node"]

                    if config.discord_notif or config.telegram_notif:
                        if config.discord_notif:
                            content = self.util.message_notif(config.discord, data_for_message, coin_value)
                            self.discord.send_message(config.discord_channel_id, config.discord_token, content)
                        if config.telegram_notif:
                            content = self.util.message_notif(config.telegram, data_for_message, coin_value)
                            self.telegram.send_message(config.telegram_chat_id, config.telegram_token, content)

                    if config.save_in_file:
                        self.util.save_in_file(str(data_for_message))

            data_for_message["sum_paid_data"] = sum_paid_data
            data_for_message["sum_reward"] = sum_reward
            data_for_message["sum_staked_data"] = sum_staked_data
            data_for_message["sum_reward_currentcy"] = sum_reward_currentcy
            data_for_message["sum_paid_currentcy"] = sum_paid_currentcy
            data_for_message["sum_staked_currentcy"] = sum_staked_currentcy
            data_for_message["sum_status_node"] = sum_status_node
            data_for_message["sum_est_month_reward"] = sum_est_month_reward
            data_for_message["sum_est_year_reward"] = sum_est_year_reward

            if config.sum_node and (config.discord_notif or config.telegram_notif):
                if config.discord_notif:
                    content = self.util.message_notif(config.discord, data_for_message, coin_value, config.sum_node)
                    self.discord.send_message(config.discord_channel_id, config.discord_token, content)
                if config.telegram_notif:
                    content = self.util.message_notif(config.telegram, data_for_message, coin_value, config.sum_node)
                    self.telegram.send_message(config.telegram_chat_id, config.telegram_token, content)

        except Exception as e:
            print(e)

    def status_node(self, address_node):
        data_reward = self.data.data_reward(address_node)
        return self.data.status_node(data_reward) == config.offline

    def check_status_node(self):
        try:
            for node in self.list_nodes:
                data = {}
                address_node = node.get('address')
                data['name'] = node.get('name')
                if self.status_node(address_node):
                    data_fichier = {
                        data['name']: "KO"
                    }
                    if config.discord_notif:
                        content = self.util.message_node_offline(config.telegram, data)
                        self.discord.send_message(config.discord_channel_id, config.discord_token, content)
                    if config.telegram_notif:
                        content = self.util.message_node_offline(config.telegram, data)
                        self.telegram.send_message(config.telegram_chat_id, config.telegram_token, content)
                else:
                    data_fichier = {
                        data['name']: "OK"
                    }

                if config.save_in_file:
                    self.util.save_in_file(str(data_fichier), "status")
        except Exception as e:
            print(e)
