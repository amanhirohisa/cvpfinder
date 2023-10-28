# cvpfinder
A tool for detecting **confusing (highly similar) variable pairs** in Java/Python programs.
- `cvpfinder4j` : tool for Java
- `cvpfinder4p` : tool for Python

These are shell scripts running Java and Python programs to analyze the source code.

## How to install
You can install this tool (1) from Docker Hub or (2) manually.

### (1) Install from Docker Hub

Run the following commands:  
<On Mac (Apple chip)>  
`docker pull amanhirohisa/cvpfinder:linux_arm64_v8`  
`docker tag amanhirohisa/cvpfinder:linux_arm64_v8 amanhirohisa/cvpfinder:latest`

<On Windows, etc.>  
`docker pull amanhirohisa/cvpfinder:linux_arm64`  
`docker tag amanhirohisa/cvpfinder:linux_arm64 amanhirohisa/cvpfinder:latest`


See https://docs.docker.com/desktop/ for installing Docker Desktop.

### (2) Manually Install
1. Download [cvpfinder-1_1.zip](https://github.com/amanhirohisa/cvpfinder/releases/download/v1.1/cvpfinder-1_1.zip) and unpack it.
2. Download [javaparser-core-3.24.2.jar](https://repo1.maven.org/maven2/com/github/javaparser/javaparser-core/3.24.2/javaparser-core-3.24.2.jar) and put it into `cvpfinder/lib`.
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

Suppose your current directory is **/Users/aman**.<br>
When you analyze **src/xxx** and get the report as **report**/report.csv, run as:

`docker container run -it -v /Users/aman:/data -v /Users/aman/report:/cvpfinder/report amanhirohisa/cvpfinder /cvpfinder/cvpfinder4j /data/src/xxx`

In the above example, the tool
- analyzes `/data/src/xxx`</span> but it corresponds to **src/xxx** under the current directory, and  
- outputs `/cvpfinder/report/report.csv` but it corresponds to **report/report.csv** under the current directory.<br>
Notice: you need to create directory **report** first.

Because the above way of running is a little complicated, we provide simple shell scripts [run_cvpfinder4j](https://raw.githubusercontent.com/amanhirohisa/cvpfinder/main/docker/run_cvpfinder4j), [run_cvpfinder4p](https://raw.githubusercontent.com/amanhirohisa/cvpfinder/main/docker/run_cvpfinder4p).  
You can analyze **src/xxx** as:

`sh run_cvpfinder4j src/xxx`

Then, you can get `report/report.csv` under the current directory.

We also provide [run_cvpfinder4j.bat](https://raw.githubusercontent.com/amanhirohisa/cvpfinder/main/docker/run_cvpfinder4j.bat), [run_cvpfinder4p.bat](https://raw.githubusercontent.com/amanhirohisa/cvpfinder/main/docker/run_cvpfinder4p.bat) for Windows platform.  
You can analyze **src\xxx** as:

`run_cvpfinder4j.bat src\xxx`
