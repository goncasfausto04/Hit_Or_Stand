"""Broad-phase projectile collisions without scanning every enemy per bullet."""
from enemy import DuplicateMonster


class EnemyGrid:
    """Index one frame's enemy positions while keeping sprite-group hit order."""

    def __init__(self, enemies, cell_size=96):
        self.cell_size = cell_size
        self._cells = {}
        self._order = {}
        self._next_order = 0
        for enemy in enemies:
            self.add(enemy)

    def _keys(self, rect):
        size = self.cell_size
        for x in range(rect.left // size, (rect.right - 1) // size + 1):
            for y in range(rect.top // size, (rect.bottom - 1) // size + 1):
                yield x, y

    def add(self, enemy):
        self._order[enemy] = self._next_order
        self._next_order += 1
        for key in self._keys(enemy.rect):
            self._cells.setdefault(key, []).append(enemy)

    def remove(self, enemy):
        # Buckets last one frame; inactive entries can be discarded on rebuild.
        self._order.pop(enemy, None)

    def first_collision(self, rect):
        candidates = set()
        for key in self._keys(rect):
            candidates.update(self._cells.get(key, ()))
        return min((enemy for enemy in candidates
                    if enemy in self._order and enemy.rect.colliderect(rect)),
                   key=self._order.__getitem__, default=None)


def resolve_projectile_hits(player, bullets, enemies):
    """Apply hits in their original order and return the number of kills."""
    grid = None
    kills = 0
    for bullet in bullets:
        if getattr(bullet, "is_enemy_bullet", False):
            if player.rect.colliderect(bullet.rect):
                if not player.invincible:
                    player.health -= bullet.damage
                bullet.kill()
            continue

        if grid is None:
            grid = EnemyGrid(enemies)
        enemy = grid.first_collision(bullet.rect)
        if enemy is None:
            continue
        enemy.health -= bullet.damage * (100000 if player.oneshotkill else 1)
        bullet.kill()
        if enemy.health <= 0:
            if isinstance(enemy, DuplicateMonster):
                for child in enemy.spawn_on_death(enemies):
                    grid.add(child)
            enemy.kill()
            grid.remove(enemy)
            kills += 1
    return kills
