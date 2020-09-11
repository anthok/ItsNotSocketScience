# ItsNotSocketScience
Mass socket listener




### Building & Running with Docker
* Build first
```
docker build Dockerfile -t socketscience
```

* Non-RHEL distros
```
mkdir fbeatlogs;
docker run --name=socketscience -d -v `pwd`/fbeatlogs:/opt/socketscience/logs --network=host socketscience
```

* On RHEL due to selinux
```
mkdir fbeatlogs;
docker run --name=socketscience -d -v `pwd`/fbeatlogs:/opt/socketscience/logs:z --network=host socketscience
```
