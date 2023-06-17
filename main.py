import sys
from routersPoller import main

if len(sys.argv) != 3:
    print("Usage: python3 main.py <community> <ip>")
    sys.exit(1)

community = sys.argv[1]
ip = sys.argv[2]

main(community, ip)