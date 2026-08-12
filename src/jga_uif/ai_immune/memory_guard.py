class MemoryGuard:
    def authorize_write(self, actor: str, owner: str) -> bool:
        return actor == owner
