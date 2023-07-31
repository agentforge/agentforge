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

move files into the `/app/collector/hotdir` from the local docker cache volume. JSON files will
be stored from here in the `/app/collector/` dir.

## Pre-processing Guide

TODO: Clean up the JSON files with this handy script

## How to Process Documents

Run the ingestion script from agentforge:

`python3 scripts/ingest.py`

This will take some time. After this complete the data is uploaded into specified vectorstore in your `.env` and can be loaded into an Agent model.

## Backup Computed Vectorstore to Disk

Move the saved vectorstore into the backup folder.

## User Guide for Domain 

Gather high quality, text-book quality source documentation for the domain. This can include well-cited research but should not include experimental or any unproven pre-prints.
