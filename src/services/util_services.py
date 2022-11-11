import os
from datetime import datetime
from common import config


class UtilServices:

    def date_diff(self, start_date):
        try:
            mining_time = datetime.now() - start_date
            mining_days = mining_time.days
            mining_hours, remainder = divmod(mining_time.seconds, 3600)
            return mining_days, mining_hours
        except Exception as e:
            print(e)

    def strfdelta(self, tdelta, fmt):
        try:
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)
        except Exception as e:
            print(e)

    def save_in_file(self, data: str, name_file: str = "data"):
        if not os.path.isdir(f"{os.getcwd()}/src/{config.dir_save}"):
            os.makedirs(f"{os.getcwd()}/src/{config.dir_save}")
        fichier = open(
            f"{os.getcwd()}/src/{config.dir_save}/{datetime.now().strftime('%Y%m%d-%H%M')}_{name_file}.txt",
            "a")
        fichier.write(data + "\n")

    def message_node_offline(self, service_notif: str, data):
        etoile = ""
        if service_notif == config.discord:
            etoile = "**"
        content = "--------------------------------------------\n"
        content += f"{etoile}Streamr Node Infos{etoile}\n"
        content += f"{etoile}{data['name']}{etoile}\n"
        content += f"Node Status : {config.offline}\n"
        content += "--------------------------------------------\n"
        return content

    def message_notif(self, service_notif: str, data, sum_data: bool = False) -> str:
        etoile = ""
        if service_notif == config.discord:
            etoile = "**"

        content = "--------------------------------------------\n"
        content += f"{etoile}Streamr Node Infos{etoile}\n"

        if sum_data:
            if config.offline in data['sum_status_node'].values():
                status_node = config.offline
            else:
                status_node = config.online

            content += f"{etoile}SUM DATA{etoile}\n"
            content += f"Node Status : {status_node}\n"
            content += f"Total Stacked : {data['sum_staked_data']} | {data['sum_staked_currentcy']}{data['currency_symbol']}\n"
            content += f"Received Rewards : {data['sum_paid_data']} | {data['sum_paid_currentcy']}{data['currency_symbol']}\n"
            content += f"Accumulated Rewards : {data['sum_reward']} | {data['sum_reward_currentcy']}{data['currency_symbol']} \n\n"

        else:
            content += f"{etoile}{data['name']}{etoile}\n"
            content += f"Node Status : {data['status_node']}\n"
            content += f"Total Stacked : {data['staked_data']} | {data['staked_currentcy']}{data['currency_symbol']}\n"
            content += f"Received Rewards : {data['paid_data']} | {data['paid_currentcy']}{data['currency_symbol']}\n"
            content += f"Accumulated Rewards : {data['reward']} | {data['reward_currentcy']}{data['currency_symbol']} \n"
            content += f"Percent Rewards : {data['percent_reward']}: \n\n"

        content += f"APR : {data['apr']}%\n"
        content += f"APY : {data['apy']}%\n"
        content += "--------------------------------------------\n"
        content += f"{etoile}Estimated{etoile}\n"
        content += f"Month Reward : {data['est_month_reward']}\n"
        content += f"Year Reward : {data['est_year_reward']}\n"
        content += "--------------------------------------------\n"

        return content
