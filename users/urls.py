from users.views import ProfessionViewSet, UserViewSet

routeList = (
    (r'professions', ProfessionViewSet),
    (r'users', UserViewSet)
)