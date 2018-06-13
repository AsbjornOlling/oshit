# Config specs

## Arguments and parameters

### The arguments

In the config segment the user can give some arguments, either when running the program or in the config.ini file.
Some arguments is requred to set either when run or in the config, other arguments is optionally.

The requried arguments is:
- `send`
- `recive`

The optionally arguments is:
- `introducer`
- `file`
- `output`
- `crypto`
- `password`
- `loglevel`
- `localport`

### Run Arguments

When the user run the program they have the ability to give some arguments with the run command.
In the config file argparser is reading the run arguments.

### Config.ini

Theres also a config.ini file, this is used when you have some arguments that you always use.
Run arguments will override the config.ini arguments, but if you always use aes crypto, set crypto = aes in config.ini
and you don't have to type it every time.
Config.ini is read by configparser.

### Fallbacks

If nothing is set in either run arguments or config.ini, we have implemented som fallbacks on some of the arguments.
These are default values the program can fallback on.
Handled by configparser.

## Error handling/User input checks

### File already exists

TODO Inform the user

### Wrong argument input

At the moment argparser is handling error control for wrong input in run arguments.
Theres also a method `check_errors` ATM it's only checking if send and recive is set at the same time or none of the is set.
TODO expand `check_errors` with the rest of the arguments "for config.ini values"
