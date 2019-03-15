# from empath import Empath
#
# lexicon = Empath()
#
# print(lexicon.analyze("I receive messages from people I don't know weekly telling me of her condition. She is scamming people of money and they are turning to me for advice.It is taking a severe toll on my mental health at this point, I am struggling with anxiety and slipping into a depression again. It takes a toll having literally no family and trying to put yourself through school, work two jobs and have a stable normal life at 23."
#                 , normalize=True))
# print(lexicon.create_category("games", ["games"], model="reddit"))
import time
from random import randint
from threading import Thread

from queue import Queue

from core.logger import Logger

log = Logger().setLogger("[Gather Task]")

def do_stuff(q):
    while True:
        log.d(str(q.get()))
        time.sleep(randint(0, 9))
        q.task_done()


q = Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
    worker = Thread(name='queue-'+str(i),target=do_stuff, args=(q,))
    worker.setDaemon(True)
    worker.start()

for x in range(100):
    q.put(x)

q.join()
