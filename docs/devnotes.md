
# Development notes

## Transport

### TODO:
- implement threaded sending and receiving
- research weather
- implement packet class
- figure out packet timers

### Flow control

OBS: modulo af SEQ
OBS: add new packets to window on ACK
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


#### Threading

Only the order they're passed to Transport needs to be sequential
Transport will always take the first element from a list
So the list in Incoming needs to be appended sequentially

Example:
- rxthread receives packet
- rxthread appends to rxqueue
- rxthread starts packethandler thread
- packethandler acquires rxqueue lock
- packethandler does its shit
	- maybe passes the packet on to application layer
- packethandler releases the rxqueue lock

#### Transport architecture

Transport: 
	- sending window
	- seq number tracking
	- works with complete Packet objects
	In:
		- reads incoming data
		- makes packet object
			- decryption
			- read seq number
			- read flags
			- read payload
		? passes it up to Transport SOMEHOW
	Out:
		- txqueue
		- sends packet object
			- 

InPacket(data)
	- if config['crypto']:
		self.crypto.decrypt()

OutPacket(data)
	- created in App layer
