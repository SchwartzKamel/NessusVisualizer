# NessusVisualizer

Web application to visualize Nessus scan results in a concise, succinct fashion.

Video Demo - [Here](https://youtu.be/8ZbkkKt7Sns)

## Getting Started

### Prerequisites

This app is modernized to run with:

```
Ubuntu 24.04 (container base)
Python 3.14
uv (dependency lock/install)
Podman (OCI runtime)
```

You will need to setup a [Nessus scanner](https://www.tenable.com/products/nessus), and have at least one scan result.

Redis is optional. If `SESSION_TYPE=redis`, set `REDIS_URI`; otherwise use `SESSION_TYPE=filesystem` for a self-contained local/container runtime.

### Installing

Clone the application, then lock and sync dependencies with `uv`:

```
uv lock
uv sync --frozen
```

Generate `.env`:

```
python setup.py
```

Or create it manually (DEV_DATABASE_URI optional):

```
SECRET_KEY=<RANDOM_HEX_STRING>
FLASK_APP=wsgi.py
PROD_DATABASE_URI=sqlite:////<FULL_PATH_TO_FILE>
DEV_DATABASE_URI=sqlite:////<FULL_PATH_TO_FILE>
SESSION_TYPE=filesystem
# If using redis sessions instead:
# SESSION_TYPE=redis
# REDIS_URI=redis://:[password]@[host_url]:[port]
NESSUS_URL=https://<NESSUS_SCANNER_IP>:8834
NESSUS_USER=<SCANNER_USERNAME>
NESSUS_PASS=<SCANNER_PASSWORD>
NESSUS_VERIFY_SSL=false
SESSION_TYPE=cachelib
SESSION_CACHE_DIR=/tmp/flask_session
```

Run locally:

`uv run python wsgi.py`

Run tests:

`uv run pytest`

### Deployment

Build and run with Podman:

```
podman build -t nessus-visualizer:py314 -f Containerfile .
podman run --rm -d --name nessus-visualizer -p 5000:5000 --env-file .env nessus-visualizer:py314
curl -fsS http://127.0.0.1:5000/login
podman rm -f nessus-visualizer
```

The container runs as a non-root user and serves the app with Waitress on port `5000`.

## Usage

Connect to the server on port 5000 and register your account (this only resides on the local database).

![register](app/static/img/Register.png)

After that you can log in.

![login](app/static/img/Login.png)

Type in the folder ID you want to browse.

![folder](app/static/img/Select_Folder.png)

Type in the scan ID you want to download (currently only one scan result may be accessed at a time, the database is not setup to handle more than that).

![scan](app/static/img/Select_Scan.png)

Once the data has downloaded you can view the scanned hosts by IP and if plugin 45590 (Operating System Common Platform Enumeration) ran it'll be included or notify you that it wasn't in the scan results.

![scan_results](app/static/img/Scan_Results.png)

Plugins are listed in order of severity and are color coded as they would be from the Nessus scanner.

- Critical (Red)
- High (Orange)
- Medium (Yellow)
- Low (Green)
- Informational (Blue)

![scan_results](app/static/img/Crit_High_Med.png)
![scan_results](app/static/img/Med_Low_Info.png)

Plugin "titles" follow the pattern of <PLUGIN_ID> | <PLUGIN_NAME> | <PORT> <CVE_IF_EXISTS> | <CVSS_SCORE>

Each plugin is on a toggle button to reveal more details in the following order:

- Simple description
- Full description
- Plugin output
- A solution to patch the vulnerability if one exists

Additionally the 'Plugin Output' is on a toggle button as some plugins contain significant amounts of data. The background element is a different shade so you can easily distinguish it from the other information.

![scan_results](app/static/img/Plugin_Details.png)

Finally there is a section to view all registered users (more features utilizing this may be built upon, e.g. multiple users each able to analyze different scan results rather than sharing the singular result).

![scan_results](app/static/img/User_Records.png)
