# RBP
Implementation of "RBP: A Website Fingerprinting Obfuscation Method Against Intelligent Fingerprinting Attacks"





$ python src/main.py -h

usage: main.py [-h] [-c <config name>] [--log <log path>]
               [--log-level <log level>]
               <traces path>
[...]
```

 1. Clone the repo: `git clone git@github.com:lt1342258812/RBP.git`

 1. Install requirements: `pip install -r requirements.txt`

 1. Run a simulation with a specific configuration: `python src/main.py -c <config name> <traces path>`

 1. Check the results in `results/<config name>_<timestamp>` directory.


## Reproduce results

First of all, you will need to download the compressed data from the releases tab, place it in the `dataset/` directory and unpack the zipped files.

### Attack accuracy

We used the attacks such as DF, TF and CUMUL to evaluate our defense.

### Performance overhead

You can run the `overheads.py` script on the two sets of traces, the original
and the simulated ones. This script will return the latency and bandwidth
overheads.

```
 $ python src/overheads.py data/*

 Bandwidth overhead: 2.775651
 Latency overhead: 1.0

### Expected data format

The source code assumes that traffic trace files are represented as `<timestamp> <packet length>` sequences. Each line is a TCP packet as captured by `dumpcap` and the direction of the packet is encoded in the sign of the length.

The filenames of the traces have the following format: `<site index>-<instance index>`.

## Questions and comments

Please, address any questions or comments to the authors of the paper. The main developers of this code are:

 - Tao Luo (taoluo.ujs@gmail.com)

