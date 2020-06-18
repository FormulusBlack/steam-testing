# Steam Testing on Forsa
Resources for reproducing the testing done on BitMarker effectiveness with regards to Steam games.


## Prerequisites
Before getting started, get a free trial of Forsa (here)[https://www.formulusblack.com/see-it-work/]. You will also need to install Forsa on your preferred OS (we used Ubuntu 18.04). <br/>


## Testing
1. Create a LEM:
```
forsa --user <username> --psswd <password> lem create --name STEAM_TESTING --size $(bc <<< "256 * 1024")
```

1. Create a VM (for our testing we used 73G RAM and 8 CPUs, but that shouldn't affect deduplication results):
```
forsa --user <username> --psswd <password> vm create --name Steam_Ubuntu --cpu <cpu> --ram <ram>
```

1. Attach the LEM to the VM:
```
forsa --user <username> --psswd <password> vm attach --device-name STEAM_TESTING --name Steam_Ubuntu --type lem
```

1. Install Ubuntu desktop on the VM. After installing Steam, take baseline disk usage information with `df`.

1. Install the games detailed in [`game-data.csv`](data/game-data.csv)
