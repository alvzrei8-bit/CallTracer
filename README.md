# CallTracer
CallTracer — a python tool that spies on obfuscated scripts to see what function they try to call!

# CallTracer

A lightweight Python runtime function tracer that shows function calls, arguments, return values, and exceptions while a Python script is running.

## Features

- 🔎 Traces function calls
- 📥 Shows function arguments
- 📤 Shows return values
- ⚠️ Detects runtime exceptions
- 🧩 Tracks dynamically executed code from `exec()`
- 🧵 Supports threaded code
- 🪶 Lightweight and dependency-free
- 📟 Outputs everything directly to the terminal
- 🚫 Filters out most Python internals and tracer noise

## Usage

```bash
python3 calltracer.py <input.py>

Example:

python3 calltracer.py target.py
```
```bash
Example

Given:

import base64

x = "..."

exec(base64.b64decode(x))

CallTracer can reveal the runtime execution flow:

[13:35:21] START /data/data/com.termux/files/home/target.py
[13:35:21] CALL <module>() [target.py:0]
[13:35:21]   CALL <module>() [<string>:0]
[13:35:21]     CALL main() [<string>:7]
[13:35:21]       CALL hello(name='Yogurt') [<string>:1]
[13:35:21]       RETURN hello -> 'hello, ChatGPT!'
[13:35:21]       CALL add(a=5, b=7) [<string>:4]
[13:35:21]       RETURN add -> 12
[13:35:21]     RETURN main -> ('hello, Yogurt!', 12)
hello, Yogurt!
12
[13:35:21]   RETURN <module> -> None
[13:35:21] RETURN <module> -> None
[13:35:21] DONE
```

What It Traces

CallTracer uses Python's runtime tracing system to observe:

Function calls

Function arguments

Return values

Exceptions

Dynamically executed Python code

Thread execution


For example:

def hello(name):
    return f"Hello {name}"

def add(a, b):
    return a + b

def main():
    x = hello("World")
    y = add(5, 7)
    return x, y

print(main())

Produces a trace similar to:

CALL main()
  CALL hello(name='World')
  RETURN hello -> 'Hello World'
  CALL add(a=5, b=7)
  RETURN add -> 12
RETURN main -> ('Hello World', 12)

Why?

CallTracer is useful for:

Debugging Python programs

Understanding unfamiliar Python code

Analyzing obfuscated scripts

Inspecting exec() payloads

Studying runtime behavior

Reverse engineering Python applications

Learning how Python code executes


How It Works

CallTracer uses:

sys.settrace()

and:

threading.settrace()

to receive runtime events from Python.

It then filters the events and displays useful execution information in the terminal.

Limitations

CallTracer is a runtime tracer, not a full sandbox.

It does not guarantee that a program is safe to execute.

A Python program can perform actions such as:

File operations

Network requests

Process execution

Environment access

Native extension calls


Use it only with code you understand or in an appropriately isolated environment.

Requirements

Python 3.x

No external dependencies


Related Tool

NetTracer — runtime network/HTTP activity tracer.

NetTracer   → Network activity
CallTracer  → Function execution

# License

MIT License
