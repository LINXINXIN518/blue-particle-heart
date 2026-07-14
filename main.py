import pygame
import random
import math
import sys


# =========================
# 基础配置（未改动）
# =========================
FPS = 60

pygame.init()

info = pygame.display.Info()
SCREEN_W, SCREEN_H = info.current_w, info.current_h

WIDTH = int(SCREEN_W * 0.80)
HEIGHT = int(SCREEN_H * 0.80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("80%画板：实心圆碎片生成蓝色3D爱心")
clock = pygame.time.Clock()

BG_COLOR = (3, 5, 10)

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2 - 35

# ✅ 保持原粒子数
TOTAL_PARTICLES = 6200

BUILD_SECONDS = 6.2
FLY_SPEED_MIN = 0.024
FLY_SPEED_MAX = 0.038

HEART_SCALE = min(WIDTH, HEIGHT) * 0.255
HEART_WIDTH = 1.08
HEART_HEIGHT = 1.12
HEART_DEPTH = 1.28


BOTTOM_PARTICLE_SIZE = 2
FLY_PARTICLE_SIZE = 2
HEART_PARTICLE_SIZE = 2

HEART_ROTATE_SPEED = 0.9
BOTTOM_ROTATE_SPEED_MIN = 4.8
BOTTOM_ROTATE_SPEED_MAX = 8.0

# =========================
# 底部实心圆参数（未改动）
# =========================
BOTTOM_CIRCLE_CENTER_X = WIDTH // 2
BOTTOM_CIRCLE_CENTER_Y = HEIGHT - int(HEIGHT * 0.14)

BOTTOM_CIRCLE_RADIUS_X = min(WIDTH * 0.25, 330)
BOTTOM_CIRCLE_RADIUS_Y = min(HEIGHT * 0.105, 85)

BOTTOM_LOCAL_RADIUS_X = 18
BOTTOM_LOCAL_RADIUS_Y = 7

ORBIT_RADIUS_MIN = 18
ORBIT_RADIUS_MAX = 58
ORBIT_TURNS_MIN = 2.2
ORBIT_TURNS_MAX = 3.8

SELF_ROTATE_SPEED_MIN = 0.18
SELF_ROTATE_SPEED_MAX = 0.38

BOTTOM_COLOR = (252, 252, 255)

# ✅ 唯一改动：紫色 → 蓝色
HEART_COLORS = [
    (180, 220, 255),  # 天蓝
    (150, 200, 255),  # 冰蓝
    (120, 180, 255),  # 中蓝
    (100, 160, 255),  # 霓虹蓝
    (140, 210, 255),  # 淡蓝
    (170, 230, 255),  # 雾蓝
]

# =========================
# 3D 爱心方程（未改动）
# =========================
def heart_value(x, y, z):
    a = x * x + 2.25 * y * y + z * z - 1
    return a * a * a - x * x * z * z * z - 0.1125 * y * y * z * z * z


def in_heart_3d(x, y, z):
    return heart_value(x, y, z) <= 0


def generate_surface_heart(count):
    points = []
    max_try = count * 350
    tries = 0

    while len(points) < count and tries < max_try:
        tries += 1
        x = random.uniform(-1.35, 1.35)
        y = random.uniform(-1.05, 1.15)
        z = random.uniform(-1.35, 1.35)

        if not in_heart_3d(x, y, z):
            continue

        length = math.sqrt(x * x + y * y + z * z)
        if length == 0:
            continue

        nx = x / length
        ny = y / length
        nz = z / length

        pushed_x = x + nx * 0.04
        pushed_y = y + ny * 0.04
        pushed_z = z + nz * 0.04

        if in_heart_3d(pushed_x, pushed_y, pushed_z):
            continue

        points.append({
            "x": x * HEART_WIDTH,
            "y": z * HEART_HEIGHT,
            "z": y * HEART_DEPTH
        })

    while len(points) < count:
        p = random.choice(points)
        points.append({
            "x": p["x"] * random.uniform(0.995, 1.005),
            "y": p["y"] * random.uniform(0.995, 1.005),
            "z": p["z"] * random.uniform(0.995, 1.005),
        })

    points.sort(key=lambda p: -p["y"])
    return points


def project_point(x, y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    rx = x * cos_a + z * sin_a
    rz = -x * sin_a + z * cos_a

    distance = 4.3
    perspective = distance / (distance - rz * 0.75)

    sx = CENTER_X + rx * HEART_SCALE * perspective
    sy = CENTER_Y - y * HEART_SCALE * perspective

    return sx, sy, rz, perspective


# =========================
# 碎片类（未改动）
# =========================
class Fragment:
    def __init__(self, target, index):
        self.tx = target["x"]
        self.ty = target["y"]
        self.tz = target["z"]

        angle = random.uniform(0, math.tau)
        radius_scale = math.sqrt(random.random())

        self.disk_angle = angle
        self.disk_radius_scale = radius_scale

        self.base_x = (
            BOTTOM_CIRCLE_CENTER_X
            + math.cos(angle) * BOTTOM_CIRCLE_RADIUS_X * radius_scale
            + random.gauss(0, 6)
        )
        self.base_y = (
            BOTTOM_CIRCLE_CENTER_Y
            + math.sin(angle) * BOTTOM_CIRCLE_RADIUS_Y * radius_scale
            + random.gauss(0, 3)
        )

        self.base_x = max(30, min(WIDTH - 30, self.base_x))
        self.base_y = max(HEIGHT - 180, min(HEIGHT - 20, self.base_y))

        self.x = self.base_x
        self.y = self.base_y
        self.delay = index / TOTAL_PARTICLES * BUILD_SECONDS * FPS

        self.progress = 0.0
        self.speed = random.uniform(FLY_SPEED_MIN, FLY_SPEED_MAX)
        self.state = "bottom"

        self.phase = random.uniform(0, math.tau)
        self.heart_color = random.choice(HEART_COLORS)

        self.disk_rotate_speed = -random.uniform(0.35, 0.65)
        self.bottom_angle = random.uniform(0, math.tau)
        self.bottom_spin = -random.uniform(
            BOTTOM_ROTATE_SPEED_MIN,
            BOTTOM_ROTATE_SPEED_MAX
        )

        self.bottom_rx = abs(random.gauss(BOTTOM_LOCAL_RADIUS_X, 7))
        self.bottom_ry = abs(random.gauss(BOTTOM_LOCAL_RADIUS_Y, 3))

        self.orbit_phase = random.uniform(0, math.tau)
        self.orbit_radius = random.uniform(ORBIT_RADIUS_MIN, ORBIT_RADIUS_MAX)
        self.orbit_turns = random.uniform(ORBIT_TURNS_MIN, ORBIT_TURNS_MAX)
        self.orbit_direction = -1

        self.self_angle = random.uniform(0, math.tau)
        self.self_rotate_speed = -random.uniform(
            SELF_ROTATE_SPEED_MIN,
            SELF_ROTATE_SPEED_MAX
        )

        self.start_x = self.x
        self.start_y = self.y

    def bottom_position(self, frame):
        time = frame / FPS
        disk_a = self.disk_angle + time * self.disk_rotate_speed

        disk_x = (
            BOTTOM_CIRCLE_CENTER_X
            + math.cos(disk_a) * BOTTOM_CIRCLE_RADIUS_X * self.disk_radius_scale
        )
        disk_y = (
            BOTTOM_CIRCLE_CENTER_Y
            + math.sin(disk_a) * BOTTOM_CIRCLE_RADIUS_Y * self.disk_radius_scale
        )

        local_a = self.bottom_angle + time * self.bottom_spin
        x = disk_x + math.cos(local_a) * self.bottom_rx
        y = disk_y + math.sin(local_a) * self.bottom_ry

        x += math.sin(frame * 0.08 + self.phase) * 0.8
        y += math.cos(frame * 0.07 + self.phase) * 0.4

        return x, y

    def update(self, frame, heart_angle):
        self.self_angle += self.self_rotate_speed

        if self.state == "bottom":
            if frame >= self.delay:
                self.start_x, self.start_y = self.bottom_position(frame)
                self.state = "flying"
            else:
                self.x, self.y = self.bottom_position(frame)
                return

        target_x, target_y, _, _ = project_point(
            self.tx, self.ty, self.tz, heart_angle
        )

        if self.state == "flying":
            self.progress += self.speed
            if self.progress >= 1:
                self.progress = 1
                self.state = "arrived"

            t = self.progress
            ease = 1 - (1 - t) ** 2.1

            mid_x = (self.start_x + target_x) / 2
            mid_y = min(self.start_y, target_y) - random.uniform(90, 170)

            bx = (
                (1 - ease) ** 2 * self.start_x
                + 2 * (1 - ease) * ease * mid_x
                + ease ** 2 * target_x
            )
            by = (
                (1 - ease) ** 2 * self.start_y
                + 2 * (1 - ease) * ease * mid_y
                + ease ** 2 * target_y
            )

            orbit_angle = (
                self.orbit_phase
                - t * math.tau * self.orbit_turns
                - frame * 0.055
            )
            ox = math.cos(orbit_angle) * self.orbit_radius * (1 - t) ** 0.7
            oy = math.sin(orbit_angle) * self.orbit_radius * 0.42 * (1 - t) ** 0.7

            float_x = math.sin(frame * 0.04 + self.phase) * 2.8 * (1 - t)
            float_y = math.cos(frame * 0.03 + self.phase) * 1.8 * (1 - t)

            self.x = bx + ox + float_x
            self.y = by + oy + float_y

        elif self.state == "arrived":
            tx, ty, _, _ = project_point(
                self.tx, self.ty, self.tz, heart_angle
            )
            self.x = tx
            self.y = ty

    def draw(self, surface, heart_angle):
        _, _, depth, _ = project_point(
            self.tx, self.ty, self.tz, heart_angle
        )

        if self.state == "bottom":
            pygame.draw.circle(
                surface,
                BOTTOM_COLOR,
                (int(self.x), int(self.y)),
                BOTTOM_PARTICLE_SIZE
            )

        elif self.state == "flying":
            t = self.progress
            mix = min(1.0, t * 3.5)

            br, bg, bb = BOTTOM_COLOR
            hr, hg, hb = self.heart_color

            r = int(br * (1 - mix) + hr * mix)
            g = int(bg * (1 - mix) + hg * mix)
            b = int(bb * (1 - mix) + hb * mix)

            pygame.draw.circle(
                surface,
                (r, g, b),
                (int(self.x), int(self.y)),
                FLY_PARTICLE_SIZE
            )

        else:
            light = (depth + 1.5) / 3.0
            light = max(0.5, min(1.2, light))

            r = min(255, int(self.heart_color[0] * light))
            g = min(255, int(self.heart_color[1] * light))
            b = min(255, int(self.heart_color[2] * light))

            pygame.draw.circle(
                surface,
                (r, g, b),
                (int(self.x), int(self.y)),
                HEART_PARTICLE_SIZE
            )


# =========================
# 主程序（未改动）
# =========================
def main():
    print("正在生成蓝色爱心，请稍候...")

    targets = generate_surface_heart(TOTAL_PARTICLES)
    fragments = [Fragment(targets[i], i) for i in range(TOTAL_PARTICLES)]

    frame = 0

    while True:
        clock.tick(FPS)
        frame += 1

        heart_angle = -frame / FPS * HEART_ROTATE_SPEED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        for f in fragments:
            f.update(frame, heart_angle)

        for f in fragments:
            f.draw(screen, heart_angle)

        pygame.display.flip()


if __name__ == "__main__":
    main()