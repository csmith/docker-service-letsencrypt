# Automatic Let's Encrypt certificate generator 

This connects my [docker-service-reporter](https://github.com/csmith/docker-service-reporter/)
and [docker-letsencrypt-lexicon](https://github.com/csmith/docker-letsencrypt-lexicon)
containers together. Between the three, they create a pipeline
to automatically obtain Let's Encrypt certificates for
containers as they're added or modified. 

## How? 

The `service-reporter` container populates `etcd` with details about
known containers.

This container monitors `etcd` for a label specifying vhosts, and builds a
list of domain names and alternatives that need certificates.

Finally, `letsencrypt-lexicon` takes in the list of domain names and
obtains the actual certificates for them.

## Usage

Create a named volume to use for the domains list and resulting
certificates:

```bash
docker volume create --name letsencrypt-data
```

You should mount this volume in the `letsencrypt-lexicon` container at
`/letsencrypt`.

Then run this container. It takes the same arguments as `service-reporter`:

```
  --etcd-host (default: etcd) hostname where ectd is running
  --etcd-port (default: 2379) port to connect to ectd on
  --etcd-prefix (default: /docker) prefix to read keys from
  --name (default: unknown) name of the host running docker
```

So running the container will look something like:

```bash
docker run -d \
  --name service-letsencrypt \
  --restart always \
  -v letsencrypt-data:/letsencrypt \
  csmith/service-letsencrypt:latest \
  --<arguments>
```

## Current known issues

* **The container performs one update and then exits.** It does not yet monitor
  for changes to etcd.

