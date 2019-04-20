from unittest import TestCase
from moto import mock_ssm
from src.index import Ssm
import cfntest
import boto3

def get_ssm(name):
  ssm = boto3.client('ssm')
  return ssm.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']

class TestScenario(TestCase):
  @mock_ssm
  def test_default(self):
    context = cfntest.get_context()
    create_event = cfntest.get_create_event({"Name":"/test/demo", "Type":"SecureString", "Value": "secret"})
    update_event = cfntest.get_update_event({"Name":"/test/demo", "Type":"SecureString", "Value": "secret2"}, cfntest.get_properties(create_event))
    delete_event = cfntest.get_delete_event(cfntest.get_properties(update_event), cfntest.get_properties(create_event))

    if True:
      c = Ssm(create_event, context)
      c.run()
      self.assertEqual(get_ssm("/test/demo"), "secret")

    if True:
      c = Ssm(update_event, context)
      c.run()
      self.assertEqual(get_ssm("/test/demo"), "secret2")

    if True:
      c = Ssm(delete_event, context)
      c.run()
      with self.assertRaises(Exception):
        get_ssm("/test/demo")
