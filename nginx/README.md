# NGINX Configuration Guide (Docker)

This README describes the standard procedure for adding a new NGINX site configuration, enabling it, generating TLS certificates using Certbot with Cloudflare DNS, and reloading NGINX inside a Docker container.

---

## 1. Create a New NGINX Site Configuration

Prepare and add a new `.conf` file in the following directory:

```
nginx/config/sites-available/
```

Example:

```
server {
    listen 443 ssl;
    http2 on;
    server_name example.sinq.cc;

    ssl_certificate     /etc/letsencrypt/live/example.sinq.cc/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.sinq.cc/privkey.pem;

    location / {
        proxy_pass http://example:3000;

        proxy_set_header Host               $host;
        proxy_set_header X-Real-IP          $remote_addr;
        proxy_set_header X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  https;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

```

Make sure the configuration file contains a valid `server` block and points to the correct certificate paths.

---

## 2. Enable the Site Configuration

Create (or update) a symbolic link from `sites-available` to `sites-enabled`:

```
ln -sf ../sites-available/example.conf \
       /opt/docker_volumes/nginx/config/sites-enabled/example.conf
```

This enables the site in NGINX.

If you need to disable the site:

```
unlink /opt/docker_volumes/nginx/config/sites-enabled/example.conf
```
---

## 3. Generate TLS Certificates (Certbot + Cloudflare DNS)

Use Certbot with the Cloudflare DNS plugin to generate or renew certificates:

```
docker compose run --rm certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /cloudflare.ini \
  --dns-cloudflare-propagation-seconds 60 \
  --cert-name domena.sinq.cc \
  -d domena.sinq.cc \
  --agree-tos \
  -m admin@sinq.cc \
  --non-interactive \
  --force-renewal
```

### Notes

* Ensure `/cloudflare.ini` contains a valid Cloudflare API token.
* The token must have permissions to manage DNS records.
* Certificates will be stored in the default Certbot volume (e.g. `certs/live/` which is maped in container to `/etc/letsencrypt/live`).

---

## 4. Test NGINX Configuration

Before reloading NGINX, always validate the configuration:

```
docker exec -it nginx nginx -t
```

If the output reports `syntax is ok` and `test is successful`, you can safely continue.

---

## 5. Reload NGINX Configuration

Apply the new configuration without restarting the container:

```
docker exec -it nginx nginx -s reload
```

NGINX will reload the configuration and start serving the new site immediately.

---

## Summary

1. Add `.conf` file to `sites-available`
2. Symlink it to `sites-enabled`
3. Generate TLS certificates using Certbot
4. Test NGINX configuration
5. Reload NGINX

Following these steps ensures a clean and safe deployment of new NGINX virtual hosts in Docker.
