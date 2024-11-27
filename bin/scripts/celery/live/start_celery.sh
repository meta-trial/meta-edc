cd ~/app &&
celery multi start worklive -A meta_edc.celery_live:app -Q live_queue -l INFO --workdir="/home/live/app/" --logfile=/home/live/log/%n%I.log --pidfile=/home/live/celery/%n.pid
