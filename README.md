# Biodiversity Analysis #

Biodiversity Data Analysis and Visualization

A Project by Institute of Information Science, Academia Sinica

## Features ##

* Spatial distribution graph
* Spatial correlation quotient
* Temporal distribution graph
* Temporal correlation quotient
* Co-occurrence correlation quotient

Supported file format: Darwin Core Archive (DwC-A).

## Screenshots ##

![a](https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/a.png "a")

![b](https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/b.png "b")

![c](https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/c.png "c")

![d](https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/d.png "d")

<img src="https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/e.png" alt="e" title="e" width="435.4" height="634.2">

![f](https://raw.githubusercontent.com/yuwen41200/biodiversity-analysis/master/img/f.png "f")

Sample biodiversity data used in the above demonstration:  
Shao, Kwang-Tsao, et al. (2012) A dataset from bottom trawl survey around Taiwan. ZooKeys 198: 103-109.  
(doi: [10.3897/zookeys.198.3032](http://dx.doi.org/10.3897/zookeys.198.3032))

## Getting Started ##

Download the repository and execute the following command:

```bash
source ./install.sh
```

From now on, you can start this program by running:

```bash
./src/app.py
```

## Requirements ##

Make sure you have installed all dependencies:

```bash
sudo apt-get install python3.5 python3.5-venv python3-numpy python3-scipy python3-matplotlib
```

This program has been tested on Ubuntu 15.10 and above,  
but it should work on other platforms with few modifications.

## Documentation ##

Full documents are available at:  
<https://rawgit.com/yuwen41200/biodiversity-analysis/master/docs/index.html>.

## Acknowledgement ##

Special thanks to:

* Tyng-ruey Chuang from Institute of Information Science, Academia Sinica
* Te-en Lin from Endemic Species Research Institute, Council of Agriculture
* Jason Mai from Biodiversity Research Center, Academia Sinica
* Yi-hong Chang from Word Gleaner Ltd.

## License ##

Biodiversity Analysis: Biodiversity Data Analysis and Visualization  
Copyright (C) 2016 Yu-wen Pwu and Yun-chih Chen

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.

You should have received a copy of the GNU General Public License  
along with this program. If not, see <http://www.gnu.org/licenses/>.
