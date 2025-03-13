# SmartSearch

### Smart Transfer is a tool that tracks and updates the latest transactions by phone number, card number and other identifiers. It provides up-to-date information about transfers made through the specified identifiers, providing the user with full control and transparency of financial transactions.

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)


## Configuration

Before running the project, you need to configure certain settings. Follow the instructions below:

1. Rename the `.env.example` file to `.env`:

   ```shell
   mv .env.example .env
   
2. #### Open the .env file in a text editor and provide the necessary values for the environment variables:
    SECRET_KEY=your_secret_key

    DATABASE_URL=your_database_url

    KAFKA_URL=kafka:29092

    ORACLE_CONNECTION=...

    CELERY_BROKER_URL=redis://redis:6379/0

    CELERY_RESULT_BACKEND=redis://redis:6379/0

## Installation

You can choose either of the following methods to install and set up the project:

### Docker Installation

1. Make sure you have Docker installed on your system. Refer to the [Docker documentation](https://docs.docker.com/get-docker/) for installation instructions.


2. Clone the repository:
    ```
    git clone https://gitlab.com/nurbolot664/miraclesoftrepo.git
    ```
   2.1 Build the Docker image and start the container:
   ```
    cd my-project
   ```
   ```
    docker-compose -f docker-compose.local.yml up --build
   ```

3. Access the application at http://localhost:8000.
___

## API Reference

- [Get Services by Phone/Card](README-API.md):
  View the available API endpoints and their functionalities.

## Celery

- [Celery Tasks](celery-tasks.md): Explore the dashboard view and its functionalities.

For more detailed instructions and examples, click on the links provided in each subsection above.


# Usage

The Usage section provides guidance on how to use and interact with the project. It covers various aspects and features to help you make the most of the project's capabilities.

1. Alembic migrations need use only local or Test Server.
  ```
   alembic init alembic
   alembic revision --autogenerate -m "init commit"
   alembic upgrade head      
  ```
2. Connect to Docker-Container PostgresSQL and Command for INSERT to data
   ```
   docker exec -it <docker_id> psql -U <user> <db_name>
   docker exec -it f5ad1449e841 psql -U postgres smart_search

   ```
   ```
   INSERT INTO core.t_phones (phone_number, is_exist_b24);
   INSERT INTO core.t_categories (id, name) VALUES (1, 'Bank')
   INSERT INTO core.t_services (service_id, service_name, logo, category_id)
   INSERT INTO core.t_association(service_id, phone_number, props_name) VALUES(1, 996708540631, 'nur');
   
   INSERT INTO core.t_service_id_storage(service_sp_id, service_id)
   VALUES
       (1, 2), (3, 4);
   
   INSERT INTO core.t_bins (name, bins)
   VALUES
       ('MOSCOMBANK', '22021202'),
       ('TKPB', '22032503'),
       ('TKPB', '22032502'),
       ('NS Bank', '22022801'),
       ('Bank Perm', '22023601'),
       ('NICO-BANK', '22025501'),
       ('Renessans Kredit', '22034102'),
       ('Renessans Kredit', '22034103'),
       ('Renessans Kredit', '22034101'),
       ('Bank Solidarnost', '22024902'),
       ('Alef-Bank', '22025301'),
       ('Novobank', '22025601'),
       ('Novobank', '22025602'),
       ('ZHIVAGO BANK', '22025701'),
       ('LANTA BANK', '22025801');
   ```
   
3. Kafka Command Show Topics and for connect to Producer/Consumer 
   ```
   kafka-topics --list --bootstrap-server localhost:29092
   kafka-console-consumer --bootstrap-server localhost:29092 --topic bakai_smart_search_topic --from-beginning
   kafka-console-producer --bootstrap-server localhost:29092 --topic bakai_smart_search_topic
   ```

For more details, please refer to the [contribution guidelines](CONTRIBUTING.md).

kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
