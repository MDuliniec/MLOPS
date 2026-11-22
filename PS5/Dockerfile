FROM debian:trixie-slim AS build
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG LLAMAFILE_URL=https://huggingface.co/mozilla-ai/llamafile_0.10/resolve/main/Qwen3.5-0.8B-Q8_0.llamafile
ARG LLAMAFILE_SHA256=d97ed2e8729437dd3d044405ba5035f352d253a0987f19e610eb538b0951a805
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -o /model.llamafile "$LLAMAFILE_URL" \
 && echo "$LLAMAFILE_SHA256  /model.llamafile" | sha256sum -c - \
 && chmod 755 /model.llamafile

FROM debian:trixie-slim
RUN useradd --system --no-create-home llamafile \
 && mkdir -p /opt/llamafile \
 && chown llamafile:llamafile /opt/llamafile
COPY --from=build --chown=llamafile:llamafile /model.llamafile /opt/llamafile/model.llamafile
ENV HOME=/opt/llamafile
WORKDIR /opt/llamafile
USER llamafile
EXPOSE 8080
ENTRYPOINT ["sh", "/opt/llamafile/model.llamafile", "--server", "--host", "0.0.0.0"]
CMD ["--port", "8080"]
