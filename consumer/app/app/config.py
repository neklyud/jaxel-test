from betterconf import field, Config


class ConsumerConfig(Config):
    kafka_host = field("KAFKA_HOST", default="localhost:9092")
    kafka_transfer_topik = field("KAFKA_TRANSFER_TOPIC", default='producer2consumer')
    postgres_host = field('POSTGRES_HOST')
    postgres_port = field('POSTGRES_PORT')
    postgres_password = field('POSTGRES_PASSWORD')
    postgres_user = field('POSTGRES_USER')
    market_db = field('MARKET_DB', default="market_db")

config = ConsumerConfig()
