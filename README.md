# gpy_site
A Dockerized Django project to communicate with Garrysmod ULX aiming to be an all in one site.( Forums, remote admin, steam auth, etc )
## Currently working features
- Docker containers
- Django basic site
- Steam Authentication
## Installation
- Fork the repo if you plan to make changes or experiment.
- CD to the base directory with docker-compose
- Run `docker-compose build`
- Run `docker-compose up -d`
- Verify everything is working with `docker-compose logs -f`
### To do:
- [ ] Link Django to Postgres db container
- [ ] Add password setting to Postgres
- [ ] Begin ULX module
- [ ] Plan ahead for feature development
