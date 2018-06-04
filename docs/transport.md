# Transport specs

## oSHIT Transport protocol

```asciiflow
        +-------------------------------------------------------------+
        |                           20 bytes                          |
        |-------------------------------------------------------------|
        |                             IPv4                            |
        +-------------------------------------------------------------+

        +-------------------------------------------------------------+
        |                            8 bytes                          |
        |-------------------------------------------------------------|
        |                              UDP                            |
        +-------------------------------------------------------------+

																    oSHIT
      +-----------------------------------------------------------------+
      |                                                                 |
      |                          oSHIT Header                           |
      | +-----------------------+-----+-----+-----+-------------------+ |
      | |        8 bits         |1 bit|1 bit|1 bit|      5 bytes      | |
      | |-----------------------|-----|-----|-----|-------------------| |
      | |     Sequence no.      | ACK | NACK| EOF |      Reserved     | |
      | +-----------------------+-----+-----+-----+-------------------+ |
      |                                                                 |
      | +-------------------------------------------------------------+ |
      | |                       Max 1456 bytes                        | |
      | |-------------------------------------------------------------| |
      | |                       oSHIT payload                         | |
      | +-------------------------------------------------------------+ |
      |                                                                 |
      +-----------------------------------------------------------------+
```

## Flow Control

- **Selective reject** flowcontrol
- **Window size:** 128 (8 bits in header)
