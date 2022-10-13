import factory
from farm_base.models.owner import Owner
import json
from farm_base.models.farm import Farm

class OwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Owner

    name = 'Usuário de Teste 1'
    document = '11111111111'
    document_type = 'CPF'


class FarmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Farm
    name = 'Minha Fazenda'
    geometry = json.dumps({
        "type": "Polygon",
        "coordinates": [
            [
                [
                    -10.93984346235492,
                    -37.5238037109375
                ],
                [
                    -11.02073244690711,
                    -37.48260498046874
                ],
                [
                    -10.94658505651706,
                    -37.43728637695312
                ],
                [
                    -10.93984346235492,
                    -37.5238037109375
                ]
            ]
        ]
    })
    area = 0.0033602770856717796
    centroid = json.dumps({
        "type": "Point",
        "coordinates": [
            -10.9690536552597,
            -37.48123168945312
        ]
    })
    municipality = 'São José'
    state = 'Santa Catarina'
    owner = factory.SubFactory(OwnerFactory)

