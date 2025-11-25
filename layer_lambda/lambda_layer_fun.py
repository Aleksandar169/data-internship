from extra_lib import shout

def lambda_handler(event, context):
    msg = event.get("text", "default")
    return {
        "original": msg,
        "layer_result": shout(msg)
    }
