# EC2 Deployment Commands

sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker

docker pull your-image
docker run -d -p 80:5000 your-image
