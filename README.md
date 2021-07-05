# CS232-Webdemo

## Install packages and dependencies and activate environment:
```
pip3 install -r requirements.txt
```
## Run demo
```
python3 main.py
```

## Docker
### Build from dockerfile:
- If you want to build docker image from ```dockerfile```, just run: ```docker build -t <your-docker-name>:<tag> .```
### Run from exist docker image:
```
docker pull nguyenquang7501/web-demo-cs232:latest
docker run -it --name web-demo-cs232 -d -p 8000:8000 nguyenquang7501/web-demo-cs232:latest
```
