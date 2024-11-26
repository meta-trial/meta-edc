cd ~/app &&
celery multi start w1 w2 -A meta_edc -l INFO --workdir="/home/live/app/" --logfile=/home/live/log/%n%I.log --pidfile=/home/live/celery/%n.pid

# to stop
# celery multi stop w1
