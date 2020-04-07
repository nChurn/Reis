FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /property_passport
WORKDIR /property_passport
COPY ./requirements.txt /property_passport/
RUN pip install -r requirements.txt
COPY . /property_passport/
RUN apt-get update
RUN apt-get install -qq -y wget xvfb unzip
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
ENV CHROMEDRIVER_VERSION 79.0.3945.36
ENV CHROMEDRIVER_DIR ./chromedriver
RUN mkdir $CHROMEDRIVER_DIR
RUN wget -q --continue -P $CHROMEDRIVER_DIR "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver/chromedriver
# ENV PATH $CHROMEDRIVER_DIR:$PATH