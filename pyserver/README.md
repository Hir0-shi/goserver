# pyserver

A Python script that analyzes the character and word frequency of a text file, with Docker support.

## Running Locally

### Setup

```bash
pyenv install 3.14.7
pyenv virtualenv 3.14.7 pyserver
pyenv local pyserver

mkdir books
wget -O books/frankenstein.txt https://raw.githubusercontent.com/asweigart/codebreaker/master/frankenstein.txt
```

### Run

```bash
python3 main.py
```

### Output

```
--- Begin report of books/frankenstein.txt ---
77986 words found in the document

The 'e' character was found 46043 times
The 't' character was found 30365 times
The 'a' character was found 26743 times
The 'o' character was found 25225 times
The 'i' character was found 24613 times
The 'n' character was found 24367 times
The 's' character was found 21155 times
The 'r' character was found 20818 times
The 'h' character was found 19725 times
The 'd' character was found 16863 times
The 'l' character was found 12739 times
The 'm' character was found 10604 times
The 'u' character was found 10407 times
The 'c' character was found 9243 times
The 'f' character was found 8731 times
The 'y' character was found 7914 times
The 'w' character was found 7638 times
The 'p' character was found 6121 times
The 'g' character was found 5974 times
The 'b' character was found 5026 times
The 'v' character was found 3833 times
The 'k' character was found 1755 times
The 'x' character was found 677 times
The 'j' character was found 504 times
The 'q' character was found 324 times
The 'z' character was found 243 times
--- End report ---
```

## Docker

### Dockerfile.py

Uses Alpine Linux with Python3 installed via apk, runs as a non-root user (`pyserver`), sets `WORKDIR /srv` so the relative path `books/frankenstein.txt` resolves correctly, and copies code + data into the container.

```dockerfile
FROM alpine:latest

RUN apk add --no-cache python3

RUN adduser -D -h /srv pyserver

WORKDIR /srv

COPY --chown=pyserver:pyserver main.py .
COPY --chown=pyserver:pyserver books/ .

USER pyserver

CMD ["python3", "main.py"]
```

| Directive | Why |
|-----------|-----|
| `--chown=pyserver:pyserver` | Sets ownership during `COPY`, avoiding a separate `RUN chown -R ...` layer that duplicates file data |
| `WORKDIR /srv` before `COPY` | Allows relative paths (`.`) in `COPY`, keeping the file cleaner |
| `USER pyserver` | Drops root privileges — the script never runs as root |

### Build and Run

```bash
docker build -t bookbot -f Dockerfile.py .
docker run bookbot
```

### Output

Same as local run above — full character frequency report for Frankenstein.

### Verify Non-Root User

```bash
docker exec -it <container_id> sh
/srv $ id
uid=1000(pyserver) gid=1000(pyserver) groups=1000(pyserver)
```

## How It Works

| Function                          | Purpose                                                     |
|-----------------------------------|-------------------------------------------------------------|
| `get_book_text(path)`             | Reads the entire book file                                  |
| `get_num_words(text)`             | Counts words by splitting on whitespace                     |
| `get_chars_dict(text)`            | Builds a frequency map of each character (case-insensitive) |
| `chars_dict_to_sorted_list(dict)` | Converts the frequency map to a sorted list                 |
| `sort_on(dict)`                   | Sort key — sorts by character count descending              |
| `main()`                          | Orchestrates everything and prints the report               |
