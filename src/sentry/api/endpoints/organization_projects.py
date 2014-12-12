from __future__ import absolute_import

from rest_framework.response import Response

from sentry.api.base import Endpoint
from sentry.api.permissions import assert_perm
from sentry.api.serializers import serialize
from sentry.models import Organization, Project, Team


class OrganizationProjectsEndpoint(Endpoint):
    def get(self, request, organization_id):
        organization = Organization.objects.get_from_cache(id=organization_id)

        assert_perm(organization, request.user, request.auth)

        team_list = Team.objects.get_for_user(
            organization=organization,
            user=request.user,
        )

        project_list = []
        for team in team_list:
            project_list.extend(Project.objects.get_for_user(
                team=team,
                user=request.user,
            ))
        project_list.sort(key=lambda x: x.name)

        return Response(serialize(project_list, request.user))