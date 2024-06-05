FROM python:3.12
LABEL maintainer="Bernd Doser <bernd.doser@h-its.org>"

RUN pip install spherinator \
    pip cache purge
