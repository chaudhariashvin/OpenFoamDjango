FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive

# RUN rm /bin/sh && ln -s /bin/bash /bin/sh
SHELL ["/bin/bash", "-c"] 

# setup timezone
ENV TZ=Europe/Helsinki
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTONUNBUFFERED 1

#
RUN umask 0022

# download openfoam and update repos
RUN apt-get update \
 && apt-get -y install software-properties-common wget python3-pip libgl1-mesa-glx xvfb git

RUN sh -c "wget -O - https://dl.openfoam.org/gpg.key | apt-key add -"
RUN apt-get update
RUN add-apt-repository http://dl.openfoam.org/ubuntu
RUN apt-get update
RUN apt-get -y install openfoam7

RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./requirements.txt /app
ENV PYVISTA_OFF_SCREEN=true
RUN pip install --no-cache-dir --upgrade pip \
  && pip3 install --no-cache-dir -r requirements.txt

RUN sudo apt-get install imagemagick # for making gif images

  # add user "foam" to install hybridPorousInterFoam
RUN useradd --user-group --create-home --shell /bin/bash foam
RUN echo "foam ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER foam
RUN umask 0022
WORKDIR /home/foam
RUN git clone https://github.com/Franjcf/hybridPorousInterFoam.git
WORKDIR hybridPorousInterFoam/OpenFoamV7/
RUN source /opt/openfoam7/etc/bashrc && ./Allwclean && ./Allwmake


USER root
COPY ./OFoamDjango /app/OFoamDjango
#COPY --chown=foam ./OFoamDjango /home/foam/app/OFoamDjango

WORKDIR /app/OFoamDjango

CMD ["./run_server.sh"]

EXPOSE 8000
