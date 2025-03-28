from django.shortcuts import render


def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.my_mapbox_access_token'
    return render(request, 'default.html',
                  {'mapbox_access_token': 'pk.eyJ1IjoiaG9zc2FpbnNoYWgiLCJhIjoiY2s2MmV0czQ3MGRzYzNucHdtanY2bWFlaiJ9.Hse6Yjb3WV73ZkOCbT5ZBA'})