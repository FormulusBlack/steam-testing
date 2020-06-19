# Steam Testing on Forsa
Resources for reproducing the testing done on BitMarker effectiveness with regards to Steam games.


## Prerequisites
Before getting started, get a free trial of Forsa [here](https://www.formulusblack.com/see-it-work/). You will also need to install Forsa on your preferred OS (we used Ubuntu 18.04). <br/>


## Testing FORSA
1. Create a LEM (Logical Extension of Memory):
```
> forsa --user <username> --psswd <password> lem create --name STEAM_TESTING --size $(bc <<< "256 * 1024")
```

2. Create a VM (for our testing we used 73G RAM and 8 CPUs, but that shouldn't affect deduplication results):
```
> forsa --user <username> --psswd <password> vm create --name Steam_Ubuntu --cpu <cpu> --ram <ram>
```

3. Attach the LEM to the VM:
```
> forsa --user <username> --psswd <password> vm attach --device-name STEAM_TESTING --name Steam_Ubuntu --type lem
```

4. Install Ubuntu desktop on the VM. After installing Steam, take baseline disk usage information with `df`.

5. Identify the amplification factor of the LEM with:
```
> forsa rtm ls
```

6. Install the games detailed in [`game-data.csv`](data/game-data.csv). As much as I wish there was a script for this, there isn't.

7. Take note of the new disk usage information with `df`. You should see around 200 GB of data in your `~/.steam/debian-installation/steamapp/common` folder.

8. Identify the amplification factor of the LEM with:
```
> forsa rtm ls
```

The actual space taken by the Steam games is given by

![formula](https://render.githubusercontent.com/render/math?math=S_1%20=%20S_0%20\cdot%20%28%20\frac{1}{A_1}%29%20-%20S_{-1}%20\cdot%20%28\frac{1}{A_{-1}}%29)

where ![formula](https://render.githubusercontent.com/render/math?math=S_1) is the space taken, ![formula](https://render.githubusercontent.com/render/math?math=S_0) is the raw data size (the output of step 4), and ![formula](https://render.githubusercontent.com/render/math?math=A_1) is the amplification factor from step 8. ![formula](https://render.githubusercontent.com/render/math?math=S_{-1}) and ![formula](https://render.githubusercontent.com/render/math?math=A_{-1}) refer to the space taken and amplification found in steps 4 and 5.

## Testing other filesystems

### 1. OpenZFS

We followed the instructions in [this guide](https://ubuntu.com/tutorials/setup-zfs-storage-pool#1-overview) for setting up a single-disk ZFS pool on Ubuntu.

Deduplication was turned on with
```
> zfs set dedup=on steampool/steam
```
where `steampool/steam` was our pool name and directory.

After copying the contents of your `~/.steam` folder over, to look at the "amplification", see the `DEDUP` field of:
```
> zpool list steampool
```

The actual space used can be calculated from this number.

### 2. lessfs

[This guide](https://opensourceforu.com/2019/02/data-deduplication-with-a-linux-based-file-system/) gave us our approach for setting up `lessfs`. Default configurations were used except for the `compression` line, which we set to `none`. We found in testing that turning on compression incurred a performance penalty too high for gaming applications.

### 3. fdupes

For testing `fdupes`, we installed with `apt`. Then, we collected data with

```
> fdupes -r ~/.steam > ~/fdupes.out
```

The included [`fdupes-analyze.py`](tools/fdupes-analyze.py) can read the output of `fdupes -r` and return the savings. To use, run
```
> ./fdupes-analyze.py ~/fdupes.out
```
