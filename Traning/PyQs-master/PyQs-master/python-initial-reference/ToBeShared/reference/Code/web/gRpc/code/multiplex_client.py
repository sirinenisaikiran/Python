"""A client that makes both Greeter and RouteGuide RPCs."""

from __future__ import print_function

import random
import time
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_client

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        greeter_stub = helloworld_pb2_grpc.GreeterStub(channel)
        route_guide_stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        greeter_response = greeter_stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
        print("Greeter client received: " + greeter_response.message)
        print("-------------- GetFeature --------------")
        route_guide_client.guide_get_feature(route_guide_stub)
        print("-------------- ListFeatures --------------")
        route_guide_client.guide_list_features(route_guide_stub)
        print("-------------- RecordRoute --------------")
        route_guide_client.guide_record_route(route_guide_stub)
        print("-------------- RouteChat --------------")
        route_guide_client.guide_route_chat(route_guide_stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
