FROM ffig/ffig-base
MAINTAINER FFIG <support@ffig.org>

COPY . /home/ffig
RUN find /home/ffig -type f -exec dos2unix {} \;
WORKDIR /home/ffig
