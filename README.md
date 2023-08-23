# pyddns
A simple python script to update DNS records on Cloudflare

## Usage
1. Install dependencies
```bash
pip install -r requirements.txt
```
2. Make a file called `.env` in the project root directory and fill in the required variables. Refer to `.env.example` for an example.
3. Run the script
```bash
python pyddns.py
```

## TODO
- Add support for IPv6
- Add socks proxy support
- Report event messages to webhooks
