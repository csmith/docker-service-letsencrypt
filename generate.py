#!/usr/bin/env python3

from collections import defaultdict
from fetcher import Fetcher
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name of the docker host to request certificates for', default='unknown')
parser.add_argument('--etcd-port', type=int, help='Port to connect to etcd on', default=2379)
parser.add_argument('--etcd-host', help='Host to connect to etcd on', default='etcd')
parser.add_argument('--etcd-prefix', help='Prefix to use when retrieving keys from etcd', default='/docker')
args = parser.parse_args()

fetcher = Fetcher(args.etcd_host, args.etcd_port, args.etcd_prefix)

while True:
  domains = defaultdict(set)
  for container, values in fetcher.get_label('com.chameth.vhost').items():
    parts = values.split(',')
    domains[parts[0].strip()] |= set([] if len(parts) == 1 else parts[1:])

  with open('/letsencrypt/domains.txt.new', 'w') as f:
    print('Writing domains.txt...')
    for domain, alts in domains.items():
      print('%s [%s]' % (domain, ', '.join(alts)))
      f.write(domain)
      if len(alts):
        f.write(' ' + ' ' .join(alts))
      f.write('\n')

  try:
    os.remove('/letsencrypt/domains.txt')
  except OSError:
    pass

  os.rename('/letsencrypt/domains.txt.new', '/letsencrypt/domains.txt')
  print('Done writing domains.txt.', flush=True)

  fetcher.wait_for_update()

