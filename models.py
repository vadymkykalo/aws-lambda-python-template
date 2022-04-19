from infi.clickhouse_orm import Model, StringField, DateTimeField, MergeTree, \
    NullableField, F, UUIDField


class Test(Model):
    id = UUIDField()
    name = NullableField(StringField())
    create_at = DateTimeField()

    engine = MergeTree(order_by=('create_at',), partition_key=(F.toYYYYMM(create_at),))
