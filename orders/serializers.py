from games.serializers import GameSerializer
from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'price': instance.price,
            'key': instance.key if instance.status == 3 else None,
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
        }
