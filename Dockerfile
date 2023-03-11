FROM alpine:3.17

RUN apk --no-cache --update-cache add python3 py3-pip py3-wheel py3-numpy py3-scikit-learn uwsgi-python3 uwsgi-http
RUN pip install --no-cache-dir Flask==2.2.3 joblib==1.2.0

COPY run.py run.sh /app/
WORKDIR /app

CMD ["/app/run.sh"]