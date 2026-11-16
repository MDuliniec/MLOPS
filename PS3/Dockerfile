FROM debian:trixie-slim AS build
ARG LLAMAFILE_URL
ARG LLAMAFILE_SHA256
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL -o /model.llamafile "$LLAMAFILE_URL" \
 && echo "$LLAMAFILE_SHA256  /model.llamafile" | sha256sum -c - \
 && chmod +x /model.llamafile

FROM debian:trixie-slim
RUN useradd --system --create-home llamafile
COPY --from=build /model.llamafile /opt/llamafile/model.llamafile
USER llamafile
EXPOSE 8080
ENTRYPOINT ["sh", "/opt/llamafile/model.llamafile", "--server", "--nobrowser", "--host", "0.0.0.0"]
CMD ["--port", "8080"]
