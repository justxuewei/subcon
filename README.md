# SubCon

Project SubCon is a configuration converter for Surge and ShadowSocks, for now it has ability to convert Surge to ShadowSocks Subscription.

# Deployment

by Docker

```bash
docker run -d \
  --name subcon \
  -p 10000:8080 \
  --restart unless-stopped \
  xavierniu/subcon
```

# API

- [GET] `http://localhost:10000/surge2ss?url=<URL>`
    - url: your Surge subscription url