# GTEx eQTL Browser example

### Build the docker image

docker build -t tag_of_docker_image directory_of_docker_file

#### Usage Example
cd C:\Users\chris\Documents\code\gtex_eqtl_browser\

docker build -t genomics_docker .

docker run -ti genomics_docker

#docker run -ti -v C:\Users\chris\Documents\code\test\:/test #genomics_docker


### Run the server using docker

```
docker run -ti -p 5000:5000 -v C:\Users\chris\Documents\code\eqtl_data\:/data -v C:\Users\chris\Documents\code\gtex_eqtl_browser\:/app genomics_docker

echo 'deb http://deb.debian.org/debian sid main' >> /etc/apt/sources.list
```

### sqlite3 commands

#### From Bash

```
sqlite3 /data/eqtl_database.db
```

```
.tables

pragma table_info(gene_info);

select * from gene_info where gene_name = 'INF2';


pragma table_info(eGene);

select * from eGene limit 5;


pragma table_info(eSNP);

select * from eSNP limit 5;

```

### Copy on windows using powershell

```
Copy-Item .\gtex_eqtl_browser2\* .\gtex_eqtl_browser -recurse
```

### Git info
```
git push origin main 
```
