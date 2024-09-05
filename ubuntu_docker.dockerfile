FROM ubuntu:18.04
LABEL key="Georg Methner"

# Update package list and install dependencies
RUN apt-get update && \
    apt-get -y install \
        python3 \
        python3-pip \
        python3-wxgtk4.0 \
        libgtk-3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install wxPython
RUN pip3 install -U \
    -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 \
    wxPython && \
    echo 'pip3 install wxPython succeeded'

# Install geojson
RUN pip3 install geojson && \
    echo 'pip3 install geojson succeeded'