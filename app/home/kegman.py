#!/usr/bin/env python
import os
import sys
import json
from setproctitle import setproctitle
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), os.path.expanduser('~/raspilot')))
from cereal import log, car
from common.params import Params
from common.profiler import Profiler
from selfdrive.kegman_conf import kegman_conf

setproctitle('webUI')

frame_count = 0
params = Params()
profiler = Profiler(False, 'dashboard')
user_id = str(params.get("PandaDongleId", True))
user_id = user_id.replace("'","")

try:
  car_params = car.CarParams.from_bytes(params.get('CarParams', True))
  kegman = kegman_conf(car_params)
  kegman_valid = ('tuneRev' in kegman.conf)
except:
  print("kegman error")
  kegman_valid = False
  do_influx = False

