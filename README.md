# gpy_site ( New name coming soon )
A Dockerized Django project to communicate with Steam, and specifically targetting `Source` servers, aiming to be an all in one community site.( Forums, remote admin through RCON, steam auth, etc ) Set up your own instance from this repository, or use use the official instance once it's up!
## Currently working features
- Docker containers
- Django basic site
- Steam Authentication
## Installation ( You must have Docker CE, Docker-Compose, Python, and PIP | Guide coming soon )
- Fork the repo if you plan to make changes or experiment.
- Review Developer Guidelines/Contributing/Pull-Requests&Forks if applicable.
- CD to the base directory with docker-compose.yml
- Run `docker-compose build`
- Run `docker-compose up -d`
- Verify everything is working with `docker-compose logs -f` or `docker-ps`
