import unittest
from datetime import datetime
from sqlmodel import Session, SQLModel, create_engine
from app.models.base import BaseModel
from app.services.base import BaseService


# Create a mock model for testing
class TestModel(BaseModel, table=True):
    name: str


class TestBaseService(unittest.TestCase):
    def setUp(self):
        # Create in-memory database for testing
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.service = BaseService(self.session, TestModel)

    def test_create(self):
        model = TestModel(name="test item")
        created = self.service.create(model)
        self.assertIsNotNone(created.id)
        self.assertEqual(created.name, "test item")
        self.assertIsInstance(created.created_at, datetime)
        self.assertIsNone(created.updated_at)

    def test_get(self):
        model = TestModel(name="test item")
        created = self.service.create(model)
        retrieved = self.service.get(created.id)
        self.assertEqual(retrieved.name, "test item")

    def test_update(self):
        model = TestModel(name="test item")
        created = self.service.create(model)
        created.name = "updated item"
        updated = self.service.update(created)
        self.assertEqual(updated.name, "updated item")
        self.assertIsNotNone(updated.updated_at)

    def test_delete(self):
        model = TestModel(name="test item")
        created = self.service.create(model)
        self.service.delete(created)
        retrieved = self.service.get(created.id)
        self.assertIsNone(retrieved)

    def test_fetch(self):
        for i in range(5):
            self.service.create(TestModel(name=f"item {i}"))
        items = self.service.fetch(limit=3)
        self.assertEqual(len(items), 3)

    def test_count(self):
        for i in range(5):
            self.service.create(TestModel(name=f"item {i}"))
        count = self.service.count()
        self.assertEqual(count, 5)


if __name__ == "__main__":
    unittest.main()
