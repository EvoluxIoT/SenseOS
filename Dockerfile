# Stage 1: Build stage
FROM ubuntu:22.04 AS builder

# Install build dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates git python3 cmake gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib build-essential

# Clone Pico SDK
RUN git clone --depth 1 https://github.com/raspberrypi/pico-sdk.git /project/pico-sdk/ && cd /project/pico-sdk/ && git submodule update --init

# Copy source files
COPY src/ /project/src/
COPY CMakeLists.txt /project
COPY pico_sdk_import.cmake /project

ENV PICO_SDK_PATH=/project/pico-sdk/

# Build project
WORKDIR /project/build
RUN cmake -DPICO_BOARD=pico_w .. && \
    make

# Stage 2: Final stage
FROM scratch

# Copy built files from the builder stage
COPY --from=builder /project/build/senseos.* /senseos/
WORKDIR /senseos

ENTRYPOINT [ "/bin/sh" ]
