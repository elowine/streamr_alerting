# Streamr Alerting

Python script that allows you to receive by message the statistics of your nodes income

If you want to support my small participation in the project :)<br>
Feel free to make a donation (DATA, MATIC, ...)<br>
Here is my METAMASK address (Polygon and Ethereum):<br>
0x4ac9F65235C2C60c1F9c11631E72b5Dce84EfEec

Once the repository clonner.<br>
The first step is to copy the <b>src/common/config.sample.py</b> file and rename it to <b>src/common/config.py</b><br>
By default all features are set to False.<br>
If you want to activate any of them you just have to set the value to <b>True</b>

---
How to run in Python (presuming you have changed the config.py)
      
      git clone https://github.com/elowine/streamr_alerting.git
      cd streamr_alerting/
      py -m pip install -r requirements.txt
      python3 src/main.py

---
# List of features (default to false):

### Sum of the node
- Allows to have a message with the sum of the nodes :

      sum_node = False

### Activate recurrent execution
- Allows you to choose if you want the execution to be regular
  <br>If the value is False the script will be executed once. 

      cron_active = False
    If the variable cron_active is set to True. The script will run two features.
<br>One to check the status of the node every hour.
<br>One to get the statistics every monday at 10am.
<br><br>
To modify the recurrence you have to go to the file <b>main.py</b>.
</br>Help with writing crons : https://www.freeformatter.com/cron-expression-generator-quartz.html
<br>And to change the lines:
</br></br>Execution every hour

      scheduler.add_job(exec_check_status_node, trigger='cron', hour="0/1")

    Execution every Monday at 10:00 am
      
      scheduler.add_job(exec_get_info, trigger='cron', hour="10", minute="0", day="2/1")


### Save in file
Allows to have a file with the information in the "save_info_node" directory by default

      
      save_in_file = False*
      dir_save = "save_info_node"*

### Notification


- Discord :

      discord_notif = False
      discord_token = "token_discord"
      discord_channel_id = "channel_id"
- Telegram

      telegram_notif = False
      telegram_token = 'token_telegram'
      telegram_chat_id = 'chat_id'

-----

The rest of the file are variables not to be touched

----

Here is an example of a message:
--------------------------------------------
      --------------------------------------------      
      Streamr Node Infos
      Elowine
      Node Status : online
      Total Stacked : 3147.88 | 82.0$
      Received Rewards : 0 | 0.0$
      Accumulated Rewards : 39.71 | 1.03$
      Percent Rewards : 3.74%:
      
      APR : 48,1%
      APY : 60,25%
      Estimated
      Month Reward : 121.12
      Year Reward : 1451.4
      --------------------------------------------
