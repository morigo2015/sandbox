from multiping import MultiPing

def ping(host,n = 0):
    if(n>0):
        avg = 0
        for i in range (n):
            avg += ping(host)
        avg = avg/n
    # Create a MultiPing object to test hosts / addresses
    mp = MultiPing([host])

    # Send the pings to those addresses
    mp.send()

    # With a 1 second timout, wait for responses (may return sooner if all
    # results are received).
    responses, no_responses = mp.receive(1)


    for addr, rtt in responses.items():
        RTT = rtt


    if no_responses:
        # Sending pings once more, but just to those addresses that have not
        # responded, yet.
        mp.send()
        responses, no_responses = mp.receive(1)
        RTT = -1

    return RTT

import sys

print(ping('www.ua',10))

# print(sys.argv[1],sys.argv[2])
# print(ping(sys.argv[1],int(sys.argv[2])))

