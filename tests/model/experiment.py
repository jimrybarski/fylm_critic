from model.experiment import ExperimentFiles
from model.device import Device
from model import version
import unittest


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        self.experiment = ExperimentFiles(Device.ORIGINAL_FYLM, "/tmp")

    def test_file_paths(self):
        self.experiment.add_image_file("FYLM-141111-001.nd2")
        self.assertEqual(self.experiment.database_file, "/tmp/141111.sqlite")
        self.assertEqual(self.experiment.metadata_file, "/tmp/141111.json")
        self.assertEqual(self.experiment.binary_data_file, "/tmp/141111.h5")

    def test_add_image(self):
        self.experiment.add_image_file("FYLM-141111-001.nd2")
        self.assertEqual(self.experiment.date, '141111')

    def test_image_files(self):
        self.experiment.add_image_file("FYLM-141111-001.nd2")
        self.experiment.add_image_file("FYLM-141111-003.nd2")
        self.experiment.add_image_file("FYLM-141111-002.nd2")
        expected = ['/tmp/FYLM-141111-001.nd2',
                    '/tmp/FYLM-141111-002.nd2',
                    '/tmp/FYLM-141111-003.nd2']
        actual = list(self.experiment.image_filenames)
        self.assertListEqual(expected, actual)

    def test_invalid_images(self):
        self.experiment.add_image_file("test.nd2")
        self.experiment.add_image_file("FYLM-141111-001.nd2")
        self.experiment.add_image_file("FYLM-141111-003.nd2")
        self.experiment.add_image_file("FYLM-141111-003-shortened.nd2")
        self.experiment.add_image_file("FYLM-141111-002.nd2")
        expected = ['/tmp/FYLM-141111-001.nd2',
                    '/tmp/FYLM-141111-002.nd2',
                    '/tmp/FYLM-141111-003.nd2']
        actual = list(self.experiment.image_filenames)
        self.assertListEqual(expected, actual)

    def test_must_add_image(self):
        with self.assertRaises(ValueError):
            date = self.experiment.date

    def test_set_metadata(self):
        self.experiment.set_metadata({"version": "0.3.2"})
        self.assertEqual(self.experiment.version, "0.3.2")

    def test_set_metadata_no_given_version(self):
        self.experiment.set_metadata({})
        self.assertEqual(self.experiment.version, version)

    def test_version_default(self):
        self.assertEqual(self.experiment.version, version)
