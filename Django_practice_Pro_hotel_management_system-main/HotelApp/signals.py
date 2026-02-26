from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OnlineBooking, OfflineBooking, Room


# When booking is created → mark room occupied
@receiver(post_save, sender=OnlineBooking)
def mark_room_occupied_online(sender, instance, created, **kwargs):
    if created:
        instance.room.status = 'occupied'
        instance.room.save()


@receiver(post_save, sender=OfflineBooking)
def mark_room_occupied_offline(sender, instance, created, **kwargs):
    if created:
        instance.room.status = 'occupied'
        instance.room.save()


# When booking is deleted → mark room available
@receiver(post_delete, sender=OnlineBooking)
def mark_room_available_online(sender, instance, **kwargs):
    instance.room.status = 'available'
    instance.room.save()


@receiver(post_delete, sender=OfflineBooking)
def mark_room_available_offline(sender, instance, **kwargs):
    instance.room.status = 'available'
    instance.room.save()