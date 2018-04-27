from evm_gm_tool.env import *
bind = "{}:{}".format(ENV_SERVER_IP, ENV_SERVER_PORT)
logfile = "/home/manhnd/PycharmProjects/GR/evm_gm_tool/gunicorn.log"
workers = 3