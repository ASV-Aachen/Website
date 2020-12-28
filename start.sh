# Vorbereitung
# git checkout release
# git pull

#-------------------------
# Bau des WebpageImage
cd Webpage
docker build -t webpageimage:0.1 .

cd ../
# ------------------------
# Docker compose
echo "-----------------------------------------"
cd ./DockerFiles
echo "start von Docker Compose"
docker-compose up -d