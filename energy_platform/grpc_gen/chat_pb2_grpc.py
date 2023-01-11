# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_pb2 as chat__pb2


class ChatServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.sendMessage = channel.unary_unary(
                '/ChatService/sendMessage',
                request_serializer=chat__pb2.ChatMessage.SerializeToString,
                response_deserializer=chat__pb2.Empty.FromString,
                )
        self.receiveMessage = channel.unary_stream(
                '/ChatService/receiveMessage',
                request_serializer=chat__pb2.Empty.SerializeToString,
                response_deserializer=chat__pb2.ChatMessage.FromString,
                )
        self.typeMessage = channel.unary_unary(
                '/ChatService/typeMessage',
                request_serializer=chat__pb2.Notification.SerializeToString,
                response_deserializer=chat__pb2.Empty.FromString,
                )


class ChatServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def sendMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def receiveMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def typeMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'sendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.sendMessage,
                    request_deserializer=chat__pb2.ChatMessage.FromString,
                    response_serializer=chat__pb2.Empty.SerializeToString,
            ),
            'receiveMessage': grpc.unary_stream_rpc_method_handler(
                    servicer.receiveMessage,
                    request_deserializer=chat__pb2.Empty.FromString,
                    response_serializer=chat__pb2.ChatMessage.SerializeToString,
            ),
            'typeMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.typeMessage,
                    request_deserializer=chat__pb2.Notification.FromString,
                    response_serializer=chat__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ChatService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def sendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/sendMessage',
            chat__pb2.ChatMessage.SerializeToString,
            chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def receiveMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ChatService/receiveMessage',
            chat__pb2.Empty.SerializeToString,
            chat__pb2.ChatMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def typeMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ChatService/typeMessage',
            chat__pb2.Notification.SerializeToString,
            chat__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
