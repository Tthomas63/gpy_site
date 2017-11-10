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

# Versioning:
The current road-map for G-Py is as follows, along with version standards.

G-Py Will start at version: 0.0.1a ( Current )

Alpha will be `x.0.1` - `x.4.9`: This will be the initial structure and clean-up of the project. Possibly just ignoring templates/styling altogether for now until all models, functions, utilities are initialized and any dependent features are in. 

Beta will be `x.5.0` - `x.9.9`: This will be templating, styling, polishing, bug fixes, final enhancements and features. Once into a stable initial release version, more polishing, responsiveness, and user interaction is planned along with updates to all function accessibility and usability. 

Subsequent versions will focus more on catering to instance hosts' needs, and making the utility more available along with advertising the project.

(major-version).(minor-version)-(sub-version)<applicable sub-version tag for beta/alpha>
IE Initial Release will be version: 1.0.0
Next minor version would be: 1.1.0

# Version 0.1.0a Target/Goal:
- [ ] Round off the entire project and clean-up
- [ ] Finish basic init of all apps, and polish to an acceptable standard
- [ ] Re-write all code to reflect new-knowledge
- [ ] Re-write main
- [ ] Re-write pipeline
- [ ] Finish re-templating with Semantic-UI
- [ ] Have a base template I am happy with




