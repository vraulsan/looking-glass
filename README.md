## BGP Looking Glass

This is a tiny and minimalist Python3 looking glass implementation.

Server connects using Paramiko and serves via Flask.

Client is HTML and Javascript is used to make the calls and update the DOM.

`git clone https://github.com/vraulsan/looking-glass.git && cd looking-glass`

Edit `routers.py` to include your routers.
Edit `templates/index.html` to change your *network* dropdown options.

Start with `python app.py`  and go to `localhost:5000`

Example:

[![example](https://i.imgur.com/fg7E8k6.png "example")](https://i.imgur.com/fg7E8k6.png "example")

**Skills**
- bgp
- ping
- traceroute

