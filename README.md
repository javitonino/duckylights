# duckylights

This is a project to control a Ducky RGB keyboard from Linux. It aims to replicate the funcionality of the official Windows-only application, although that goal is still very far away.

## Features

For now, only setting a custom color mode (individual color per key) is supported. 

Missing (amongst others): setting non-custom modes, saving & loading profiles.

## Usage

To set a random color for each key (there are also some more interesting examples in the `examples` directory):

```python
import duckylights
import random

def random_color():
  return hex(random.randint(0, 256**3 - 1))[2:].rjust(6, '0')

with duckylights.keyboard() as dev, dev.programming() as ducky:
  colors = [random_color() for i in range(6 * 22)]
  ducky.custom_mode(colors)
  input()
```

Common issues:
- You may need to adjust the device ID that `duckylights` looks for. It defaults to `04d9:0348` (Ducky One 2 RGB), but you can adjust it by passing the `vendor` and `product` options like:
  `with duckylights.keyboard(duckylights.device_path(vendor=0x04d9, product=0x0348)) as dev, dev.programming() as ducky:`

- You may need to give permissions to your user to access the `hidraw` devices. The quick and dirty way is to just give read/write permissions to your user over the affected hidraw device. The better way is to use an udev rule to do so in a more permanent way.
