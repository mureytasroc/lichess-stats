import os


def in_prod():
    return os.environ.get("FASTAPI_ENV") == "production"


def setup_sentry(app):
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])
    app.add_middleware(SentryAsgiMiddleware)
