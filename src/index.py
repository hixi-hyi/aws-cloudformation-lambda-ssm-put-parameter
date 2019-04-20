from cfnprovider import CustomResourceProvider, get_logger, policy
import boto3
import os
logger = get_logger(__name__)
env = os.environ

class Ssm(CustomResourceProvider):
  def init(self):
    self._region = self.get('Region', env.get('AWS_REGION'))
    self._name = self.get('Name')
    self._type = self.get('Type')
    self._value = self.get('Value')

    self._ssm = boto3.client('ssm', region_name=self._region)
    self.response.physical_resource_id = self.id
    self.response.set_data('Name', self._name)
    self.response.set_data('Value', self._value)
  @property
  def id(self):
    return "{}:{}:{}".format(self._region, self._type, self._name)

  def default_deletion_policies(self):
    return ['Delete']

  def ssm_put(self, overwrite=False):
    self._ssm.put_parameter(
      Name=self._name,
      Value=self._value,
      Type=self._type,
      Overwrite=overwrite
    )

  def create(self, policies):
    self.ssm_put(False)

  def update(self, policies):
    self.ssm_put(True)

  def delete(self, policies):
    if policies.has('Retain'):
      return

    try:
      self._ssm.delete_parameter(Name=self._name)
    except Exception as e:
      if policies.has('IgnoreError'):
        return
      raise e

def handler(event, context):
  c = Ssm(event, context)
  c.handle()
