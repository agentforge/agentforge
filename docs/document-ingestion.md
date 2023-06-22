# Document Uploader Documentation

## How to Upload Documents

Install our fork of the opensource collector repository [agentforge/anything-llm](https://github.com/agentforge/anything-llm/tree/master/collector). The easiest way to do this is to simply build and run the [collector.Dockerfile](https://github.com/fragro/agentforge/blob/main/docker/collector.Dockerfile) we created.

```bash
docker build -f docker/collector.Dockerfile -t collector .
docker-compose run -d collector`
```

Access the docker container
```bash
docker exec -it agentforge_collector_1 /bin/bash
cd collector
```

Then you can parse online resources (youtube, websites, substack, etc) by running:

`python3 main.py`

or upload documents (PDF, MD, DOCX) to the hotdir after running:

`python3 watch.py`

move files into the `/app/collector/hotdir` from the local docker cache volume.

## Pre-processing Guide

## How to Process Documents

## Backup Computed Vectorstore to Disk


## User Guide for Domain 

Gather high quality, text-book quality source documentation for the domain. This can include well-cited research but should not include experimental or any unproven pre-prints.
