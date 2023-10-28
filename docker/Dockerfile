FROM python:3.9.16-buster

RUN apt-get update
RUN apt-get install -y openjdk-11-jre-headless
RUN wget https://github.com/amanhirohisa/cvpfinder/releases/download/v1.1/cvpfinder-1_1.zip
RUN unzip cvpfinder-1_1.zip
RUN chmod 755 cvpfinder/cvpfinder4*
RUN wget https://repo1.maven.org/maven2/com/github/javaparser/javaparser-core/3.24.2/javaparser-core-3.24.2.jar
RUN mv javaparser-core-3.24.2.jar /cvpfinder/lib
RUN chmod 644 /cvpfinder/lib/javaparser-core-3.24.2.jar
RUN pip install git+https://github.com/casics/spiral.git
RUN apt-get -y install enchant
RUN pip install gensim pyenchant
