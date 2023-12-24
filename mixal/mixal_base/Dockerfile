FROM alpine:latest

RUN apk update
RUN apk add lftp
RUN apk add make
RUN apk add glib-dev
RUN apk add glib
RUN apk add build-base
RUN apk add gcc
RUN apk add intltool

RUN lftp -c "open ftp://ftp.gnu.org/pub/gnu/mdk; get v1.3.0/mdk-1.3.0.tar.gz"
RUN tar xfvz mdk-1.3.0.tar.gz
RUN mdk-1.3.0/configure
RUN cd mdk-1.3.0
RUN make
RUN make install