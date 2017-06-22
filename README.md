![Build status](https://travis-ci.org/palnet/latlong.svg?branch=master)

## latlong
The `latlong` package allows for encoding and decoding of lat-long coordinates. All points are stored in the `Point` class, which has fields `lat`, `long`, and `num`. `num` is a numerical representation, and is how a single point is able to be represented by just 39 bits while maintaing a maximum error of ~27 metres. `encodeCoords()` takes a space-separated string of lat-long pairs and returns a numerical value of the 39-bit representations concatenated. `decodeCoords()` does just the opposite, taking in the concatenated 39-bit representation and returning an array of `Point` objects.

## Requirements

Bitops requites `type_check` to be installed. This is available at [@jhpratt/type_check.py](https://github.com/jhpratt/type_check.py) or by running `pip install type-check`.
