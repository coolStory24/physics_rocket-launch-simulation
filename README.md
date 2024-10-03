# Kabal space program

![icon](media/icon.png)

## Demo

![demo](media/demo.gif)

## Run

We recomend to use `virtualenv` to run it:

```bash
python3 -m venv .env
. .env/bin/activate
pip3 install -r requirements.txt
cd simulator
python3 main.py
```

Show help message:

```bash
python3 main.py --help
```

## Building graphics

![graphic](media/speed-vs-time.png)
![graphic](media/rocket-trajectory.png)
![graphic](media/acceleration-vs-time.png)

You can use `-g` or `--build-graphics` option to build graphics when rocket lands.

```bash
python3 main.py --build-graphics
```

**Warning**: building graphics for mars voyage requires 12G ram(TODO: optimise2)

## Configure

Confige file: `simulator/config.py`.

## Hotkeys

- `c` - show/hide entities text markers
- `h` - show/hide gui widgets
- `w`, `a`, `s`, `d` and arrows for navigation
- `+`, `-` for scale
- `mouse` for navigation and scale
- `[`, `]` - to change time acceleration
- `space` - pause
- click on entity to follow it
- `escape` to unfollow entity