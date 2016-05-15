#!/usr/bin/env python3

import etcd


class Fetcher:

  def __init__(self, host, port, prefix):
    self._client = etcd.Client(host=host, port=port)
    self._prefix = prefix


  def _read_recursive(self, key):
    try:
      return self._client.read(self._prefix + key, recursive=True)
    except etcd.EtcdKeyNotFound:
      return None 


  def get_label(self, label):
    node = self._read_recursive('/labels/%s' % label)
    return {child.key.split('/')[-1]: child.value for child in node.children}

