# scrapy

An application framework for crawling websites and extracting structured data (https://docs.scrapy.org/)

## Getting Started

### Prerequisites

- python3.11 (pyenv)
- poetry

### Setup development env and running tests

```shell
poetry install
poetry shell
```

### Creating a project
```shell
# scrapy startproject <project_name> [project_dir]
scrapy startproject databius .
```
### Start the first spider
```shell
scrapy genspider apache.org www.apache.org/logos
```

### Run a spider
```shell
scrapy crawl apache.org
```

