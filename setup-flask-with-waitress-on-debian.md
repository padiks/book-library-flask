# Setting Up Flask App with Waitress on Debian

This guide explains how to run your existing Flask application as a service using Waitress on Debian.

---

## 1. Update and Install System Packages

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git
```

* `python3` – Python interpreter
* `python3-pip` – Python package manager
* `python3-venv` – For creating virtual environments
* `git` – Optional, if you need to clone repos

---

## 2. Copy Your Flask App to Debian

Assuming you already copied your app to `/home/user/Public/web/flaskapp`:

```bash
cd /home/user/Public/web
ls
# Should show flaskapp/
```

---

## 3. Create a Python Virtual Environment

Inside your Flask app folder:

```bash
cd flaskapp
python3 -m venv venv
source venv/bin/activate
```

* `venv` folder contains isolated Python packages
* `source venv/bin/activate` activates the environment

---

## 4. Install Required Python Packages

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install flask waitress markdown jinja2 markupsafe
```

* `flask` – Core web framework
* `waitress` – Production WSGI server
* `markdown` – For rendering Markdown files
* `jinja2` – Template engine

If you have a `requirements.txt` in your app:

```bash
pip install -r requirements.txt
```

---

## 5. Modify Flask App for Waitress

Replace the last part:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4040, debug=True)
```

with Waitress:

```python
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=4040)
```

> This allows the app to run via Waitress, which is production-ready.

---

## 6. Test Running the App

Inside the virtual environment:

```bash
# python3 app.py or
python3 -m waitress --listen=0.0.0.0:4040 app:app
```

* Replace `tutorial.py` with your main Flask file if named differently.
* Visit `http://<your-debian-ip>:4040` to check it works.

---

## 7. Create a Systemd Service

To run automatically on boot:

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

Add the following:

```ini
[Unit]
Description=Flask Book Library
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/Public/web/flaskapp
Environment="PATH=/home/user/Public/web/flaskapp/venv/bin"
ExecStart=/home/user/Public/web/flaskapp/venv/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

* Replace `user` with your Debian username.
* `app.py` → your Flask app main script.

---

## 8. Enable and Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

Check status:

```bash
sudo systemctl status flaskapp
```

* Should show `active (running)` if everything works.

---

## 9. Access the App

Open a browser and go to:

```
http://<your-debian-ip>:4040
```

* Should show your Flask Book Library.
* Service will restart automatically on reboot.

---

## 10. Useful Systemd Commands

```bash
sudo systemctl stop flaskapp
sudo systemctl restart flaskapp
sudo journalctl -u flaskapp -f   # View live logs
```

---

✅ Your Flask + Waitress app is now running on Debian as a persistent service!
