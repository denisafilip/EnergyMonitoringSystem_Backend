import grpc
import chat_pb2
import chat_pb2_grpc


class ChatClient:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

    def send_message(self, sender, receiver, content):
        message = chat_pb2.ChatMessage(
            sender=sender, receiver=receiver, content=content)
        self.stub.sendMessage(message)

    def receive_message(self):
        for message in self.stub.receiveMessage(chat_pb2.Empty()):
            yield message


client = ChatClient()
client.send_message('Alice', 'Bob', 'Hello, Bob!')
client.send_message('Bob', 'Alice', 'Hi, Alice!')
for message in client.receive_message():
    print(f'{message.sender}: {message.content}')
