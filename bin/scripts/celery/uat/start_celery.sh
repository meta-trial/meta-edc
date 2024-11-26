cd ~/app &&
celery multi start w1 w2 -A meta_edc -l INFO --workdir="/home/uat/app/" --logfile=/home/uat/log/%n%I.log --pidfile=/home/uat/celery/%n.pid

# to stop
# celery multi stop w1
