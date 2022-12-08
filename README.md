# Advent of Code 2022

## Creating days

Have added a setup script that creates empty `script.py`, `example.txt` and `input.txt` files.

Run with `./setup.sh day_<number>`

**TODO:** Look into automatcially populating the input file?

## Running

As I have zero idea what I'm doing with python modules, to run this you have to do something like `py -m src.day_01.script`, else it won't find the utils module.

Have added a script file that does the above so I don't have to type the whole damn line out.

Run with `./run-day.sh day_<number>`

## Notes

Remember to include the `..` with `..utils.input`, which doesn't throw an error if ignored, but won't work.

## Conclusion

Damn I'm bad at python.
