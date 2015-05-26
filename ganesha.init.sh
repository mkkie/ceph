#!/bin/sh
#
### BEGIN INIT INFO
# Provides: ganesha.nfsd
# Required-Start: $local_fs $named $time $network 
# Required-Stop:  $local_fs $named $time $network 
# Default-Start:  2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: start and stop the ganesha.nfsd nfs-v4 service.
# Description: ganesha.nfsd is an NFS-v4 with compiled-in CephFS  support. 
### END INIT INFO
#

. /lib/lsb/init-functions
PATH=/usr/local/bin:/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/sbin
PATHPROG=/usr/local/bin/ganesha.nfsd
LOGFILE=/var/log/nfs-ganesha.log
CONFFILE=/etc/ganesha/ganesha.conf

# Local Daemon selection may be done by using /etc/quagga/daemons.
# See /usr/share/doc/quagga/README.Debian.gz for further information.
# Keep zebra first and do not list watchquagga!

# Print the name of the pidfile.
pidfile()
{
	echo "/run/ganesha/ganesha.pid"
}

# Check if daemon is started by using the pidfile.
started()
{
	[ -e `pidfile` ] && kill -0 `cat \`pidfile \`` 2> /dev/null && return 0
	return 1
}

# Starts the server if it's not alrady running according to the pid file.
# The Quagga daemons creates the pidfile when starting.
start()
{
  if started 
    then echo "ganesha.nfsd is running already."
         return 0
  else        
        if [ ! -d /run/ganesha ] 
          then sudo mkdir /run/ganesha 
               sudo chown `whoami`:`whoami` /run/ganesha 
        fi

	start-stop-daemon \
		--start \
                --background \
		--exec "$PATHPROG" \
                --  -f $CONFFILE  -L $LOGFILE  -p `pidfile` \
#                --  -L $LOGFILE \
#                --  -p `pidfile` 

  fi
}

# Stop the daemon given in the parameter, printing its name to the terminal.
stop()
{
    if ! started ; then
	echo "Sorry, ganesha.nfsd is not running."
	return 0
    else
	PIDFILE=`pidfile`
	PID=`cat $PIDFILE 2>/dev/null`
	start-stop-daemon --stop --quiet --oknodo --exec "$PATHPROG"
	#
	#       Now we have to wait until $DAEMON has _really_ stopped.
	#
	if test -n "$PID" && kill -0 $PID 2>/dev/null; then
	    echo -n " (waiting) ."
	    cnt=0
	    while kill -0 $PID 2>/dev/null; 
              do
		cnt=`expr $cnt + 1`
		if [ $cnt -gt 60 ]; then
		    # Waited 120 secs now, fail.
		    echo -n "Failed.. "
		    break
		fi
		sleep 2
		echo -n "."
              done
        fi
	echo -n " $1"
	rm -f `pidfile`
    fi
}


#########################################################
# 		Main program 				#
#########################################################

case "$1" in
    start)
        start
	;;

    stop|0)
	# stop ganesha.nfsd
        stop
   	;;

    restart|force-reload)
	$0 stop 
	sleep 1
	$0 start 
	;;

    status)
        if started 
          then echo "ganesha.nfsd is still running."
               return 0
        else 
          echo "Sorry, ganesha.nfsd is dead."
          return 1
        fi
	;;

    *)
    	echo "Usage: /etc/init.d/ganesha.nfsd {start|stop|restart|force-reload|status}"
	echo "     E.g. 'ganesha.nfsd --help'"
	echo "       will show you the basic usage."
	exit 1
	;;
esac

exit 0
