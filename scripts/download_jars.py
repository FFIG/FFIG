#!/usr/bin/env python

# Running this script downloads required JAR files from the web.

# FIXME: This script should be replaced by use of a Java package manager.

import os
import requests


def main():
    src_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    download_dir = os.path.join(src_dir, 'build', 'jars')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    google_drive_urls = {
        'hamcrest': "http://central.maven.org/maven2/org/hamcrest/hamcrest-all/1.3/hamcrest-all-1.3.jar",
        'jna': "http://repo1.maven.org/maven2/net/java/dev/jna/jna/4.5.1/jna-4.5.1.jar",
        'junit': "https://repo.maven.apache.org/maven2/junit/junit/4.12/junit-4.12.jar"
    }

    for k, v in google_drive_urls.items():
        print("Downloading {}.jar from {}".format(k, v))
        r = requests.get(v, allow_redirects=True)
        jarfile = os.path.join(download_dir, k+'.jar')
        with open(jarfile, 'wb') as o:
            o.write(r.content)


if __name__ == "__main__":
    main()
