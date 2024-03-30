import selectors
import sys

def on_read(selector, key):
    data = key.fileobj.read()
    print(data)

selector = selectors.DefaultSelector()
selector.register(sys.stdin, selectors.EVENT_READ, on_read)

while True:
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key)