import pytest
from farm_base.models.owner import Owner
from farm_base.models.farm import Farm


pytestmark = [pytest.mark.django_db]


def test_must_create_owner(owner):
    assert Owner.objects.count() == 1
    assert owner.name == 'Usuário de Teste 1'
    assert owner.document == '11111111111'
    assert owner.document_type == 'CPF'
    assert owner.is_active is True


def test_must_create_farm(farm, owner):
    assert Farm.objects.count() == 1
    assert farm.name == 'Minha Fazenda'
    assert farm.area == 0.0033602770856717796
    assert farm.is_active is True
    assert farm.municipality == 'São José'
    assert farm.state == 'Santa Catarina'
    assert farm.owner == owner
