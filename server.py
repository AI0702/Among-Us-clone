import socket
import asyncore
import random
import pickle
import time

BUFFERSIZE = 8192

print("Server Address: " + socket.gethostbyname(socket.gethostname()))

outgoing = []

class Minion:
  def __init__(self, player_id):
    self.x = 50
    self.y = 50
    self.sync_img = None
    self.sync_img_index = None
    self.left_img_index = 0
    self.right_img_index = 0
    self.up_img_index = 0
    self.down_img_index = 0
    self.alive_status = True
    self.player_id = player_id
    self.player_colour = None
    self.tasks_completed = 0
    self.sabotagelights_sync = 0
    self.sabotagereactor_sync = 0
    self.victim_id = 0
    self.imposter = False
    self.emergency_sync = 0
    self.voted = None
    self.got_votes = 0
    self.emergency_meeting_img_sync = None
    self.emergency_meeting_img_sync_report = None
    self.victim_id_report = 0
    self.got_reported = False
    self.eject_sync = False
    self.eject_img = None

minionmap = {}

def updateWorld(message):
  arr = pickle.loads(message)
  print(str(arr))
  player_id = arr[1]
  x = arr[2]
  y = arr[3]
  alive_status = arr[4]
  sync_img = arr[5]
  sync_img_index = arr[6]
  left_img_index = arr[7]
  right_img_index = arr[8]
  up_img_index = arr[9]
  down_img_index = arr[10]
  player_colour = arr[11]
  tasks_completed = arr[12]
  sabotagelights_sync = arr[13]
  sabotagereactor_sync = arr[14]
  victim_id = arr[15]
  imposter = arr[16]
  emergency_sync = arr[17]
  voted = arr[18]
  got_votes = arr[19]
  emergency_meeting_img_sync = arr[20]
  emergency_meeting_img_sync_report = arr[21]
  victim_id_report = arr[22]
  got_reported = arr[23]
  eject_sync = arr[24]
  eject_img = arr[25]

  if player_id == 0: return

  minionmap[player_id].x = x
  minionmap[player_id].y = y
  minionmap[player_id].alive_status = alive_status
  minionmap[player_id].sync_img = sync_img
  minionmap[player_id].sync_img_index = sync_img_index
  minionmap[player_id].left_img_index = left_img_index
  minionmap[player_id].right_img_index = right_img_index
  minionmap[player_id].up_img_index = up_img_index
  minionmap[player_id].down_img_index = down_img_index
  minionmap[player_id].player_colour = player_colour
  minionmap[player_id].tasks_completed = tasks_completed
  minionmap[player_id].sabotagelights_sync = sabotagelights_sync
  minionmap[player_id].sabotagereactor_sync = sabotagereactor_sync
  minionmap[player_id].victim_id = victim_id
  minionmap[player_id].imposter = imposter
  minionmap[player_id].emergency_sync = emergency_sync
  minionmap[player_id].voted = voted
  minionmap[player_id].got_votes = got_votes
  minionmap[player_id].emergency_meeting_img_sync = emergency_meeting_img_sync
  minionmap[player_id].emergency_meeting_img_sync_report = emergency_meeting_img_sync_report
  minionmap[player_id].victim_id_report = victim_id_report
  minionmap[player_id].got_reported = got_reported
  minionmap[player_id].eject_sync = eject_sync
  minionmap[player_id].eject_img = eject_img

  remove = []

  for i in outgoing:
    update = ['player locations']

    for key, value in minionmap.items():
      update.append([value.player_id, value.x, value.y, value.alive_status, value.sync_img, value.sync_img_index, value.left_img_index, value.right_img_index, value.up_img_index, value.down_img_index, value.player_colour, value.tasks_completed, value.sabotagelights_sync, value.sabotagereactor_sync, value.victim_id, value.imposter, value.emergency_sync, value.voted, value.got_votes, value.emergency_meeting_img_sync, value.emergency_meeting_img_sync_report, value.victim_id_report, value.got_reported, value.eject_sync, value.eject_img])
    
    try:
      i.send(pickle.dumps(update))
    except Exception:
      remove.append(i)
      continue
    
    print ('sent update data')

    for r in remove:
      outgoing.remove(r)

class MainServer(asyncore.dispatcher):
  def __init__(self, port):
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(('', port))
    self.listen(10)
  def handle_accept(self):
    conn, addr = self.accept()
    print ('Connection address:' + addr[0] + " " + str(addr[1]))
    outgoing.append(conn)
    player_id = random.randint(1000, 1000000)
    playerminion = Minion(player_id)
    minionmap[player_id] = playerminion
    conn.send(pickle.dumps(['id update', player_id]))
    SecondaryServer(conn)

class SecondaryServer(asyncore.dispatcher_with_send):
  def handle_read(self):
    recievedData = self.recv(BUFFERSIZE)
    if recievedData:
      updateWorld(recievedData)
    else: self.close()

MainServer(4321)
asyncore.loop()