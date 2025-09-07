FROM alpine:latest

# Install dependencies, download, build and install MDK in a single layer to minimize space
RUN apk update && apk add --no-cache \
    lftp \
    make \
    glib-dev \
    glib \
    build-base \
    gcc \
    intltool \
    && lftp -c "open ftp://ftp.gnu.org/pub/gnu/mdk; get v1.3.0/mdk-1.3.0.tar.gz" \
    && tar xfvz mdk-1.3.0.tar.gz \
    && cd mdk-1.3.0 \
    && ./configure \
    && make \
    && make install \
    && cd .. \
    && rm -rf mdk-1.3.0 mdk-1.3.0.tar.gz \
    && apk del lftp build-base gcc \
    && rm -rf /var/cache/apk/* /tmp/* /var/tmp/*