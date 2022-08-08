from locust import HttpUser, task

data = {'date': 'helloworld', 'data_1': 'helloworld1'}


class EmptyGet(HttpUser):
    host = 'http://localhost:5000'

    @task
    def empty_get(self):
        self.client.get('/test_performance/empty_get')


class EmptyPost(HttpUser):
    host = 'http://localhost:5000'

    @task
    def empty_post(self):
        self.client.post('/test_performance/empty_post', json=data)


class InsertSync(HttpUser):
    host = 'http://localhost:5000'

    @task
    def insert_sync(self):
        self.client.post('/test_performance/insert_sync', json=data)


class EmptyPostExpress(HttpUser):
    host = 'http://localhost:3000'

    @task
    def empty_post(self):
        self.client.post('/', json={'date': 'helloworld', 'data_1': 'helloworld1'})
