from concurrent import futures

import chat_pb2 as chat_pb2
import chat_pb2_grpc as chat_pb2_grpc
import grpc


class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []

    def sendMessage(self, request, context):
        # Implement the logic for handling a message sent from the client
        # sender = models.User.objects.filter(email=request.sender).first()
        # receiver = models.User.objects.filter(email=request.receiver).first()
        """if sender and receiver:
            models.ChatMessage.objects.create(
                sender=sender, receiver=receiver, content=request.content
            )"""
        print(f"Received message from {request.sender}: {request.content}")
        self.messages.append(chat_pb2.ChatMessage(sender=request.sender,
                                                  receiver=request.receiver,
                                                  content=request.content,
                                                  timestamp=request.timestamp))
        return chat_pb2.Empty()

    def receiveMessage(self, request, context):
        # Implement the logic for sending a stream of messages to the client
        for message in self.messages:
            yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
