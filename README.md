# Docker Web Service
Using two Docker Containers make a web service with a web app and a database. 
Final course project for Computer Structure II.
Made by:
- [Sebastian Enrique González Benítez](https://github.com/gonzalezsebastian)
- [Camilo Andrés Céspedes Jímenez](https://github.com/Camilo-116)
- [Dilan Jesús Triana Sánchez](https://github.com/Tdilan395)

# Set Up
```sh
$ git clone https://github.com/gonzalezsebastian/DockerWebService.git
$ cd DockerWebService
$ docker-compose up -d
```
# Test app
1. `curl http://localhost:5000/` test if conection with the database is succesfull sending message 'ok' if not 'nok'.
2. `curl http://localhost:5000/tablaS/<id>` creates a hash with ID.
3. `curl http://localhost:5000/tablaS/<id>/<ts>` creates a hash with ID and TimeStamp.
4. `curl http://localhost:5000/tablaA/<id>/<hash>` marks attendance with student ID and checks if the hash is valid and is within 4 hours of hash generation.
5. `curl http://localhost:5000/tablaA` returns a JSON of attendance of all classes.
6. `curl http://localhost:5000/tablaS` returns a JSON of all generated hashes for attendance.
7. `curl http://localhost:5000/sesion/<id>` returns a JSON for an specific ID in sessions tables.
8. `curl http://localhost:5000/delete` deletes content of both tables.
