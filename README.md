# trade-analysis
A simple python framework to analyze trade execution. trade-analysis has been created with the aim to analyze execution of trades better.  One can estimate how much saving a person will make if he/she executes the trades using the benchmark execution algorithms provided in this repo.
With trade-analysis more seasoned traders can code up their intuition and see how it performs on different securities on historical data.

## Installation
1. Make sure you have a github account. If not make one [here](https://github.com/join)  
2. Fork the repo.  
3. Clone it into you repository:  
    `git clone https://github.com/USERNAME/trade-analysis`  
4. Make sure pip is installed. Check if is installed by `pip -V` on linux systems. If not do the following:  
        `sudo apt-get update`  
        `sudo apt-get upgrade`  
        `sudo apt-get install python-pip`        
5. We love  using virtualenv. It enables to work on different python projects with different versions of libraries. It is not mandatory to install. Install it from [here](https://virtualenv.pypa.io/en/stable/installation/)  
6. Install the project requirements by executing `pip install -r requirements.txt`  
7. Add to PYTHONPATH trade-analysis directory.

## Contribution
We want you to contribute and make this project richer. After you have successfully installed the requirements and are ready to code, glance through the [contribution guidelines](CONTRIBUTING.md) to get the formatting and code structure related things which this project adheres to.

## License
See the [license](LICENSE) file.

## Examples
If you want to do the analysis of a trade of selling 12 shares of etf VWO at time 5:35:00 PM UTC on 25th March 2015 using our mean reversion execution algorithm, execute the following command.  
`python execution/simulate_execution.py 20150325 VWO S 12 MeanRev 173500`

We have provided sample minute bars for different securities generated from market data of 25th March 2015. Hence for running the backtesting one can give any of the shortcodes which are present in datafiles directory. MeanRev, Momentum and Direct are the execution algorithms provided.
