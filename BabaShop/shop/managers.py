from django.db import models


class DeletedShop(models.Manager):
    def get_queryset(self):
        return super(DeletedShop, self).get_queryset().filter(is_deleted=True)


class UndeletedShop(models.Manager):
    def get_queryset(self):
        return super(UndeletedShop, self).get_queryset().filter(is_deleted=False)

