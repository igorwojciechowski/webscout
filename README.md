# webscout

```
 __          __  _     _____                 _
 \ \        / / | |   / ____|               | |
  \ \  /\  / /__| |__| (___   ___ ___  _   _| |_
   \ \/  \/ / _ \ '_  \___ \ / __/ _ \| | | | __|
    \  /\  /  __/ |_) |___) | (_| (_) | |_| | |_
     \/  \/ \___|_.__/_____/ \___\___/ \__,_|\__|
    version: 0.1

```

A CLI tool for web application reconaissance.

## Features

- Probing URLs and outputting response status code
- Saving HTTP response to `*.http` files
- Taking screenshots of visited URLs
- Generating `html` report with screenshots and headers from the response

## Requirements

- Python 3.5+
- PIP

## Setup

1. Clone repository
    ```bash
    $ git clone https://github.com/igorwojciechowski/webscout
    ```
2. Go to repository and install webscout package
    ```bash
    $ cd webscout/
    $ pip install .
    ```

![Webscout Setup](docs/img/setup.gif)

## Usage

```
usage: webscout [-h] [-o OUTPUT] [-th THREADS] [-to TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory for report
  -th THREADS, --threads THREADS
                        Number of threads
  -to TIMEOUT, --timeout TIMEOUT
                        Requests/Screenshots timeout in seconds
```

To run Webscout, simply provide a list of URLs as a stdin to `webscout`

```bash
$ cat urls.txt | webscout
```


![Webscout Usage](docs/img/usage.gif)

