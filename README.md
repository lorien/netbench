# Network Libraries Benchmark

Comparison of time, cpu, memory usage by different network libraries.


## Installation

* `apt-get install time`
* `make build`


## Usage

* Activate virtualenv `source .env/bin/activate`
* Run `./all.sh`
* Wait
* Open "var/result/index.html" file


## Configuration

To change list of running test cases edit "./config" file


## Troubleshooting

Try to run test directly without using any profilng tootls: `python3 runtest.py socket`
