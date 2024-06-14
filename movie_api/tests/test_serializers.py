from django.test import TestCase
from django.utils import timezone
from movie_api.models import Movie, Review, UserProfile
from movie_api.serializers import MovieSerializer, ReviewSerializer, UserProfileSerializer

class UserProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.user_attributes = {
            'name': 'John Doe',
            'email': 'john@example.com',
        }
        self.user = UserProfile.objects.create(**self.user_attributes)
        self.serializer = UserProfileSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'email', 'created_on', 'updated_on'])

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.user_attributes['name'])
        self.assertEqual(data['email'], self.user_attributes['email'])

class MovieSerializerTestCase(TestCase):
    def setUp(self):
        self.movie_attributes = {
            'name': 'Test Movie',
            'description': 'A test movie description',
            'movie_type': 'Action',
        }
        self.movie = Movie.objects.create(**self.movie_attributes)
        self.serializer = MovieSerializer(instance=self.movie)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'name', 'description', 'movie_type', 'created_on', 'updated_on', 'reviews'])

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.movie_attributes['name'])
        self.assertEqual(data['description'], self.movie_attributes['description'])
        self.assertEqual(data['movie_type'], self.movie_attributes['movie_type'])

class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(name='John Doe', email='john@example.com')
        self.movie = Movie.objects.create(name='Test Movie', description='Test Description', movie_type='Action')
        self.review_attributes = {
            'user': self.user,
            'movie': self.movie,
            'comment': 'Great movie!',
            'rating': 5,
        }
        self.review = Review.objects.create(**self.review_attributes)
        self.serializer = ReviewSerializer(instance=self.review)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'movie', 'user', 'comment', 'rating', 'created_on', 'updated_on'])

    def test_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['comment'], self.review_attributes['comment'])
        self.assertEqual(data['rating'], self.review_attributes['rating'])
        self.assertEqual(data['user']['name'], self.user.name)
        self.assertEqual(data['movie'], self.movie.id)