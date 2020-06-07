from .fixtures import make_app_client
import pytest


@pytest.mark.parametrize(
    "allow,expected_anon,expected_auth",
    [(None, 200, 200), ({}, 403, 403), ({"id": "root"}, 403, 200),],
)
def test_view_query(allow, expected_anon, expected_auth):
    with make_app_client(
        metadata={
            "databases": {
                "fixtures": {"queries": {"q": {"sql": "select 1 + 1", "allow": allow}}}
            }
        }
    ) as client:
        anon_response = client.get("/fixtures/q")
        assert expected_anon == anon_response.status
        auth_response = client.get(
            "/fixtures/q", cookies={"ds_actor": client.ds.sign({"id": "root"}, "actor")}
        )
        assert expected_auth == auth_response.status


@pytest.mark.parametrize(
    "allow,expected_anon,expected_auth",
    [(None, 200, 200), ({}, 403, 403), ({"id": "root"}, 403, 200),],
)
def test_view_instance(allow, expected_anon, expected_auth):
    with make_app_client(metadata={"allow": allow}) as client:
        for path in (
            "/",
            "/fixtures",
            "/fixtures/compound_three_primary_keys",
            "/fixtures/compound_three_primary_keys/a,a,a",
        ):
            anon_response = client.get(path)
            assert expected_anon == anon_response.status
            auth_response = client.get(
                path, cookies={"ds_actor": client.ds.sign({"id": "root"}, "actor")},
            )
            assert expected_auth == auth_response.status