from django.db import migrations
from django.db.models import Q

ROOM_IMAGE_MAP = {
    "single": [("101", "rooms/single1.jpg"), ("102", "rooms/single2.jpg"),
               ("103", "rooms/single1.jpg"), ("104", "rooms/single2.jpg")],
    "double": [("201", "rooms/double1.jpg"), ("202", "rooms/double2.jpg"),
               ("203", "rooms/double1.jpg")],
    "suite":  [("301", "rooms/suite1.jpg"),  ("302", "rooms/suite2.jpg"),
               ("303", "rooms/suite1.jpg")],
}


def assign_room_images(apps, schema_editor):
    Room = apps.get_model("HotelApp", "Room")
    for room_type, assignments in ROOM_IMAGE_MAP.items():
        for room_number, image_path in assignments:
            Room.objects.filter(
                room_number=room_number
            ).filter(
                Q(image="") | Q(image__isnull=True)
            ).update(image=image_path)


def remove_room_images(apps, schema_editor):
    Room = apps.get_model("HotelApp", "Room")
    for room_type, assignments in ROOM_IMAGE_MAP.items():
        for room_number, image_path in assignments:
            Room.objects.filter(room_number=room_number, image=image_path).update(image="")


class Migration(migrations.Migration):
    dependencies = [
        ("HotelApp", "0007_seed_initial_rooms"),
    ]

    operations = [
        migrations.RunPython(assign_room_images, remove_room_images),
    ]
