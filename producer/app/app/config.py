from betterconf import field, Config
from betterconf.caster import to_int


class ProducerConfig(Config):
    listen_timeout = field("LISTEN_TIMEOUT", default=5, caster=to_int)
    kafka_host = field("KAFKA_HOST", default="localhost:9092")
    garantex_api_host = field("GARANTEX_API_HOST", default='https://garantex.io/api/v2/')
    kafka_transfer_topik = field("KAFKA_TRANSFER_TOPIC", default='producer2consumer')

config = ProducerConfig()
