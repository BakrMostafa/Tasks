from project.settings import DEBUG


def website_context(request):
    debug = DEBUG
    return {
        "debug": debug,
    }
