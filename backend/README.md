# DormHub Backend API HELLO

## Installation

Simply run the following command:

```bash
docker-compose up
```

Then import dump.sql to your database.
```bash
docker cp dump.sql backend-db-1:/dump.sql # w folderze z plikiem dump.sql
docker exec -it backend-db-1 bin/bash
mysql -u <username from env> -p<password from env> < dump.sql
exit
```


