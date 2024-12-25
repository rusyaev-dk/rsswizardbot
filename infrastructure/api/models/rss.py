from infrastructure.database.models.rss import RSSLocal


class RSS:
    def __init__(
            self,
            rss_id: str,
            rss_url: str,
            owner_tg_id: int
    ):
        self.rss_id = rss_id
        self.rss_url = rss_url
        self.owner_tg_id = owner_tg_id

    @classmethod
    def from_local(
            cls,
            local: RSSLocal
    ) -> 'RSS':
        return cls(
            rss_id=local.rss_id,
            rss_url=local.rss_url,
            owner_tg_id=local.owner_tg_id,
        )
