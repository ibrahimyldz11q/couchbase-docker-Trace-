from flask import Flask
from couchbase.cluster import Cluster, PasswordAuthenticator
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)

# Couchbase bağlantısı
cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('username', 'password')
cluster.authenticate(authenticator)
bucket = cluster.bucket('your_bucket_name')
collection = bucket.default_collection()

# Jaeger konfigürasyonu
config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
    },
    service_name='your-flask-app',
)

# Jaeger örneği oluştur
tracer = config.initialize_tracer()

# FlaskTracing ile Flask uygulamasını sar
tracing = FlaskTracing(tracer, True, app)

@app.route('/')
def home():
    with tracer.start_span('couchbase-operation'):
        # Couchbase operasyonu
        result = collection.get('your_document_key')
        value = result.content_as[str]()
        return f'Value from Couchbase: {value}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
