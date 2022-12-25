# cvpfinder
A tool for detecting **confusing (highly similar) variable pairs** in Java/Python programs.
- `cvpfinder4j` : tool for Java
- `cvpfinder4p` : tool for Python

These are shell scripts running Java and Python programs to analyze the source code.

## How to install
You can install this tool (1) from Docker Hub or (2) manually.

### Install from Docker Hub

Run the following command:  
`docker pull amanhirohisa/cvpfinder`

See https://docs.docker.com/desktop/ for installing Docker Desktop.

### Manually Install
1. Download [cvpfinder-1_0.zip](https://github.com/amanhirohisa/cvpfinder/releases/download/v1.0/cvpfinder-1_0.zip) and unpack it.
2. Download [javaparser-core-3.24.2.jar](https://search.maven.org/search?q=g:com.github.javaparser%20AND%20a:javaparser-core) and put it into `cvpfinder/lib`.
3. Add the directory `cvpfinder` to your PATH environmental variable.  
ex. `export PATH=$PATH:/home/xxx/cvpfinder`
4. Install the followings:  
  4.1) Java (>= 1.8.0)  
  4.2) Python (= 3.9.x) ... [Spiral](https://github.com/casics/spiral) 1.1.0, the identifier splitter, does *not work under Python >= 3.10*.<br>
  4.3) enchant  
  ex. `apt-get install enchant`  
  4.4) [Spiral](https://github.com/casics/spiral) 1.1.0  
  ex. `pip install git+https://github.com/casics/spiral.git`  
  4.5) gensim, pyenchant  
  ex. `pip install gensim pyenchant`

##  Usage
Run the following command (`xxx` is a Java source file or a directory):  
`cvpfinder4j xxx`  
Then, you get the report file `cvpfinder/report/report.csv`

For Python programs, run `cvpfinder4p` instead.

### Run via Docker
You need to mount the input/output directories.  

When you analyze <span style="color: red">C:\Users\aman\src\xxx</span> and get the report as <span style="color: green">C:\Users\aman\report</span>\report.csv, run as:  
`docker container run -it -v `<span style="color: red">C:\Users\aman\src\xxx</span>`:/data -v ` <span style="color: green">C:\Users\aman\report</span>`:/cvpfinder/report cvpfinder /cvpfinder/cvpfinder4j /data/`<span style="color: red">xxx</span>

In the above example, the tool
- analyzes `/data/xxx`</span> but it corresponds to your <span style="color: red">C:\Users\aman\src\xxx</span>, and  
- outputs `/cvpfinder/report/report.csv` but it corresponds to your <span style="color: green">C:\Users\aman\report</span>\report.csv.<br>
Notice: you need to create <span style="color: green">C:\Users\aman\report</span> first.
