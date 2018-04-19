FROM ffig/ffig-base
MAINTAINER FFIG <support@ffig.org>

RUN add-apt-repository ppa:openjdk-r/ppa; apt update; apt install -y openjdk-8-jdk swift

COPY . /home/ffig
RUN find /home/ffig \( -name "*.py" -o -name "*.sh" \) -exec dos2unix {} +
WORKDIR /home/ffig
