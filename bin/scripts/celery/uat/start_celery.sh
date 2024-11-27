cd ~/app &&
celery multi start workuat -A meta_edc.celery_uat:app -Q uat_queue -l INFO --workdir="/home/uat/app/" --logfile=/home/uat/log/%n%I.log --pidfile=/home/uat/celery/%n.pid
