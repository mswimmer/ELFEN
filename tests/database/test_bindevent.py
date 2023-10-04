import uuid
import hashlib

from django.test import TestCase
from web.models import SampleMetadata
from analysis.analysis_models.dynamic_analysis import BindEvent, KernelTrace

from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class BindEventTestCase(TestCase):
    databases = {"elfen"}

    @classmethod
    def setUpTestData(cls):
        test_string = b"This is a test"
        cls.md5 = hashlib.md5(test_string).hexdigest()
        cls.sha1 = hashlib.sha1(test_string).hexdigest()
        cls.sha256 = hashlib.sha256(test_string).hexdigest()
        cls.uuid1 = uuid.uuid4()
        cls.sample = SampleMetadata.objects.create(
            md5=cls.md5,
            sha1=cls.sha1,
            sha256=cls.sha256,
            username="test_user"
        )
        cls.kernel_trace = KernelTrace.objects.create()
        BindEvent.objects.create(
            sample=cls.sample,
            kernel_trace=cls.kernel_trace,
            procname=b"test"
        )

    def test_bindevent_get(self):
        """
        This test checks if created BindEvent object can be retrieved
        successfully from the DB.
        """
        event = BindEvent.objects.get(sample=self.sample)
        self.assertEqual(event.sample.sha256, self.sha256)

    def test_bindevent_update(self):
        """
        This test checks if created BindEvent object can be updated
        successfully.
        """
        event = BindEvent.objects.get(sample=self.sample)

        new_procname = b"test2"
        event.procname = new_procname
        event.save()

        event = BindEvent.objects.get(sample=self.sample)
        self.assertEqual(event.procname.tobytes(), new_procname)

    def test_bindevent_delete(self):
        """
        This test checks if an existing BindEvent object can be deleted.
        It should be, since *currently* there are no other db objects referencing
        this BindEvent object.
        """
        event = BindEvent.objects.get(sample=self.sample)
        event.delete()

        try:
            BindEvent.objects.get(sample=self.sample)
            self.fail('BindEvent object not deleted in database')
        except ObjectDoesNotExist:
            pass

    def test_bindevent_foreignkey_sample_cannot_delete(self):
        """
        This test checks if the SampleMetadata object referenced by the BindEvent
        object can be deleted. It should not be, since there is a foreign key constraint
        with on_delete=models.PROTECT.
        """
        sample = SampleMetadata.objects.get(sha256=self.sha256)
        try:
            sample.delete()
            self.fail('SampleMetadata object deleted in database')
        except IntegrityError:
            pass

    def test_bindevent_foreignkey_KernelTrace_delete(self):
        """
        This test checks if the KernelTrace object referenced by the BindEvent
        object can be deleted. It should be, since there is a foreign key constraint
        with on_delete=models.CASCADE.
        """
        event = BindEvent.objects.get(sample=self.sample)
        kernel_trace = event.kernel_trace
        try:
            kernel_trace.delete()
        except IntegrityError:
            self.fail('KernelTrace object not deleted in database')
