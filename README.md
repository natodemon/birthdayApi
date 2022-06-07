# birthdayApi

## Purpose

The purpose of this project is to create a simple 'Hello World' style application that exposes an API with GET and PUT methods.

## Usage

The application is containerised and a docker-compose file is supplied for local deployment. From the project's root directory, run the following command:

```bash
docker-compose -f birthdayApi.yaml up
```

As the output will indicate, the program will now be listening for requests at `localhost` on port 5000.

### Requests

Request: `PUT /hello/<username> { “dateOfBirth”: “YYYY-MM-DD” }`
Response: `204 No Content`

Request: `GET /hello/<username>`
Response: `200 OK`

### Examples

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"dateOfBirth":"2021-06-06"}' http://localhost:5000/hello/adam

curl -X GET http://localhost:5000/hello/hoovie
```

### Testing

The suite of tests is written using the `pytest` module and consists of a series of functional test. Executing the test set is achieved by changing to the _test_ directory and, with the _birthdayApi_ service running, executing the command `pytest`

## Implementation

This section gives a brief description of a number of the technologies used in this project and the reason for choosing them.

### Server-side

The application itself and by extension the testing suite are written in Python. This was chosen due to the large number of relevant libraries available allowing for quick development, the author's familiarity with the language and it's compatibility with other technologies.

### Datastore

Initially a very simple local key-value store was to be used to contain the user data given the project's simple functionality. However this would not have scaled very well and crucially, it would not have allowed for horizontal scaling of the application due to each application instance having it's own datastore. 

DynamoDB was chosen as it would allow for a redundant & highly-available datestore while abstracting away all of the infrastructure management. This, along with the availability of a locally deployable container for testing made DynamoDB a good choice to focus on coding a solution and not worrying about DB management. 

This solution does result in some potential cloud lock-in, however switching to another cloud solution such as GCP's Firestore would be quite a trivial task at a code level.

### Containerisation

A containerised as opposed to serverless solution was chosen as it allows for a highly-available and horizontally scalable service. Docker containers also allow for easy version control and can be deployed on many different infrastructure types, be that kubernetes-based or a native cloud solution.