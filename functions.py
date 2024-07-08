import pygame


def draw_rounded_rect(surface, color, rect, corner_radius):
    corner_radius = min(corner_radius, min(rect.width, rect.height) / 2)

    x, y, w, h = rect
    rounded_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    rects = [
        (corner_radius, 0, w - 2 * corner_radius, h),
        (0, corner_radius, w, h - 2 * corner_radius)
    ]
    circles = [
        (corner_radius, corner_radius),
        (w - corner_radius, corner_radius),
        (corner_radius, h - corner_radius),
        (w - corner_radius, h - corner_radius)
    ]

    for r in rects:
        pygame.draw.rect(rounded_surface, color, r)

    for c in circles:
        pygame.draw.circle(rounded_surface, color, c, corner_radius)

    surface.blit(rounded_surface, (x, y), special_flags=pygame.BLEND_RGBA_MAX)
