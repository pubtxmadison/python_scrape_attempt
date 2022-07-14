ARG FUNCTION_DIR="/function"

FROM ubuntu:22.04


RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  python3.9 \
  python3-pip

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

COPY testlambda.py ${FUNCTION_DIR}
COPY requirements.txt ${FUNCTION_DIR}
RUN ls
#COPY doHL.js ${LAMBDA_TASK_ROOT}
#COPY jquery-3.2.1.min.js ${LAMBDA_TASK_ROOT}


RUN python3 -m pip install awslambdaric --target "${FUNCTION_DIR}"


ENV PLAYWRIGHT_BROWSERS_PATH=${FUNCTION_DIR}/pw-browsers 
RUN python3 -m pip install -r ${FUNCTION_DIR}/requirements.txt --target "${FUNCTION_DIR}"
RUN python3 -m playwright install --with-deps chromium
# I switched to just installing chromium/chromium deps because I think the stealth package I found 
# only works with it anyway, but I'd be happy to use webkit or firefox if they can be made stealth
#RUN python3 -m playwright install-deps 



#blanked out the below variables, they are used in testlambda.py - but obviously not in github
ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_DEFAULT_REGION=

ENV proxy_address=
ENV proxy_username=
ENV proxy_password=

ENV mysql_host=
ENV mysql_userid=
ENV mysql_passwd=
ENV mysql_port=
ENV mysql_db=

ENV slack_token=

ENV testlambda=True

RUN which python3


# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh

ENTRYPOINT [ "/entry.sh" ]
# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "testlambda.handler" ]
