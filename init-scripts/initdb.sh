#!/bin/sh

# Inicializa base de datos


MYSQL_LOOPS="60"
#wait for mysql
i=0
while ! mysqladmin -h ${MUSSA_DB_HOST} -u root -p$MYSQL_ROOT_PASSWORD ping   >/dev/null 2>&1 < /dev/null; do
  i=`expr $i + 1`
  if [ $i -ge $MYSQL_LOOPS ]; then
    echo "$(date) - ${MUSSA_DB_HOST} still not reachable, giving up"
    exit 1
  fi
  echo "$(date) - waiting for ${MUSSA_DB_HOST}..."
  sleep 2
done


db_exists=$(mysql  --user=root --password="$MYSQL_ROOT_PASSWORD"  --host="$MUSSA_DB_HOST"  -s -N -e "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '${MUSSA_DB_NAME}'" information_schema)
  if [[ -z "${db_exists}" ]]; then
	echo "Inicializando base de datos"
	mysql  --user=root --password="$MYSQL_ROOT_PASSWORD"  --host="$MUSSA_DB_HOST" -e "CREATE DATABASE $MUSSA_DB_NAME"
        mysql  --user=root --password="$MYSQL_ROOT_PASSWORD"  --host="$MUSSA_DB_HOST" -e "GRANT ALL PRIVILEGES ON $MUSSA_DB_NAME.* TO ${MUSSA_DB_USER}@'%' IDENTIFIED BY '${MUSSA_DB_PASS}'" mysql
	mysql  --user=root --password="$MYSQL_ROOT_PASSWORD"  --host="$MUSSA_DB_HOST" $MUSSA_DB_NAME < /app/schema.sql
else
	echo "Base de datos ya inicializada"
	exit 0
fi
	
