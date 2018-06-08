
# Development notes

## Transport

### TODO:
x test udp socket by printing incoming data
? implement packet end detection
- implement packet class
- dummynet for testing?

### Flow control

OBS: modulo af SEQ
OBS: add to window on ACK
OBS: when adding to buffer, check if within window
OBS: handle holes in buffer when passing buffer to oSHIT
OBS: better timers in python - callback methods? timers?
OBS: enlargen timeouts when in recovery mode
 
#### Receiving

- Packet arrives
- (optionally) Decrypt payload
? verify checksum
- Check flags

- `if ACK:`
	- Everything up to packet with SEQ is good
	- Delete every packet with no. less than SEQ from `window`

- `if NACK:`
	- Re-transmit packet with SEQ
	- Prepend packet with SEQ to `txqueue`

- `if !(ACK || NACK):`
	- Send ACK
	- Pass payload on to business logic
	- `if SEQ > lastreceived + 1:` 
		- `if len(lastreceived) == 0:`
			- send `NACK`
		- insert in `rxbuffer`
	- `else:`
		- `lastreceived = SEQ`
	- if packet with no. `lastreceived + 1` in `rxbuffer`:
		- pass rxbuffer to businesslogic


#### Sending

Threaded loop:
- pop Packet from `txqueue`
- add timeout time to Packet
- transmit packet
- `for packet in window:`
	- `if currenttime > packet.timeout`:
	- append packet to `txqueue`
- `if len(window) < WSIZE:`
	- construct new packet
	- append to window
	- append to `txqueue`


