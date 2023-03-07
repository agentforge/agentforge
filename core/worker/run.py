#!/usr/bin/env python
from redis import Redis
from rq import Worker

# Preload libraries
import core.worker.worker

# Provide the worker with the list of queues (str) to listen to.
w = Worker(['default'], connection=Redis())
w.work()
