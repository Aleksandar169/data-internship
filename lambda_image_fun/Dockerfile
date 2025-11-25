FROM public.ecr.aws/lambda/python:3.11

#RUN pip install pandas boto3 requests

COPY lambda_fun.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_fun.lambda_handler"]
