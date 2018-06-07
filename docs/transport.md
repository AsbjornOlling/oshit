# Transport specs

## oSHIT Transport Header

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
      | |        8 bits         |1 bit|1 bit|1 bit|       5 bit       | |
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

### Flags:

#### ACK
If the NACK is set, the sequence no. represents the next packet that can be received.
That is, if ACK arrives with sequence no. 4, we know that packets 1, 2, and 3 have all arrived.
When an ACK 4 is received, the next packet to be sent should be the packet with sequence no. 4.

### NACK
If the NACK flag is set, the sequence no. represents the number of the expected packet. 
When NACK 4 is received, the next packet to be sent should be packet with sequence no. 4.

#### EOF
The EOF flag is set, when the packet is the last packet containing file data.
The receiving client will detect this, and inform the user that the transfer is complete.


## Handshake
The purpose of the handshake is primarily to exchange keys.

```asciiflow

                       Sender                               Receiver
                         +                                     +
                         |  Crypto setting, file checksum      |
                         +------------------------------------>|
                         |                                     | gen_rsa_key()
                         |                    Public RSA key   |
                         |<------------------------------------+
           gen_aes_key() |                                     |
                         | RSA-encrypted AES key               |
                         +------------------------------------>|
                         |                                     |
                         |       AES-encrypted data            |
                         +--------------------------->         |
                         |                                     |
                         |  AES-encrypted data                 |
                         +----------------------->             |
                         |                                     |
                         |     ...                             |
                         +------------------>                  |
                         |                                     |
                         |                                     |
                         |                                     |
                         v                                     v
```



## Flow Control

- **Selective reject** flowcontrol
- **Window size:** 128 (8 bits in header)

### Buffers / lists

For sending
- `window` - A list of packets ready to send
- `txqueue` - A list of packets to be sent

For receiving
- `rxbuffer` - A buffer for packets arriving out of sequence
- `lastreceived` - SEQ no of last valid received packet
