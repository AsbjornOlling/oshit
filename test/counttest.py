
txmin = 0
txmax = 3

openwsize = 0
i = txmin
while i != txmax:
    i = (i + 1) % 256
    openwsize += 1

print(openwsize)
