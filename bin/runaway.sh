#!/bin/bash
#set -x
set -e

IP='0.0.0.0'
PORT='8686'
STATEPORT='18686'
processes='2'
workers='8'
procname='runaway'
procnamemaster='runaway_master'
export RUNAWAY_CONF_DIR='/etc/runaway/'

if [[ -z ${RUNAWAY_BASEDIR} ]]
then
	RUNAWAY_BASEDIR=$(dirname $(dirname $(readlink /proc/$$/fd/255)))
fi

if [[ -z ${RUNAWAY_BINDIR} ]]
then
    RUNAWAY_BINDIR=$RUNAWAY_BASEDIR"/bin"
fi

if [[ -z ${PYTHON} ]]
then
	PYTHON='/usr/bin/python'
fi

if [[ -z ${PYTHON_ENV} ]]
then
	PYTHON_ENV='/usr/bin/virtualenv'
fi

if [[ -z $RUNAWAY_ENV_PATH ]]
then
	RUNAWAY_ENV_PATH="/usr/local/$procname"
fi

if [[ -z ${RUNAWAY_PID_FILE} ]]
then
	RUNAWAY_PID_FILE=$RUNAWAY_BASEDIR'/runaway.pid'
fi

if [[ -z ${RUNAWAY_LOG_FILE} ]]
then
	RUNAWAY_LOG_FILE="/var/log/runaway/runaway.log"
fi

find ${RUNAWAY_BASEDIR} -name *.pyc|xargs rm -f {}

function start(){

mkdir -p `dirname $RUNAWAY_PID_FILE`
mkdir -p `dirname $RUNAWAY_LOG_FILE`

if [ ! -d $RUNAWAY_CONF_DIR ]; 
then
	echo "WARN......Use dev config run now!"
fi

find ${RUNAWAY_BASEDIR} -name *.pyc|xargs /bin/rm -f {}

if [ ! -d $RUNAWAY_ENV_PATH ]; then
	# install first time
	[ -z `rpm -qa|grep python-devel` ] && yum install python-devel openldap-devel mysql-devel -y
	[ ! -e /usr/bin/virtualenv ] && yum install python-virtualenv -y
	$PYTHON_ENV $RUNAWAY_ENV_PATH
	source $RUNAWAY_ENV_PATH/bin/activate
	#pip install -U pip==8.1.0  # offical source, maybe slow
	pip install -r $RUNAWAY_BASEDIR/requirements.txt -i http://pypi.douban.com/simple  # use http, limitation of python version
fi

source $RUNAWAY_ENV_PATH/bin/activate
cd ${RUNAWAY_BASEDIR}

uwsgi --http-socket $IP:$PORT -w $procname:app --processes $processes --workers $workers --enable-threads \
--procname=$procname --procname-master=$procnamemaster --daemonize $RUNAWAY_LOG_FILE --pidfile $RUNAWAY_PID_FILE --stats $IP:$STATEPORT --http-timeout 10 \
--post-buffering 4096 --buffer-size 4096 --socket-timeout 60

$RUNAWAY_ENV_PATH/bin/python ${RUNAWAY_BASEDIR}/runaway/while/runtask.py start
echo $procname" is start!"

}

function stop(){

	pids=$(ps -ef | grep $procname | grep -v 'grep' | grep -v '.sh' | awk '{print $2}')
	for i in ${pids}
	do 
		kill -9 ${i} > /dev/null
    done

    rm -f $RUNAWAY_PID_FILE

    $RUNAWAY_ENV_PATH/bin/python ${RUNAWAY_BASEDIR}/runaway/while/runtask.py stop
    echo $procname" is stop!"

}

function restart(){

	stop
	sleep 1
	start

}

function reload(){
	source $RUNAWAY_ENV_PATH/bin/activate

	if [[ -f ${RUNAWAY_PID_FILE} ]]
	then
		uwsgi --reload $RUNAWAY_PID_FILE
	else
		echo $RUNAWAY_PID_FILE" not found!"
	fi

	echo $procname" is reload!"

}


case $1 in
	start|START)
	start
	;;
	stop|STOP)
	stop
	;;
	restart|RESTART)
	restart
	;;
	reload|RELOAD)
	reload
	;;
	*)
	echo "USAGE: $0 start|stop|restart|reload"
	exit 1
	;;
esac
