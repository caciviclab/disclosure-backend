from rest_framework import serializers
from ..models import Ballot, BallotItem, Candidate, Office, OfficeElection, Referendum
from _django_utils import ExtendedModelSerializer


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office


class ReferendumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referendum
        exclude = ('ballot',)


class OfficeElectionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True)

    class Meta:
        model = OfficeElection
        exclude = ('ballot', 'office')

    def to_representation(self, obj):
        office = OfficeSerializer(obj.office).data
        office_election = super(OfficeElectionSerializer, self).to_representation(obj)
        office.update(office_election)
        return office


class BallotItemSerializer(serializers.ModelSerializer):
    contest_type = serializers.CharField(source='get_contest_type_display')

    def to_representation(self, obj):
        ballot_item = super(BallotItemSerializer, self).to_representation(obj)
        subclass_data = dict()
        if obj.contest_type == 'R':
            subclass_data = ReferendumSerializer(obj.referendum).data
        elif obj.contest_type == 'O':
            subclass_data = OfficeElectionSerializer(obj.officeelection).data

        subclass_data.update(ballot_item)
        return subclass_data

    class Meta:
        model = BallotItem
        exclude = ('ballot',)


class BallotSerializer(ExtendedModelSerializer):
    ballot_items = BallotItemSerializer(many=True, read_only=True)

    class Meta:
        model = Ballot
        rename = dict(locality='locality_id')
