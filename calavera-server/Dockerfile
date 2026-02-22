FROM ubuntu:latest
WORKDIR /app
COPY . /app

ARG VERSION=0.0.1
ENV VERSION=${VERSION}

RUN chmod +x ./calavera-server-v${VERSION}/calavera-server-v${VERSION}.sh \
    && chmod +x ./calavera-server-v${VERSION}/calavera-server-v${VERSION}.x86_64

EXPOSE 9080
CMD ["sh", "-c", "./calavera-server-v${VERSION}/calavera-server-v${VERSION}.sh --headless"]
