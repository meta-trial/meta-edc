cd ~/app &&
celery multi stopwait w1 w2 &&
celery -A meta_edc control shutdown &&
cd ~/
