# Steam Testing on Forsa
Resources for reproducing the testing done on BitMarker effectiveness with regards to Steam games.


## Prerequisites
Before getting started, get a free trial of Forsa (here)[https://www.formulusblack.com/see-it-work/]. You will also need to install Forsa on your preferred OS (we used Ubuntu 18.04). <br/>


## Testing
1. Create a LEM (Logical Extension of Memory):
```
forsa --user <username> --psswd <password> lem create --name STEAM_TESTING --size $(bc <<< "256 * 1024")
```

2. Create a VM (for our testing we used 73G RAM and 8 CPUs, but that shouldn't affect deduplication results):
```
forsa --user <username> --psswd <password> vm create --name Steam_Ubuntu --cpu <cpu> --ram <ram>
```

3. Attach the LEM to the VM:
```
forsa --user <username> --psswd <password> vm attach --device-name STEAM_TESTING --name Steam_Ubuntu --type lem
```

4. Install Ubuntu desktop on the VM. After installing Steam, take baseline disk usage information with `df`.

5. Identify the amplification factor of the LEM with:
```
forsa rtm ls
```

6. Install the games detailed in [`game-data.csv`](data/game-data.csv). As much as I wish there was a script for this, there isn't.

7. Take note of the new disk usage information with `df`. You should see around 200 GB of data in your `~/.steam/debian-installation/steamapp/common` folder.

8. Identify the amplification factor of the LEM with:
```
forsa rtm ls
```

The actual space taken is given by

![formula](https://render.githubusercontent.com/render/math?math=S_1%20=%20S_0%20*%20%28%20\frac{1}{A_1}%29%20-%20S_{-1}%20*%20%28\frac{1}{A_{-1}}%29)

where ![formula](https://render.githubusercontent.com/render/math?math=S_1) is the space taken, ![formula](https://render.githubusercontent.com/render/math?math=S_0) is the raw data size (the output of step 4), and ![formula](https://render.githubusercontent.com/render/math?math=A_1) is the amplification factor from step 8. ![formula](https://render.githubusercontent.com/render/math?math=S_{-1}) and ![formula](https://render.githubusercontent.com/render/math?math=A_{-1}) refer to the space taken and amplification found in steps 4 and 5.
