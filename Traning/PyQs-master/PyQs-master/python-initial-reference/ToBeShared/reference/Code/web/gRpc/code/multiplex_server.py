"""A gRPC server servicing both Greeter and RouteGuide RPCs."""

from concurrent import futures
import time
import math
import logging

import grpc

import greeter_server
import route_guide_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(greeter_server.GreeterServicer(), server)
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(route_guide_server.RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
