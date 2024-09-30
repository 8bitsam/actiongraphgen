#############################################################################
#
# (c) 2024 The Trustees of Columbia University in the City of New York.
# All rights reserved.
#
# File coded by: Billinge Group members and community contributors.
#
# See GitHub contributions for a more detailed list of contributors.
# https://github.com/8bitsam/actiongraphgen/graphs/contributors
#
# See LICENSE.rst for license information.
#
#############################################################################

import asyncio
from collections import defaultdict


class MessageBus:
    """A class that handles asynchronous event-driven data streaming for action graphs."""

    def __init__(self):
        """Constructor method"""
        self.channels = defaultdict(list)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def register_listener(self, channel: str, listener):
        """Register a node to listen to a specific channel.
        :param channel: The channel to listen to.
        :type channel: str

        :param listener: The listener to register.
        :type listener: callable
        """

        self.channels[channel].append(listener)

    async def publish_event(self, channel: str, data: list):
        """Publish an event to a specific channel asynchronously.
        :param channel: The channel to publish to.
        :type channel: str

        :param data: The data to publish.
        :type data: list
        """
        if channel not in self.channels:
            return

        listeners = self.channels[channel]
        tasks = [listener.process_event(data) for listener in listeners]
        await asyncio.gather(*tasks)

    async def start_stream(self, input_events: list):
        """Start the asynchronous stream of input events.
        :param input_events: A list of input events.
        :type input_events: list
        """
        tasks = [self.publish_event(event["channel"], event["data"]) for event in input_events]
        self.loop.run_until_complete(asyncio.gather(*tasks))


class NodeListener:
    """A class representing a node that listens for data events in the message bus.
    :param node_id: The node id.
    :type node_id: int

    :param graph: The action graph to listen to.
    :type graph: ActionGraph

    :param message_bus: A message bus instance.
    :type message_bus: MessageBus
    """

    def __init__(self, node_id: int, graph, message_bus: MessageBus):
        """Constructor method"""
        self.node_id = node_id
        self.graph = graph
        self.message_bus = message_bus
        self.message_bus.register_listener(f"node_{node_id}", self)

    async def process_event(self, data: list):
        """Process an incoming event and propagate it to child nodes.
        :param data: Input data stream.
        :type data: list
        """
        # Update operations (params) with incoming data
        for param in self.graph.param_types:
            if param in data:
                self.graph.data.data_list[self.node_id][param] = data[param]

        # Process the node's operation and propagate it to the children
        processed_data = self.graph.data.process_node(self.node_id, data)
        children = self.graph.get_children(self.node_id)

        # Propagate to children nodes by publishing events to their channels
        tasks = [self.message_bus.publish_event(f"node_{child}", processed_data) for child in children]
        await asyncio.gather(*tasks)
