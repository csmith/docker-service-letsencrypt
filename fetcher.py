#!/usr/bin/env python3

import etcd
import time


class Fetcher:

  def __init__(self, host, port, prefix):
    self._client = etcd.Client(host=host, port=port)
    self._prefix = prefix


  def _read(self, key, **kwargs):
    try:
      node = self._client.read(self._prefix + key, **kwargs)
      return node.value if node else None
    except etcd.EtcdKeyNotFound:
      return None


  def _read_recursive(self, key):
    try:
      return self._client.read(self._prefix + key, recursive=True)
    except etcd.EtcdKeyNotFound:
      return None 


  def get_label(self, label):
    node = self._read_recursive('/labels/%s' % label)
    if node:
      return {child.key.split('/')[-1]: child.value for child in node.children}
    else:
      return {}


  def wait_for_update(self):
    original_time = self._read('/_updated')
    new_time = original_time

    while new_time == original_time:
      try:
        new_time = self._read('/_updated', wait=True)
      except etcd.EtcdWatchTimedOut:
        new_time = self._read('/_updated')
      time.sleep(10)

