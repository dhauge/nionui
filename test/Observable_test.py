# standard libraries
import logging
import unittest
import uuid

# third party libraries
# None

# local libraries
from nion.ui import Observable


class Archivable(Observable.ManagedObject):
    def __init__(self):
        super(Archivable, self).__init__()
        self.define_property("abc")


class TestObservableClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_archivable_can_read_when_missing_property_keys(self):
        Archivable().read_from_dict(dict())


class ObjectWithUUID(object):

    def __init__(self):
        self.uuid = uuid.uuid4()


class TestManagedObjectContextClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_managed_object_context_calls_register_on_already_registered_object(self):
        global was_registered
        managed_object_context = Observable.ManagedObjectContext()
        object1 = ObjectWithUUID()
        managed_object_context.register(object1)
        was_registered = False
        def registered(object):
            global was_registered
            was_registered = True
        managed_object_context.subscribe(object1.uuid, registered, None)
        self.assertTrue(was_registered)

    def test_managed_object_context_calls_register_when_object_becomes_registered(self):
        global was_registered
        managed_object_context = Observable.ManagedObjectContext()
        object1 = ObjectWithUUID()
        was_registered = False
        def registered(object):
            global was_registered
            was_registered = True
        managed_object_context.subscribe(object1.uuid, registered, None)
        managed_object_context.register(object1)
        self.assertTrue(was_registered)

    def test_managed_object_context_calls_unregister_when_object_becomes_unregistered(self):
        global was_registered
        managed_object_context = Observable.ManagedObjectContext()
        object1 = ObjectWithUUID()
        was_registered = False
        def registered(object):
            global was_registered
            was_registered = True
        def unregistered(object):
            global was_registered
            was_registered = False
        managed_object_context.subscribe(object1.uuid, registered, unregistered)
        managed_object_context.register(object1)
        self.assertTrue(was_registered)
        object1 = None
        self.assertFalse(was_registered)

    def test_managed_object_context_unregister_without_subscription_works(self):
        # this test will only generate extra output in the failure case, which has been fixed
        managed_object_context = Observable.ManagedObjectContext()
        object1 = ObjectWithUUID()
        managed_object_context.register(object1)
        object1 = None

    def test_subscribing_to_publisher_twice_works(self):
        publisher = Observable.Publisher()
        one = list()
        two = list()
        def handle_one(value):
            one.append(value)
        def handle_two(value):
            two.append(value)
        subscription1 = publisher.subscribex(Observable.Subscriber(handle_one))
        subscription2 = publisher.subscribex(Observable.Subscriber(handle_two))
        publisher.notify_next_value(5)
        self.assertEqual(one, [5, ])
        self.assertEqual(two, [5, ])
        subscription1.close()
        publisher.notify_next_value(6)
        self.assertEqual(one, [5, ])
        self.assertEqual(two, [5, 6])
        subscription2 = None
        publisher.notify_next_value(7)
        self.assertEqual(one, [5, ])
        self.assertEqual(two, [5, 6])

    def test_subscribing_with_select_works(self):
        publisher = Observable.Publisher()
        one = list()
        def handle_one(value):
            one.append(value)
        subscription1 = publisher.select(lambda x: x*2).subscribex(Observable.Subscriber(handle_one))
        publisher.notify_next_value(5)
        self.assertEqual(one, [10, ])

    def test_subscribing_with_select_twice_works(self):
        publisher = Observable.Publisher()
        one = list()
        two = list()
        def handle_one(value):
            one.append(value)
        def handle_two(value):
            two.append(value)
        subscription1 = publisher.select(lambda x: x*2).subscribex(Observable.Subscriber(handle_one))
        subscription2 = publisher.select(lambda x: x*3).subscribex(Observable.Subscriber(handle_two))
        publisher.notify_next_value(5)
        self.assertEqual(one, [10, ])
        self.assertEqual(two, [15, ])

    def test_subscribing_with_cache_twice_works(self):
        publisher = Observable.Publisher()
        one = list()
        two = list()
        def handle_one(value):
            one.append(value)
        def handle_two(value):
            two.append(value)
        subscription1 = publisher.select(lambda x: x*2).cache().subscribex(Observable.Subscriber(handle_one))
        subscription2 = publisher.select(lambda x: x*3).cache().subscribex(Observable.Subscriber(handle_two))
        publisher.notify_next_value(5)
        self.assertEqual(one, [10, ])
        self.assertEqual(two, [15, ])
        publisher.notify_next_value(5)
        self.assertEqual(one, [10, ])
        self.assertEqual(two, [15, ])
        publisher.notify_next_value(6)
        self.assertEqual(one, [10, 12])
        self.assertEqual(two, [15, 18])


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
