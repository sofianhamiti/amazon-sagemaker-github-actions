FROM public.ecr.aws/lambda/python:3.8

# Copy Canvas shutdown code
COPY cors.py ${LAMBDA_TASK_ROOT}/


CMD [ "cors.lambda_handler" ]