# Aqua Monitor

Just as the title said, it's Aqua's monitor, that keep monitoring Hololive + Holostars stream and records the message that contain a certain keyword from it

Basic code is from [matsuri monitor](https://github.com/lyger/matsuri-monitor) also using [dragonjet's](https://twitter.com/dragonjetmkii) JSON endpoints from his [Hololive Tools](https://hololive.jetri.co/#/) to monitor live stream.

Named "Aqua Monitor" because... it's Aqua's monitor as well. how to use it, basically modifying the `groupers.json` file. (for more information see Matsuri-monitor github)

```bash
$ docker build -t aqua-monitor .
$ docker run -d \
    --name aqua-monitor \
    -p 127.0.0.1:$LOCAL_PORT:8080/tcp \
    --mount type=bind,target=/app/archives,source=$LOCAL_ARCHIVES_DIR \
    aqua-monitor --
```

Mount for where you save the file (the directory)

`$LOCAL_PORT` needed to be higher than 1024
