from __future__ import annotations

import argparse
import os
import sys
import subprocess
import textwrap
import time
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT_DIR = Path("/Users/eniholla/Desktop/Projects/hotel-management-system")
PROJECT_DIR = ROOT_DIR / "Django_practice_Pro_hotel_management_system-main"
ASSET_DIR = ROOT_DIR / "documentation" / "assets"
SCREENSHOT_DIR = ASSET_DIR / "screenshots"
FLOWCHART_DIR = ASSET_DIR / "flowcharts"
DIAGRAM_DIR = ASSET_DIR / "diagrams"
PAGE_EXPORT_DIR = ASSET_DIR / "pages"
DEMO_DB_PATH = ASSET_DIR / "documentation_demo.sqlite3"


def load_font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def ensure_directories() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    FLOWCHART_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)
    PAGE_EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def configure_django(database_path: Path) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HotelManagementSystem.settings")
    os.environ["DATABASE_URL"] = f"sqlite:///{database_path}"
    os.environ.setdefault("IOT_MONITOR_AUTOSTART", "0")
    os.environ.setdefault("IOT_ALERT_SMS_ENABLED", "0")
    os.environ.setdefault("IOT_ALERT_EMAIL_ENABLED", "0")
    if str(PROJECT_DIR) not in sys.path:
        sys.path.insert(0, str(PROJECT_DIR))


def seed_demo_database(database_path: Path, *, reset: bool = True) -> None:
    ensure_directories()
    if reset and database_path.exists():
        database_path.unlink()

    configure_django(database_path)

    import django

    django.setup()

    from django.core.management import call_command
    from django.utils import timezone
    from HotelApp.models import (
        ActivityLog,
        Authorregis,
        Employee,
        HousekeepingTask,
        OfflineBooking,
        OnlineBooking,
        Payment,
        Room,
        Salary,
    )
    from alerts.models import AlertNotification, IoTDevice, RoomConditionAlert, SensorReading
    from alerts.services import ensure_iot_devices, record_sensor_payload

    call_command("migrate", interactive=False, verbosity=0)

    # Clear seeded content if the caller chooses not to reset the database file.
    AlertNotification.objects.all().delete()
    RoomConditionAlert.objects.all().delete()
    SensorReading.objects.all().delete()
    IoTDevice.objects.all().delete()
    HousekeepingTask.objects.all().delete()
    Payment.objects.all().delete()
    OnlineBooking.objects.all().delete()
    OfflineBooking.objects.all().delete()
    Salary.objects.all().delete()
    Employee.objects.all().delete()
    ActivityLog.objects.all().delete()
    Room.objects.all().delete()
    Authorregis.objects.all().delete()

    today = timezone.localdate()
    now = timezone.now()

    admin = Authorregis.objects.create_superuser(
        email="admin.demo@rosegold.com",
        password="AdminDemo123!",
        first_name="Adebayo",
        last_name="Akinsola",
        phone_number="+2348012345670",
    )
    receptionist = Authorregis.objects.create_user(
        email="reception.demo@rosegold.com",
        password="ReceptionDemo123!",
        first_name="Grace",
        last_name="Okafor",
        phone_number="+2348012345671",
        is_receptionist=True,
        is_staff=False,
    )
    guest = Authorregis.objects.create_user(
        email="guest.demo@example.com",
        password="GuestDemo123!",
        first_name="Daniel",
        last_name="Olaoye",
        phone_number="+2348012345672",
    )
    vip_guest = Authorregis.objects.create_user(
        email="vip.demo@example.com",
        password="GuestDemo123!",
        first_name="Amara",
        last_name="Nwosu",
        phone_number="+2348012345673",
    )

    image_names = [
        "rooms/single1.jpg",
        "rooms/single2.jpg",
        "rooms/double1.jpg",
        "rooms/double2.jpg",
        "rooms/suite1.jpg",
        "rooms/suite2.jpg",
    ]

    room_specs = [
        ("101", "single", 1, "WiFi, AC, TV, Work Desk", Decimal("15000.00"), "occupied", "clean"),
        ("102", "single", 1, "WiFi, AC, Smart TV, Breakfast", Decimal("18000.00"), "reserved", "clean"),
        ("103", "single", 1, "WiFi, AC, Garden View", Decimal("16000.00"), "available", "clean"),
        ("104", "single", 1, "WiFi, AC, Reading Desk", Decimal("20000.00"), "available", "dirty"),
        ("201", "double", 2, "WiFi, AC, Mini Bar, Balcony", Decimal("35000.00"), "occupied", "clean"),
        ("202", "double", 2, "WiFi, AC, Twin Beds, Mini Fridge", Decimal("42000.00"), "reserved", "clean"),
        ("203", "double", 2, "WiFi, AC, Smart Lock, Work Area", Decimal("60000.00"), "maintenance", "in_progress"),
        ("301", "suite", 3, "WiFi, Jacuzzi, King Bed, Lounge", Decimal("85000.00"), "available", "clean"),
        ("302", "suite", 3, "WiFi, Ocean View, Butler Service", Decimal("120000.00"), "reserved", "clean"),
        ("303", "suite", 3, "WiFi, Private Lounge, Smart Lighting", Decimal("95000.00"), "available", "clean"),
    ]

    rooms: dict[str, Room] = {}
    for index, spec in enumerate(room_specs):
        room_number, room_type, floor, facility, price, status, housekeeping = spec
        room = Room.objects.create(
            room_number=room_number,
            room_type=room_type,
            floor=floor,
            facility=facility,
            price=price,
            status=status,
            housekeeping_status=housekeeping,
            image=image_names[index % len(image_names)],
            last_cleaned=now - timedelta(hours=index + 2),
        )
        rooms[room_number] = room

    housekeeping_staff = Employee.objects.create(
        employee_id="EMP-001",
        first_name="Janet",
        last_name="Akinyemi",
        email="janet.housekeeping@rosegold.com",
        mobile_number="+2348015550001",
        joining_date=today - timedelta(days=400),
        date_of_birth=today - timedelta(days=11_000),
        department="Housekeeping",
        gender="Female",
        blood_group="O+",
        education="ND Hospitality Management",
        guardian="Mr. Akinyemi",
        guardian_number="+2348015550002",
        image="employees/WhatsApp_Image_2026-03-23_at_16.07.02.jpeg",
        address="15 Heritage Estate, Lagos",
    )
    front_desk_staff = Employee.objects.create(
        employee_id="EMP-002",
        first_name="Musa",
        last_name="Danjuma",
        email="musa.frontdesk@rosegold.com",
        mobile_number="+2348015550003",
        joining_date=today - timedelta(days=250),
        date_of_birth=today - timedelta(days=10_500),
        department="Front Desk",
        gender="Male",
        blood_group="A+",
        education="B.Sc. Computer Science",
        guardian="Mrs. Danjuma",
        guardian_number="+2348015550004",
        image="employees/WhatsApp_Image_2026-03-23_at_16.07.02.jpeg",
        address="7 Victoria Garden City, Lagos",
    )
    Salary.objects.create(employee=housekeeping_staff, salary=Decimal("95000.00"))
    Salary.objects.create(employee=front_desk_staff, salary=Decimal("110000.00"))

    online_checkout = OnlineBooking.objects.create(
        user=guest,
        room=rooms["101"],
        check_in=today - timedelta(days=2),
        check_out=today,
        adults=2,
        children=0,
        city="Lagos",
        country="Nigeria",
        address="17 Adeola Odeku Street, Victoria Island",
        status="checked_in",
        checked_in_at=now - timedelta(days=2),
        is_vip=False,
    )
    online_arrival = OnlineBooking.objects.create(
        user=vip_guest,
        room=rooms["102"],
        check_in=today,
        check_out=today + timedelta(days=3),
        adults=2,
        children=1,
        city="Abuja",
        country="Nigeria",
        address="22 Gana Street, Maitama",
        status="confirmed",
        is_vip=True,
    )
    online_future = OnlineBooking.objects.create(
        user=guest,
        room=rooms["302"],
        check_in=today + timedelta(days=5),
        check_out=today + timedelta(days=8),
        adults=2,
        children=0,
        city="Ibadan",
        country="Nigeria",
        address="9 Ring Road, Ibadan",
        status="confirmed",
        is_vip=False,
    )

    offline_checkout = OfflineBooking.objects.create(
        room=rooms["201"],
        first_name="Tunde",
        last_name="Balogun",
        email="tunde.balogun@example.com",
        mobile_number="+2348090000001",
        check_in=today - timedelta(days=1),
        check_out=today,
        adults=2,
        children=0,
        country="Nigeria",
        address="Lekki Phase 1, Lagos",
        status="checked_in",
        checked_in_at=now - timedelta(days=1),
    )
    offline_arrival = OfflineBooking.objects.create(
        room=rooms["202"],
        first_name="Chioma",
        last_name="Eze",
        email="chioma.eze@example.com",
        mobile_number="+2348090000002",
        check_in=today,
        check_out=today + timedelta(days=2),
        adults=1,
        children=0,
        country="Nigeria",
        address="GRA, Port Harcourt",
        status="confirmed",
    )

    Payment.objects.create(
        booking_type="online",
        booking_id=online_arrival.id,
        amount=online_arrival.get_total_amount(),
        payment_method="paystack",
        payment_status="paid",
        receipt_number="HMS-DEMO-PAID-001",
        paystack_reference="HMS-DEMO-PAID-001",
        paid_at=now - timedelta(hours=3),
        created_by=guest,
    )
    Payment.objects.create(
        booking_type="offline",
        booking_id=offline_checkout.id,
        amount=offline_checkout.get_total_amount(),
        payment_method="cash",
        payment_status="paid",
        receipt_number="HMS-DEMO-PAID-002",
        paid_at=now - timedelta(hours=1),
        created_by=receptionist,
    )
    Payment.objects.create(
        booking_type="offline",
        booking_id=offline_arrival.id,
        amount=offline_arrival.get_total_amount(),
        payment_method="transfer",
        payment_status="pending",
        receipt_number="HMS-DEMO-PENDING-001",
        created_by=receptionist,
    )

    HousekeepingTask.objects.create(
        room=rooms["104"],
        status="pending",
        priority="urgent",
        assigned_to=housekeeping_staff,
        notes="Guest requested express turnaround before afternoon check-in.",
        created_by=receptionist,
    )
    HousekeepingTask.objects.create(
        room=rooms["203"],
        status="in_progress",
        priority="high",
        assigned_to=housekeeping_staff,
        notes="Room inspection tied to maintenance and safety review.",
        created_by=admin,
        started_at=now - timedelta(minutes=45),
    )

    ActivityLog.objects.create(
        user=guest,
        action_type="booking_created",
        description="Created an online reservation for Room 102 after a successful Paystack payment.",
        booking_type="online",
        booking_id=online_arrival.id,
        room=rooms["102"],
    )
    ActivityLog.objects.create(
        user=receptionist,
        action_type="payment_received",
        description="Recorded a desk payment for Room 201 at checkout.",
        booking_type="offline",
        booking_id=offline_checkout.id,
        room=rooms["201"],
    )
    ActivityLog.objects.create(
        user=receptionist,
        action_type="room_status_changed",
        description="Updated Room 104 to dirty pending express housekeeping.",
        room=rooms["104"],
    )
    ActivityLog.objects.create(
        user=admin,
        action_type="housekeeping_assigned",
        description="Assigned a high-priority housekeeping review for Room 203.",
        room=rooms["203"],
    )

    devices = ensure_iot_devices()
    device_by_room = {device.room.room_number: device for device in devices}

    for room_number, room in rooms.items():
        device = device_by_room[room_number]
        if room_number == "203":
            record_sensor_payload(
                device,
                {
                    "temperature_c": 33.8,
                    "gas_level": 138,
                    "motion_state": "brief",
                    "occupancy_expected": True,
                    "recorded_at": now - timedelta(minutes=2),
                },
            )
        elif room_number == "104":
            record_sensor_payload(
                device,
                {
                    "temperature_c": 24.3,
                    "gas_level": 16,
                    "motion_state": "active",
                    "occupancy_expected": False,
                    "recorded_at": now - timedelta(minutes=1),
                },
            )
        elif room_number == "102":
            record_sensor_payload(
                device,
                {
                    "temperature_c": 27.9,
                    "gas_level": 22,
                    "motion_state": "brief",
                    "occupancy_expected": False,
                    "recorded_at": now - timedelta(minutes=3),
                },
            )
        else:
            record_sensor_payload(
                device,
                {
                    "temperature_c": 22.1,
                    "gas_level": 14,
                    "motion_state": "idle",
                    "occupancy_expected": room.status in {"occupied", "maintenance"},
                    "recorded_at": now - timedelta(minutes=4),
                },
            )

    print(f"Seeded documentation demo database at {database_path}")
    print("Admin: admin.demo@rosegold.com / AdminDemo123!")
    print("Receptionist: reception.demo@rosegold.com / ReceptionDemo123!")
    print("Guest: guest.demo@example.com / GuestDemo123!")


@dataclass
class FlowStep:
    title: str
    subtitle: str = ""
    kind: str = "process"


@dataclass(frozen=True)
class EntityBox:
    key: str
    title: str
    fields: list[str]
    x: int
    y: int
    width: int = 430
    accent: str = "#dbeafe"
    border: str = "#1d4ed8"


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test_line = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= width or not current:
            current = test_line
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_arrow(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, color: str) -> None:
    draw.line((x, y1, x, y2), fill=color, width=5)
    draw.polygon([(x - 12, y2 - 10), (x + 12, y2 - 10), (x, y2 + 12)], fill=color)


def draw_flowchart(feature: str, steps: list[FlowStep], output_path: Path) -> None:
    width = 1500
    height = max(900, 210 + (len(steps) * 170))
    image = Image.new("RGB", (width, height), "#f8fafc")
    draw = ImageDraw.Draw(image)

    title_font = load_font(44, bold=True)
    label_font = load_font(24, bold=True)
    body_font = load_font(18)

    draw.rounded_rectangle((40, 40, width - 40, height - 40), radius=28, outline="#dbe4f0", width=4, fill="#ffffff")
    draw.text((70, 70), f"{feature} Feature Flowchart", font=title_font, fill="#0f172a")
    draw.text((70, 128), "Documentation visual for Chapter 4 implementation discussion", font=body_font, fill="#64748b")

    center_x = width // 2
    top = 210
    box_w = 860
    box_h = 104
    colors = {
        "start": ("#e0f2fe", "#0c4a6e"),
        "process": ("#fef3c7", "#92400e"),
        "decision": ("#fee2e2", "#991b1b"),
        "end": ("#dcfce7", "#166534"),
    }

    for index, step in enumerate(steps):
        y = top + (index * 150)
        fill, border = colors.get(step.kind, colors["process"])

        if step.kind == "decision":
            cx, cy = center_x, y + (box_h // 2)
            diamond = [(cx, y - 10), (cx + 160, cy), (cx, y + box_h + 10), (cx - 160, cy)]
            draw.polygon(diamond, fill=fill, outline=border)
            text_width = 250
            title_y = y + 8
        elif step.kind in {"start", "end"}:
            draw.ellipse((center_x - (box_w // 2), y, center_x + (box_w // 2), y + box_h), fill=fill, outline=border, width=3)
            text_width = box_w - 120
            title_y = y + 18
        else:
            draw.rounded_rectangle(
                (center_x - (box_w // 2), y, center_x + (box_w // 2), y + box_h),
                radius=24,
                fill=fill,
                outline=border,
                width=3,
            )
            text_width = box_w - 120
            title_y = y + 16

        title_lines = wrap_text(draw, step.title, label_font, text_width)
        current_y = title_y
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=label_font)
            draw.text((center_x - ((bbox[2] - bbox[0]) // 2), current_y), line, font=label_font, fill="#111827")
            current_y += 28

        if step.subtitle and step.kind != "decision":
            subtitle_lines = wrap_text(draw, step.subtitle, body_font, text_width)
            for line in subtitle_lines[:2]:
                bbox = draw.textbbox((0, 0), line, font=body_font)
                draw.text((center_x - ((bbox[2] - bbox[0]) // 2), current_y + 4), line, font=body_font, fill="#475569")
                current_y += 22

        if index < len(steps) - 1:
            draw_arrow(draw, center_x, y + box_h + 8, y + 138, "#94a3b8")

    image.save(output_path)


def draw_polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[int, int]],
    *,
    color: str,
    width: int = 4,
    dashed: bool = False,
) -> None:
    if len(points) < 2:
        return

    if not dashed:
        draw.line(points, fill=color, width=width, joint="curve")
        return

    dash_length = 18
    gap_length = 12

    for start, end in zip(points, points[1:]):
        x1, y1 = start
        x2, y2 = end
        if x1 == x2:
            step = 1 if y2 >= y1 else -1
            distance = abs(y2 - y1)
            position = 0
            while position < distance:
                seg_start = y1 + (position * step)
                seg_end = y1 + (min(position + dash_length, distance) * step)
                draw.line((x1, seg_start, x2, seg_end), fill=color, width=width)
                position += dash_length + gap_length
        elif y1 == y2:
            step = 1 if x2 >= x1 else -1
            distance = abs(x2 - x1)
            position = 0
            while position < distance:
                seg_start = x1 + (position * step)
                seg_end = x1 + (min(position + dash_length, distance) * step)
                draw.line((seg_start, y1, seg_end, y2), fill=color, width=width)
                position += dash_length + gap_length
        else:
            draw.line((x1, y1, x2, y2), fill=color, width=width)


def entity_height(entity: EntityBox) -> int:
    return 78 + (len(entity.fields) * 27) + 26


def entity_anchor(entity: EntityBox, side: str) -> tuple[int, int]:
    height = entity_height(entity)
    if side == "left":
        return (entity.x, entity.y + (height // 2))
    if side == "right":
        return (entity.x + entity.width, entity.y + (height // 2))
    if side == "top":
        return (entity.x + (entity.width // 2), entity.y)
    if side == "bottom":
        return (entity.x + (entity.width // 2), entity.y + height)
    raise ValueError(f"Unsupported side: {side}")


def draw_entity_box(
    draw: ImageDraw.ImageDraw,
    entity: EntityBox,
    title_font: ImageFont.ImageFont,
    body_font: ImageFont.ImageFont,
) -> None:
    height = entity_height(entity)
    draw.rounded_rectangle(
        (entity.x, entity.y, entity.x + entity.width, entity.y + height),
        radius=26,
        fill="#ffffff",
        outline=entity.border,
        width=4,
    )
    draw.rounded_rectangle(
        (entity.x, entity.y, entity.x + entity.width, entity.y + 64),
        radius=26,
        fill=entity.accent,
        outline=entity.border,
        width=4,
    )
    draw.rectangle(
        (entity.x, entity.y + 40, entity.x + entity.width, entity.y + 64),
        fill=entity.accent,
        outline=entity.accent,
    )

    title_bbox = draw.textbbox((0, 0), entity.title, font=title_font)
    title_x = entity.x + ((entity.width - (title_bbox[2] - title_bbox[0])) // 2)
    draw.text((title_x, entity.y + 16), entity.title, font=title_font, fill="#0f172a")

    current_y = entity.y + 82
    for field in entity.fields:
        draw.text((entity.x + 22, current_y), field, font=body_font, fill="#334155")
        current_y += 27


def draw_relationship(
    draw: ImageDraw.ImageDraw,
    entities: dict[str, EntityBox],
    source_key: str,
    target_key: str,
    *,
    source_side: str,
    target_side: str,
    source_cardinality: str,
    target_cardinality: str,
    label: str = "",
    color: str = "#64748b",
    dashed: bool = False,
    waypoints: list[tuple[int, int]] | None = None,
    label_offset: tuple[int, int] = (0, 0),
    card_offset: int = 18,
    font: ImageFont.ImageFont,
) -> None:
    source = entities[source_key]
    target = entities[target_key]
    start = entity_anchor(source, source_side)
    end = entity_anchor(target, target_side)
    points = [start, *(waypoints or []), end]
    draw_polyline(draw, points, color=color, width=4, dashed=dashed)

    sx, sy = start
    tx, ty = end

    if source_side == "left":
        source_pos = (sx - (card_offset + 12), sy - 22)
    elif source_side == "right":
        source_pos = (sx + 12, sy - 22)
    elif source_side == "top":
        source_pos = (sx - 12, sy - (card_offset + 26))
    else:
        source_pos = (sx - 12, sy + 6)

    if target_side == "left":
        target_pos = (tx - (card_offset + 12), ty - 22)
    elif target_side == "right":
        target_pos = (tx + 12, ty - 22)
    elif target_side == "top":
        target_pos = (tx - 16, ty - (card_offset + 26))
    else:
        target_pos = (tx - 16, ty + 6)

    draw.text(source_pos, source_cardinality, font=font, fill="#0f172a")
    draw.text(target_pos, target_cardinality, font=font, fill="#0f172a")

    if label:
        label_point = points[len(points) // 2]
        draw.text(
            (label_point[0] + label_offset[0], label_point[1] + label_offset[1]),
            label,
            font=font,
            fill=color,
        )


def generate_erd_diagram() -> None:
    ensure_directories()

    width = 2460
    height = 1600
    image = Image.new("RGB", (width, height), "#f8fafc")
    draw = ImageDraw.Draw(image)

    title_font = load_font(44, bold=True)
    subtitle_font = load_font(22)
    group_font = load_font(24, bold=True)
    entity_title_font = load_font(23, bold=True)
    entity_body_font = load_font(18)
    relation_font = load_font(17, bold=True)
    note_font = load_font(18)

    draw.rounded_rectangle((30, 30, width - 30, height - 30), radius=28, outline="#dbe4f0", width=4, fill="#ffffff")
    draw.text((70, 62), "Entity-Relationship Diagram of the Hotel Management System", font=title_font, fill="#0f172a")
    draw.text(
        (70, 118),
        "Chapter 3 data design view showing the live Django entities that support reservations, operations, and IoT monitoring.",
        font=subtitle_font,
        fill="#475569",
    )

    panels = [
        ((55, 180, 630, 1550), "#eff6ff", "#bfdbfe", "Core Identity and Inventory"),
        ((665, 180, 1240, 1550), "#fffbeb", "#fde68a", "Reservations and Rooms"),
        ((1275, 180, 1850, 1550), "#f8fafc", "#cbd5e1", "Operations and Payments"),
        ((1885, 180, 2405, 1550), "#ecfeff", "#a5f3fc", "Monitoring and Alerts"),
    ]
    for (x1, y1, x2, y2), fill, border, label in panels:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=24, fill=fill, outline=border, width=3)
        draw.text((x1 + 22, y1 + 18), label, font=group_font, fill="#0f172a")

    entities = {
        "author": EntityBox(
            key="author",
            title="Authorregis",
            fields=[
                "PK id",
                "email (unique)",
                "phone_number",
                "is_staff",
                "is_receptionist",
            ],
            x=95,
            y=260,
            accent="#dbeafe",
            border="#2563eb",
        ),
        "employee": EntityBox(
            key="employee",
            title="Employee",
            fields=[
                "PK employee_id",
                "email (unique)",
                "mobile_number (unique)",
                "department",
                "joining_date",
            ],
            x=95,
            y=975,
            accent="#dbeafe",
            border="#2563eb",
        ),
        "salary": EntityBox(
            key="salary",
            title="Salary",
            fields=[
                "PK id",
                "FK employee_id -> Employee",
                "salary",
            ],
            x=95,
            y=1265,
            accent="#dbeafe",
            border="#2563eb",
        ),
        "online_booking": EntityBox(
            key="online_booking",
            title="OnlineBooking",
            fields=[
                "PK id",
                "FK user_id -> Authorregis",
                "FK room_id -> Room",
                "check_in / check_out",
                "status",
                "is_vip",
            ],
            x=700,
            y=250,
            accent="#fef3c7",
            border="#d97706",
        ),
        "room": EntityBox(
            key="room",
            title="Room",
            fields=[
                "PK id",
                "room_number (unique)",
                "room_type",
                "price",
                "status",
                "housekeeping_status",
            ],
            x=700,
            y=610,
            accent="#fef3c7",
            border="#d97706",
        ),
        "offline_booking": EntityBox(
            key="offline_booking",
            title="OfflineBooking",
            fields=[
                "PK id",
                "FK room_id -> Room",
                "guest_name / email",
                "check_in / check_out",
                "status",
                "is_vip",
            ],
            x=700,
            y=1060,
            accent="#fef3c7",
            border="#d97706",
        ),
        "activity_log": EntityBox(
            key="activity_log",
            title="ActivityLog",
            fields=[
                "PK id",
                "FK user_id -> Authorregis",
                "FK room_id -> Room?",
                "action_type",
                "booking_type / booking_id",
                "description",
            ],
            x=1310,
            y=250,
            accent="#e2e8f0",
            border="#475569",
        ),
        "housekeeping": EntityBox(
            key="housekeeping",
            title="HousekeepingTask",
            fields=[
                "PK id",
                "FK room_id -> Room",
                "FK assigned_to -> Employee?",
                "FK created_by -> Authorregis?",
                "status",
                "priority",
                "notes",
            ],
            x=1310,
            y=690,
            accent="#e2e8f0",
            border="#475569",
        ),
        "payment": EntityBox(
            key="payment",
            title="Payment",
            fields=[
                "PK id",
                "booking_type",
                "booking_id",
                "FK created_by -> Authorregis?",
                "payment_method / status",
                "receipt_number",
                "paystack_reference",
            ],
            x=1310,
            y=1130,
            accent="#e2e8f0",
            border="#475569",
        ),
        "iot_device": EntityBox(
            key="iot_device",
            title="IoTDevice",
            fields=[
                "PK id",
                "O2O room_id -> Room",
                "device_identifier",
                "is_online",
                "sampling_interval_seconds",
                "last_seen_at",
            ],
            x=1920,
            y=250,
            accent="#cffafe",
            border="#0891b2",
        ),
        "sensor_reading": EntityBox(
            key="sensor_reading",
            title="SensorReading",
            fields=[
                "PK id",
                "FK device_id -> IoTDevice",
                "FK room_id -> Room",
                "temperature_c / gas_level",
                "motion_state",
                "overall_status",
                "recorded_at",
            ],
            x=1920,
            y=610,
            accent="#cffafe",
            border="#0891b2",
        ),
        "room_alert": EntityBox(
            key="room_alert",
            title="RoomConditionAlert",
            fields=[
                "PK id",
                "FK room_id -> Room",
                "FK device_id -> IoTDevice",
                "FK latest_reading_id -> SensorReading?",
                "FK acknowledged_by -> Authorregis?",
                "alert_type / severity",
                "is_active",
                "triggered_at / resolved_at",
            ],
            x=1920,
            y=1015,
            accent="#cffafe",
            border="#0891b2",
        ),
        "alert_notification": EntityBox(
            key="alert_notification",
            title="AlertNotification",
            fields=[
                "PK id",
                "FK alert_id -> RoomConditionAlert",
                "channel / event_type",
                "recipient / status",
                "provider_reference",
            ],
            x=1920,
            y=1335,
            accent="#cffafe",
            border="#0891b2",
        ),
    }

    for entity in entities.values():
        draw_entity_box(draw, entity, entity_title_font, entity_body_font)

    solid = "#64748b"
    logical = "#b45309"

    draw_relationship(
        draw,
        entities,
        "author",
        "online_booking",
        source_side="right",
        target_side="left",
        source_cardinality="1",
        target_cardinality="0..*",
        label="creates",
        color=solid,
        font=relation_font,
        label_offset=(-40, -34),
    )
    draw_relationship(
        draw,
        entities,
        "room",
        "online_booking",
        source_side="top",
        target_side="bottom",
        source_cardinality="1",
        target_cardinality="0..*",
        label="assigned to",
        color=solid,
        font=relation_font,
        label_offset=(28, -12),
    )
    draw_relationship(
        draw,
        entities,
        "room",
        "offline_booking",
        source_side="bottom",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="supports",
        color=solid,
        font=relation_font,
        label_offset=(28, -10),
    )
    draw_relationship(
        draw,
        entities,
        "employee",
        "salary",
        source_side="bottom",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="receives",
        color=solid,
        font=relation_font,
        label_offset=(22, -8),
    )
    draw_relationship(
        draw,
        entities,
        "author",
        "activity_log",
        source_side="top",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="records",
        color=solid,
        waypoints=[(310, 165), (1570, 165)],
        font=relation_font,
        label_offset=(-26, -32),
    )
    draw_relationship(
        draw,
        entities,
        "room",
        "housekeeping",
        source_side="right",
        target_side="left",
        source_cardinality="1",
        target_cardinality="0..*",
        label="needs",
        color=solid,
        font=relation_font,
        label_offset=(-14, -34),
    )
    draw_relationship(
        draw,
        entities,
        "room",
        "iot_device",
        source_side="right",
        target_side="left",
        source_cardinality="1",
        target_cardinality="1",
        label="monitored by",
        color=solid,
        waypoints=[(1835, 726), (1835, 366)],
        font=relation_font,
        label_offset=(-44, -34),
    )
    draw_relationship(
        draw,
        entities,
        "iot_device",
        "sensor_reading",
        source_side="bottom",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="produces",
        color=solid,
        font=relation_font,
        label_offset=(28, -8),
    )
    draw_relationship(
        draw,
        entities,
        "room",
        "sensor_reading",
        source_side="right",
        target_side="left",
        source_cardinality="1",
        target_cardinality="0..*",
        label="context for",
        color=solid,
        waypoints=[(1835, 726), (1835, 726)],
        font=relation_font,
        label_offset=(-60, -34),
    )
    draw_relationship(
        draw,
        entities,
        "sensor_reading",
        "room_alert",
        source_side="bottom",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="may trigger",
        color=solid,
        font=relation_font,
        label_offset=(26, -8),
    )
    draw_relationship(
        draw,
        entities,
        "room_alert",
        "alert_notification",
        source_side="bottom",
        target_side="top",
        source_cardinality="1",
        target_cardinality="0..*",
        label="sends",
        color=solid,
        font=relation_font,
        label_offset=(22, -8),
    )
    draw_relationship(
        draw,
        entities,
        "payment",
        "online_booking",
        source_side="left",
        target_side="right",
        source_cardinality="0..*",
        target_cardinality="0..1",
        label="logical link",
        color=logical,
        dashed=True,
        waypoints=[(1250, 1248), (1250, 360)],
        font=relation_font,
        label_offset=(-40, -34),
    )
    draw_relationship(
        draw,
        entities,
        "payment",
        "offline_booking",
        source_side="left",
        target_side="right",
        source_cardinality="0..*",
        target_cardinality="0..1",
        label="logical link",
        color=logical,
        dashed=True,
        waypoints=[(1250, 1248), (1250, 1166)],
        font=relation_font,
        label_offset=(-44, -34),
    )

    legend_x = 1535
    legend_y = 54
    draw.rounded_rectangle((legend_x, legend_y, legend_x + 470, legend_y + 110), radius=20, fill="#ffffff", outline="#cbd5e1", width=3)
    draw.line((legend_x + 20, legend_y + 34, legend_x + 120, legend_y + 34), fill=solid, width=4)
    draw.text((legend_x + 140, legend_y + 20), "Solid connector = FK / one-to-one relation", font=note_font, fill="#334155")
    draw_polyline(draw, [(legend_x + 20, legend_y + 74), (legend_x + 120, legend_y + 74)], color=logical, width=4, dashed=True)
    draw.text((legend_x + 140, legend_y + 60), "Dashed connector = application-level logical relation", font=note_font, fill="#334155")

    note_text = "Payment uses booking_type and booking_id to point to either OnlineBooking or OfflineBooking, so the payment relation is logical rather than a direct foreign key."
    wrapped = textwrap.wrap(note_text, width=104)
    note_y = 1512
    for line in wrapped:
        draw.text((85, note_y), line, font=note_font, fill="#475569")
        note_y += 24

    image.save(DIAGRAM_DIR / "hotel_system_erd.png")


def generate_flowcharts() -> None:
    ensure_directories()
    charts = {
        "login_flow.png": [
            FlowStep("User opens login page", "The system presents an email-based authentication form.", "start"),
            FlowStep("Credentials are submitted", "Email and password are posted to the Django login view."),
            FlowStep("Role is evaluated", "Guests, admins, and reception staff are redirected differently.", "decision"),
            FlowStep("Role dashboard is loaded", "Guest home, admin dashboard, or receptionist dashboard is shown."),
            FlowStep("Session is established", "Protected routes now use the authenticated session.", "end"),
        ],
        "rooms_flow.png": [
            FlowStep("Guest opens the rooms catalogue", "Public room cards show images, price, status, and facilities.", "start"),
            FlowStep("System retrieves room inventory", "Room records are fetched from the database and ordered."),
            FlowStep("Guest inspects room details", "The room card acts as the main selection point."),
            FlowStep("Preferred room is selected", "The chosen room can be passed into the booking page.", "decision"),
            FlowStep("Booking handoff begins", "The booking form is prefilled with the selected room.", "end"),
        ],
        "booking_flow.png": [
            FlowStep("Guest starts a reservation", "Booking begins from the online booking page.", "start"),
            FlowStep("Stay dates and guest counts are entered", "The UI calculates nights and expected cost."),
            FlowStep("Server validates booking window", "The form checks for invalid dates and room clashes.", "decision"),
            FlowStep("Pending booking is stored in session", "Booking data is held temporarily until payment succeeds."),
            FlowStep("Guest is redirected to payment summary", "The booking is not confirmed yet.", "end"),
        ],
        "payment_flow.png": [
            FlowStep("Payment summary page is displayed", "The user reviews dates, room rate, and total amount.", "start"),
            FlowStep("Paystack transaction is initialized", "The server creates a unique payment reference."),
            FlowStep("User completes checkout on Paystack", "Paystack processes card, transfer, USSD, or wallet payment."),
            FlowStep("Callback verifies the reference", "The server confirms the payment before writing the booking.", "decision"),
            FlowStep("Booking and payment records are finalized", "Room status is updated to reserved and activity is logged.", "end"),
        ],
        "admin_flow.png": [
            FlowStep("Admin opens the custom dashboard", "The interface aggregates operational metrics from the database.", "start"),
            FlowStep("System compiles hotel summaries", "Bookings, users, rooms, staff, revenue, and IoT counters are calculated."),
            FlowStep("Admin reviews live panels", "Quick actions connect room, user, salary, and booking management pages."),
            FlowStep("Admin updates operational records", "CRUD operations modify hotel data through the web interface."),
            FlowStep("Changes appear immediately in the dashboard", "The control panel remains synchronized with live records.", "end"),
        ],
        "receptionist_flow.png": [
            FlowStep("Receptionist signs in", "Front desk staff are redirected to a task-focused dashboard.", "start"),
            FlowStep("Today's arrivals and departures are reviewed", "Check-in and check-out lists are grouped by booking state."),
            FlowStep("Guest or room action is selected", "Staff can open room board, housekeeping, search, or payment tools.", "decision"),
            FlowStep("Operational update is recorded", "Room status, activity logs, and task records are updated immediately."),
            FlowStep("Front desk state refreshes", "Reception sees the latest room occupancy and pending work.", "end"),
        ],
        "iot_flow.png": [
            FlowStep("IoT monitoring cycle runs", "Each room has a logical device mapped to the room inventory.", "start"),
            FlowStep("Sensor payload is generated or received", "Temperature, gas level, and motion state are captured."),
            FlowStep("Rules evaluate room condition", "Thresholds determine whether the room is normal, warning, or critical.", "decision"),
            FlowStep("Alert lifecycle is updated", "New alerts are created and resolved alerts are closed automatically."),
            FlowStep("Admin dashboard and alert center refresh", "The hotel sees current HSE status for every monitored room.", "end"),
        ],
    }

    for filename, steps in charts.items():
        draw_flowchart(filename.replace("_", " ").replace(".png", "").title(), steps, FLOWCHART_DIR / filename)

    generate_erd_diagram()
    print(f"Generated {len(charts)} flowcharts in {FLOWCHART_DIR}")
    print(f"Generated ERD diagram in {DIAGRAM_DIR}")


def rewrite_response_html(html: str, base_url: str) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    base_tag = soup.new_tag("base", href=f"{base_url}/")
    if soup.head:
        soup.head.insert(0, base_tag)

    for tag_name, attribute in (("a", "href"), ("link", "href"), ("img", "src"), ("script", "src"), ("form", "action")):
        for tag in soup.find_all(tag_name):
            value = tag.get(attribute)
            if not value or value.startswith(("http://", "https://", "mailto:", "#", "javascript:", "data:")):
                continue
            if value.startswith("/"):
                tag[attribute] = f"{base_url}{value}"

    return str(soup)


def export_html_pages(base_url: str, database_path: Path) -> None:
    ensure_directories()
    configure_django(database_path)

    import django

    django.setup()

    from django.test import Client
    from django.urls import reverse
    from HotelApp.models import Authorregis, Room

    admin = Authorregis.objects.get(email="admin.demo@rosegold.com")
    receptionist = Authorregis.objects.get(email="reception.demo@rosegold.com")
    guest = Authorregis.objects.get(email="guest.demo@example.com")
    room = Room.objects.get(room_number="103")

    def save_page(name: str, response) -> None:
        html = response.content.decode("utf-8")
        rewritten = rewrite_response_html(html, base_url)
        (PAGE_EXPORT_DIR / name).write_text(rewritten, encoding="utf-8")

    anonymous_client = Client()
    save_page("login_page.html", anonymous_client.get(reverse("author_login")))
    save_page("rooms_page.html", anonymous_client.get(reverse("room_list")))

    guest_client = Client()
    guest_client.force_login(guest)
    save_page("booking_page.html", guest_client.get(f"{reverse('online_booking')}?room={room.id}&new=1"))
    session = guest_client.session
    session["pending_booking"] = {
        "room_id": room.id,
        "check_in": "2026-03-29",
        "check_out": "2026-03-31",
        "adults": 2,
        "children": 1,
        "city": "Lagos",
        "country": "Nigeria",
        "address": "Documentation Demo",
    }
    session.save()
    save_page("payment_page.html", guest_client.get(reverse("booking_payment_page")))

    admin_client = Client()
    admin_client.force_login(admin)
    save_page("admin_dashboard.html", admin_client.get(reverse("dashboard")))
    save_page("iot_dashboard.html", admin_client.get(reverse("iot_monitoring_dashboard")))

    receptionist_client = Client()
    receptionist_client.force_login(receptionist)
    save_page("receptionist_dashboard.html", receptionist_client.get(reverse("receptionist_dashboard")))

    print(f"Exported HTML page snapshots to {PAGE_EXPORT_DIR}")


def capture_screenshots_with_quicklook(base_url: str, database_path: Path) -> None:
    export_html_pages(base_url, database_path)

    page_map = [
        ("login_page.html", "login_page.png"),
        ("rooms_page.html", "rooms_page.png"),
        ("booking_page.html", "booking_page.png"),
        ("payment_page.html", "payment_page.png"),
        ("admin_dashboard.html", "admin_dashboard.png"),
        ("iot_dashboard.html", "iot_dashboard.png"),
        ("receptionist_dashboard.html", "receptionist_dashboard.png"),
    ]
    html_paths = [str(PAGE_EXPORT_DIR / html_name) for html_name, _ in page_map]
    subprocess.run(
        ["qlmanage", "-t", "-s", "1400", "-o", str(SCREENSHOT_DIR), *html_paths],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    for html_name, png_name in page_map:
        quicklook_output = SCREENSHOT_DIR / f"{html_name}.png"
        if quicklook_output.exists():
            quicklook_output.replace(SCREENSHOT_DIR / png_name)

    print(f"Rendered Quick Look screenshots in {SCREENSHOT_DIR}")


def capture_screenshots(base_url: str, database_path: Path) -> None:
    ensure_directories()

    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import SessionNotCreatedException
    except Exception:
        capture_screenshots_with_quicklook(base_url, database_path)
        return

    try:
        driver = webdriver.Safari()
    except SessionNotCreatedException:
        capture_screenshots_with_quicklook(base_url, database_path)
        return

    wait = WebDriverWait(driver, 20)

    def resize_view(height: int = 1500) -> None:
        driver.set_window_rect(x=40, y=40, width=1440, height=height)
        time.sleep(0.8)

    def save(name: str, height: int = 1500) -> None:
        resize_view(height)
        driver.save_screenshot(str(SCREENSHOT_DIR / name))

    def login(email: str, password: str) -> None:
        driver.get(f"{base_url}/login/")
        wait.until(EC.visibility_of_element_located((By.ID, "id_username"))).clear()
        driver.find_element(By.ID, "id_username").send_keys(email)
        driver.find_element(By.ID, "id_password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1.5)

    try:
        driver.get(f"{base_url}/login/")
        wait.until(EC.visibility_of_element_located((By.ID, "id_username")))
        save("login_page.png", 1200)

        driver.get(f"{base_url}/rooms/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".rooms-page")))
        save("rooms_page.png", 1650)

        login("guest.demo@example.com", "GuestDemo123!")

        driver.get(f"{base_url}/online-booking/?room=3&new=1")
        wait.until(EC.visibility_of_element_located((By.ID, "booking-form")))
        driver.find_element(By.ID, "room_id").send_keys("Room 103")
        check_in = driver.find_element(By.ID, "check_in")
        check_in.clear()
        check_in.send_keys("2026-03-29")
        check_out = driver.find_element(By.ID, "check_out")
        check_out.clear()
        check_out.send_keys("2026-03-31")
        save("booking_page.png", 1450)

        driver.find_element(By.CSS_SELECTOR, ".submit-btn").click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".table.table-bordered")))
        save("payment_page.png", 1500)

        driver.get(f"{base_url}/logout/")
        time.sleep(1)

        login("admin.demo@rosegold.com", "AdminDemo123!")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".admin-stat-grid")))
        save("admin_dashboard.png", 1700)

        driver.get(f"{base_url}/monitoring/iot/")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#iot-room-grid")))
        save("iot_dashboard.png", 1850)

        driver.get(f"{base_url}/logout/")
        time.sleep(1)

        login("reception.demo@rosegold.com", "ReceptionDemo123!")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".admin-page-wrap")))
        save("receptionist_dashboard.png", 1750)

    finally:
        driver.quit()

    print(f"Captured screenshots in {SCREENSHOT_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate documentation assets for the chapter 2/3/4 report.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    seed_parser = subparsers.add_parser("seed-demo", help="Create a clean demo database used for screenshots.")
    seed_parser.add_argument("--database", type=Path, default=DEMO_DB_PATH)
    seed_parser.add_argument("--no-reset", action="store_true")

    subparsers.add_parser("flowcharts", help="Generate feature flowchart images and the Chapter 3 ERD.")
    subparsers.add_parser("erd", help="Generate only the Chapter 3 entity-relationship diagram.")

    screenshots_parser = subparsers.add_parser("screenshots", help="Capture screenshots from a running local server.")
    screenshots_parser.add_argument("--base-url", default="http://127.0.0.1:8010")
    screenshots_parser.add_argument("--database", type=Path, default=DEMO_DB_PATH)

    args = parser.parse_args()

    if args.command == "seed-demo":
        seed_demo_database(args.database, reset=not args.no_reset)
    elif args.command == "flowcharts":
        generate_flowcharts()
    elif args.command == "erd":
        generate_erd_diagram()
    elif args.command == "screenshots":
        capture_screenshots(args.base_url.rstrip("/"), args.database)


if __name__ == "__main__":
    main()
