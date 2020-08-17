import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from graphene.test import Client

from post.models import Post
from post.schema import schema

from users.models import User


post_list_query = """
    query {
        posts {
            id,
            title,
            user {
            id,
            username
            }
        }
    }
"""

post_by_id_query = """
    query {
        postById(id: $id) {
            title,
            user {
                id,
                username
            }
        }
    }
"""

create_post_mutation = """
    mutation {
        createPost(postInput: $input) {
            post {
                id,
                title,
                user {
                    id,
                    username
                }
            }
        }
    }
"""

update_post_mutation = """
    mutation {
        updatePost(id: $id, postInput: $input){
            post {
                id,
                title,
                user {
                    id,
                    username
                }
            }
        }
    }
"""

delete_post_mutation = """
    mutation {
        deletePost(id: $ID) {
            deleted
        }
    }
"""

@pytest.mark.django_db
class TestPostSchema(TestCase):
    def setUp(self):
        self.client = Client
        self.post = mixer.blend(Post)

    def test_post_list_query(self):
        mixer.blend(Post)

        response = self.client.execute(post_list_query)
        posts = response.get('data').get('posts')

        assert len(posts)

    def test_post_by_id_query(self):
        response = self.client.execute(post_by_id_query)
        response_post = response.get('data').get('postById')

        assert response_post['id'] == str(self.post.id)

    def test_create_post_mutation(self):
        user = mixer.blend(User)

        payload = {
            "title": "Test create in GraphQL",
            "content": "Testing create post functionality of the Django with GraphQL",
            "userId": user.id
        }

        response = self.client.execute(create_post_mutation, variables={"input": payload})
        post = response.get('data').get('createPost').get('post')
        title = post.get('title')

        assert title == payload['title']

    def test_update_post_mutation(self):
        payload = {
            "id": self.post.id,
            "title": "Test update in GraphQL",
            "content": "Testing update post functionality of the Django with GraphQL"
        }

        response = self.client.execute(update_post_mutation, variables={"input": payload})

        response_post = response.get('data').get('createPost').get('post')
        title = response_post.get('title')

        assert title == payload['title']
        assert title != self.post.title

    def test_delete_post_mutation(self):
        payload = {
            "id": self.post.id
        }

        response = self.client.execute(delete_post_mutation, variables={"input": payload})
        deleted = response.get('data').get('deletePost').get('deleted')

        assert deleted


