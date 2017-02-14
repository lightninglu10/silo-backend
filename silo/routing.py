from channels.routing import route, route_class
from channels.staticfiles import StaticFilesConsumer
from messagesapp import consumers as messages_consumers

# routes defined for channel calls
# this is similar to the Django urls, but specifically for Channels
channel_routing = [
    route_class(messages_consumers.MessagesConsumer, path=r'^/api/channels/messages/')
]