# Keyua Portal

## Start
Install environment. From project folder run command:
```
./build/buildenv.sh
```
Install Fabric
```
pip install fabric3
```

## Create database, run project, run Celery
```
./manage.py migrate
./manage.py runserver
./manage.py celeryd -B
```

## Internationalization
```
./manage.py makemessages_lazy -l ru
./manage.py compilemessages
```

## Run tests
```
./manage.py test --keepdb
```

### Troubleshooting
[Install python3.X-dev](https://stackoverflow.com/questions/26053982/error-setup-script-exited-with-error-command-x86-64-linux-gnu-gcc-failed-wit)

ImportError: ../env/lib/python3.6/site-packages/psycopg2/.libs/libresolv-2-c4c53def.5.so: symbol __res_maybe_init, version GLIBC_PRIVATE not defined in file libc.so.6 with link time reference

Solution:
```
./env/bin/pip install psycopg2 --upgrade
```