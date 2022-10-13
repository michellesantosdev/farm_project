import json

import pytest

from django.test import Client

pytestmark = [pytest.mark.django_db]


def test_must_create_farm(client: Client, owner):
    data_requests = {
        "name": "Minha Fazenda",
        "geometry": json.dumps({
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -10.93984346235492,
                        -37.5238037109375
                    ], [
                        -11.02073244690711,
                        -37.48260498046874
                    ], [
                        -10.94658505651706,
                        -37.43728637695312
                    ], [
                        -10.93984346235492,
                        -37.5238037109375
                    ]
                ]
            ]
        }),
        "municipality": "São José",
        "state": "Santa Catarina",
        "owner": owner.id
    }

    response = client.post(path='/api/v1/farms', data=data_requests)

    assert response.status_code == 201
    assert json.loads(response.content) == {
        'id': 1,
        'name': 'Minha Fazenda',
        'geometry': {'type': 'Polygon', 'coordinates': [[[-37.5238037109375, -10.93984346235492], [-37.48260498046874, -11.02073244690711], [-37.43728637695312, -10.94658505651706], [-37.5238037109375, -10.93984346235492]]]},
        'centroid': {'type': 'Point', 'coordinates': [-37.48123168945313, -10.969053655259698]},
        'area': 0.003360277085671756,
        'municipality': 'São José',
        'state': 'Santa Catarina',
        'owner': 1
    }


def test_should_not_create_farm_without_required_fields(client: Client):
    data_requests = {
        "geometry": json.dumps({
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -10.93984346235492,
                        -37.5238037109375
                    ], [
                        -11.02073244690711,
                        -37.48260498046874
                    ], [
                        -10.94658505651706,
                        -37.43728637695312
                    ], [
                        -10.93984346235492,
                        -37.5238037109375
                    ]
                ]
            ]
        })
    }

    response = client.post(path='/api/v1/farms', data=data_requests)

    assert response.status_code == 400
    assert json.loads(response.content) == {
        'name': ['This field is required.'],
        'municipality': ['This field is required.'],
        'state': ['This field is required.'],
        'owner': ['This field is required.']
    }


def test_must_list_farm_by_filters(client: Client, farm):

    response = client.get(path=f'/api/v1/farms?name={farm.name}&'
                               f'municipality={farm.municipality}&'
                               f'state={farm.state}&'
                               f'id={farm.id}&'
                               f'owner__name={farm.owner.name}&'
                               f'owner__document={farm.owner.document}&'
                               f'owner__document_type={farm.owner.document_type}')

    assert response.status_code == 200
    assert json.loads(response.content) == [{
        'name': 'Minha Fazenda',
        'owner': 1,
        'centroid': {'type': 'Point', 'coordinates': [-37.48123168945312, -10.9690536552597]},
        'area': 0.0033602770856717796,
        'municipality': 'São José',
        'state': 'Santa Catarina'
    }]


def test_must_list_farm_by_id(client: Client, farm):
    response = client.get(path=f'/api/v1/farms/{farm.id}')

    assert response.status_code == 200

    data_response = json.loads(response.content)
    assert data_response['id'] == 1
    assert data_response['owner'] == {
        'id': 1,
        'name': 'Usuário de Teste 1',
        'document': '11111111111',
        'document_type': 'CPF'
    }
    assert data_response['name'] == 'Minha Fazenda'
    assert data_response['geometry'] == {'type': 'Polygon', 'coordinates': [[[-37.5238037109375, -10.93984346235492], [-37.48260498046874, -11.02073244690711], [-37.43728637695312, -10.94658505651706], [-37.5238037109375, -10.93984346235492]]]}
    assert data_response['area'] == 0.0033602770856717796
    assert data_response['centroid'] == {'type': 'Point', 'coordinates': [-37.48123168945312, -10.9690536552597]}
    assert data_response['creation_date'] is not None
    assert data_response['last_modification_date'] is not None
    assert data_response['is_active'] is True
    assert data_response['municipality'] == 'São José'
    assert data_response['state'] == 'Santa Catarina'
