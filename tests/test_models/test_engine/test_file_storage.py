#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
TestFileStorage = file_storage.TestFileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of TestFileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.tfs_f = inspect.getmembers(TestFileStorage, inspect.isfunction)

    def test_pep8_conformance_test_file_storage(self):
        """Test that tests/test_models/test_engine/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_test_file_storage_module_docstring(self):
        """Test for the test_file_storage.py module docstring"""
        self.assertIsNot(TestFileStorage.__doc__, None,
                         "test_file_storage.py needs a docstring")
        self.assertTrue(len(TestFileStorage.__doc__) >= 1,
                        "test_file_storage.py needs a docstring")

    def test_test_file_storage_class_docstring(self):
        """Test for the TestFileStorage class docstring"""
        self.assertIsNot(TestFileStorage.__doc__, None,
                         "TestFileStorage class needs a docstring")
        self.assertTrue(len(TestFileStorage.__doc__) >= 1,
                        "TestFileStorage class needs a docstring")

    def test_tfs_func_docstrings(self):
        """Test for the presence of docstrings in TestFileStorage methods"""
        for func in self.tfs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the TestFileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the TestFileStorage.__objects attr"""
        storage = TestFileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._TestFileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the TestFileStorage.__objects attr"""
        storage = TestFileStorage()
        save = TestFileStorage._TestFileStorage__objects
        TestFileStorage._TestFileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._TestFileStorage__objects)
        TestFileStorage._TestFileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = TestFileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = TestFileStorage._TestFileStorage__objects
        TestFileStorage._TestFileStorage__objects = new_dict
        storage.save()
        TestFileStorage._TestFileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

