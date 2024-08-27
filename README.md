# tile-ops
`tile-ops` is a CLI tool to calculate the latency of HTTP requests.

## Installation
To install the required dependencies, use `pip` to install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Run
```bash
python tile_ops/calculate_latency.py https://staging.api.xclaim.xcover.com/auth/jwt/token/programmatic-access --header "Authorization: "
```

