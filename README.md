
# MCQ Server

[![CodeFactor](https://www.codefactor.io/repository/github/pict-acm-student-chapter/mcq-server/badge/master)](https://www.codefactor.io/repository/github/pict-acm-student-chapter/mcq-server/overview/master)

This is the repo for the MCQ Platform's server with Django as the framework and PostgreSQL as the database.


## About the project.
-   PostgreSQL used as the primary database.
-   Superuser is already initialized with the credentials: Username- `admin`, Email- `admin@admin.com`, Password- `admin`
-   Integration with Django Rest Framework
-   Integrated Djoser for user register/login/logout workflows.
-   Used JWT for Authentication.
-   API Documentation is configured using swagger.
-   Containerized using Docker and managed using docker-compose.

## Getting Started
To get a local copy of this template up and running on your machine, follow these simple steps.
### Prerequisites
- Docker
`curl -fsSL https://get.docker.com -o get-docker.sh`
`sudo sh get-docker.sh`
`sudo apt install docker-compose`
`sudo groupadd docker`
`sudo usermod -aG docker $USER`
`newgrp docker`

### Installation
- Clone the repo `git clone https://github.com/PICT-ACM-Student-Chapter/MCQ-Server.git`
- Change the current directory to the template `cd MCQ-Server`
- Build the docker containers`docker-compose -f docker-compose.dev.yml build` for the dev containers and `docker-compose -f docker-compose.prod.yml build` for the prod containers
- Run the docker containers`docker-compose -f docker-compose.dev.yml up` for the dev containers and `docker-compose -f docker-compose.prod.yml up` for the prod containers

## API Documentation
API documentation is done using swagger. Visit `/swagger` for API documentation.

## Technologies used
<a href="https://www.djangoproject.com/" target="_blank"><img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/> </a>
<a href="https://www.django-rest-framework.org/" target="_blank"> <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" /> </a>
<a href="https://www.docker.com/" target="_blank"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/></a>



## Contributing
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/PICT-ACM-Student-Chapter/MCQ-Server](https://github.com/PICT-ACM-Student-Chapter/MCQ-Server)

