# hypersimplified-audiobook

Place the audiobook you want to read in a file called 'audiobook.mp3' in the root directory.

Just run it as an uvicorn app, e.g.

```
uvicorn app.main:app --reload --port 8001
```

It is suggested to run it behind a reverse proxy to handle https.
