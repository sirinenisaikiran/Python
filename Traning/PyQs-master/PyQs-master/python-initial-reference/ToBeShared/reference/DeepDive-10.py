###GRPC 
$ pip install grpcio grpcio-tools grpcio-reflection

##Proto file - protos/helloworld.proto
//To add comments to your .proto files, use C/C++-style // and /* ... */ syntax. 

syntax = "proto3";  //https://developers.google.com/protocol-buffers/docs/proto3

//Causes top-level messages, enums, and services to be defined at the package level, rather than 
//inside an outer class named after the .proto file
option java_multiple_files = true;
//The package you want to use for your generated Java classes.
option java_package = "python.examples.helloworld";
//The class name for the outermost Java class (and hence the file name) you want to generate.
option java_outer_classname = "HelloWorldProto";
//Sets the Objective-C class prefix which is prepended to all Objective-C generated classes and enums from this .proto
option objc_class_prefix = "HLW";
//option optimize_for = CODE_SIZE; //SPEED, LITE_RUNTIME

//in python this is ignored 
package helloworld;

// The greeting service definition.
service Greeter {
  // Takes HelloRequest and returns HelloReply
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// Check how to assign unique Field Number(frequent fields - 1 to 15)
//https://developers.google.com/protocol-buffers/docs/proto3#assigning-field-numbers
//creates .name getter and setter 
message HelloRequest {
  string name = 1;
}

/*
https://developers.google.com/protocol-buffers/docs/proto3
Types 
Scalar - double,float, int32, int64, uint32, uint64, string , bool 
    Each has std default value
enum Corpus {  UNIVERSAL = 0;, ...}
Other message type eg HelloRequest
map<key_type, value_type> map_field = N;
Oneof:  Like discriminated union 
Any (bytes) after import "google/protobuf/any.proto";
By Default 'required', but can have 'optional' profix
'repeated' prefix means List 
You can nest messages as deeply as you like, then access like 
    SearchResponse.Result result = 1;
Fields can be removed, as long as the field number is not used again in updated message type.
int32, uint32, int64, uint64, and bool are all compatible 
string and bytes are compatible as long as the bytes are valid UTF-8. 
Changing a single value into a member of a new oneof is safe and binary compatible
*/

message HelloReply {
  string message = 1;
}





#Generate stub 
$ python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/helloworld.proto

Generates 
helloworld_pb2.py
    Used by Client, Servers , containing all message definition
helloworld_pb2_grpc.py
    Used by Server , Extend from Servicer class 
    And use add_GreeterServicer_to_server to add this servicer to Server 
    Used by Client, uses Stub 
    
    
##server, greeter_server.py 
from concurrent import futures
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
#With gprc reflections 
#Server reflection is a service defined to provides information 
#about publicly-accessible gRPC services on a gRPC server.
#It is used by gRPC CLI, which can be used to introspect server protos and send/receive test RPCs
from grpc_reflection.v1alpha import reflection
def serve_public():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    SERVICE_NAMES = (
        helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

    
##client: greeter_client.py 
from __future__ import print_function
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    
#With channel options 
def run_options():
    # For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
    with grpc.insecure_channel(target='localhost:50051',
                               options=[('grpc.lb_policy_name', 'pick_first'),
                                        ('grpc.enable_retries', 0),
                                        ('grpc.keepalive_timeout_ms', 10000)
                                       ]) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        # Timeout in seconds.
        # https://grpc.io/grpc/python/grpc.html
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'),
                                 timeout=10)
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()


##Use Evans , https://github.com/ktr0731/evans/releases
#More uses eg streaming etc - https://github.com/ktr0731/evans
$ evans -r --port 50051 --host localhost repl

> show package
> show service
> show service  helloworld
> show message helloworld
> desc HelloReply
#call service 
> service Greeter
> call SayHello
name (TYPE_STRING) => 
> quit

##Usage of gprc_cli (windows prebuilt not available)
#List all the services exposed at a given port
$ grpc_cli ls localhost:50051

#output:
helloworld.Greeter
grpc.reflection.v1alpha.ServerReflection

#List one service with details, helloworld.Greeter is full name of the service.
$ grpc_cli ls localhost:50051 helloworld.Greeter -l

#output:
filename: helloworld.proto
package: helloworld;
service Greeter {
  rpc SayHello(helloworld.HelloRequest) returns (helloworld.HelloReply) {}
}

#List one method with details
$ grpc_cli ls localhost:50051 helloworld.Greeter.SayHello -l

#output:
rpc SayHello(helloworld.HelloRequest) returns (helloworld.HelloReply) {}

#Get information about the request type
$ grpc_cli type localhost:50051 helloworld.HelloRequest

#output:
message HelloRequest {
  optional string name = 1;
}

#Call a unary method Send a rpc to a helloworld server at localhost:50051:
$ grpc_cli call localhost:50051 SayHello "name: 'gRPC CLI'"

#output:  
message: "Hello gRPC CLI"

#Use local proto files
$ grpc_cli call localhost:50051 SayHello "name: 'world'" --protofiles=../protos/helloworld.proto

#Send non-proto rpc
$ grpc_cli call localhost:50051 /helloworld.Greeter/SayHello \
      --input_binary_file=input.bin \
      --output_binary_file=output.bin


###Complex Gprc - Routes servers
https://grpc.io/docs/languages/python/basics/

#In Python stream is modelled as Iterator for recieving and generator/yield for Sending 
$ python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/route_guide.proto



##route_guide.proto - generates route_guide_pb2.py, route_guide_pb2_grpc.py
syntax = "proto3";

option java_multiple_files = true;
option java_package = "examples.routeguide";
option java_outer_classname = "RouteGuideProto";
option objc_class_prefix = "RTG";

package routeguide;

// Interface exported by the server.
service RouteGuide {
  // A simple RPC.
  //
  // Obtains the feature at a given position.
  //
  // A feature with an empty name is returned if there's no feature at the given
  // position.
  rpc GetFeature(Point) returns (Feature) {}

  // A server-to-client streaming RPC.
  //
  // Obtains the Features available within the given Rectangle.  Results are
  // streamed rather than returned at once (e.g. in a response message with a
  // repeated field), as the rectangle may cover a large area and contain a
  // huge number of features.
  rpc ListFeatures(Rectangle) returns (stream Feature) {}

  // A client-to-server streaming RPC.
  //
  // Accepts a stream of Points on a route being traversed, returning a
  // RouteSummary when traversal is completed.
  rpc RecordRoute(stream Point) returns (RouteSummary) {}

  // A Bidirectional streaming RPC.
  //
  // Accepts a stream of RouteNotes sent while a route is being traversed,
  // while receiving other RouteNotes (e.g. from other users).
  rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
}

// Points are represented as latitude-longitude pairs in the E7 representation
// (degrees multiplied by 10**7 and rounded to the nearest integer).
// Latitudes should be in the range +/- 90 degrees and longitude should be in
// the range +/- 180 degrees (inclusive).
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}

// A latitude-longitude rectangle, represented as two diagonally opposite
// points "lo" and "hi".
message Rectangle {
  // One corner of the rectangle.
  Point lo = 1;

  // The other corner of the rectangle.
  Point hi = 2;
}

// A feature names something at a given point.
//
// If a feature could not be named, the name is empty.
message Feature {
  // The name of the feature.
  string name = 1;

  // The point where the feature is detected.
  Point location = 2;
}

// A RouteNote is a message sent while at a given point.
message RouteNote {
  // The location from which the message is sent.
  Point location = 1;

  // The message to be sent.
  string message = 2;
}

// A RouteSummary is received in response to a RecordRoute rpc.
//
// It contains the number of individual points received, the number of
// detected features, and the total distance covered as the cumulative sum of
// the distance between each point.
message RouteSummary {
  // The number of points received.
  int32 point_count = 1;

  // The number of known features passed while traversing the route.
  int32 feature_count = 2;

  // The distance covered in metres.
  int32 distance = 3;

  // The duration of the traversal in seconds.
  int32 elapsed_time = 4;
}

##route_guide_db.json
[{
    "location": {
        "latitude": 407838351,
        "longitude": -746143763
    },
    "name": "Patriots Path, Mendham, NJ 07945, USA"
}, {
    "location": {
        "latitude": 408122808,
        "longitude": -743999179
    },
    "name": "101 New Jersey 10, Whippany, NJ 07981, USA"
}, ...]

#Server - route_guide_server.py 
"""The Python implementation of the gRPC route guide server."""

from concurrent import futures
import time
import math
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

def read_route_guide_database():
    """Reads the route guide database.

  Returns:
    The full contents of the route guide database as a sequence of
      route_guide_pb2.Features.
  """
    feature_list = []
    with open("route_guide_db.json") as route_guide_db_file:
        for item in json.load(route_guide_db_file):
            feature = route_guide_pb2.Feature(
                name=item["name"],
                location=route_guide_pb2.Point(
                    latitude=item["location"]["latitude"],
                    longitude=item["location"]["longitude"]))
            feature_list.append(feature)
    return feature_list


def get_feature(feature_db, point):
    """Returns Feature at given location or None."""
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


def get_distance(start, end):
    """Distance between two points."""
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    # Formula is based on http://mathforum.org/library/drmath/view/51879.html
    a = (pow(math.sin(delta_lat_rad / 2), 2) +
         (math.cos(lat_rad_1) * math.cos(lat_rad_2) *
          pow(math.sin(delta_lon_rad / 2), 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000
    # metres
    return R * c


class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self):
        self.db = route_guide_resources.read_route_guide_database()

    def GetFeature(self, request, context):
        feature = get_feature(self.db, request)
        if feature is None:
            return route_guide_pb2.Feature(name="", location=request)
        else:
            return feature

    def ListFeatures(self, request, context):
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if (feature.location.longitude >= left and
                    feature.location.longitude <= right and
                    feature.location.latitude >= bottom and
                    feature.location.latitude <= top):
                yield feature

    def RecordRoute(self, request_iterator, context):
        point_count = 0
        feature_count = 0
        distance = 0.0
        prev_point = None

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)
            prev_point = point

        elapsed_time = time.time() - start_time
        return route_guide_pb2.RouteSummary(point_count=point_count,
                                            feature_count=feature_count,
                                            distance=int(distance),
                                            elapsed_time=int(elapsed_time))

    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

#Client - route_guide_client.py 
from __future__ import print_function

import random
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc
import route_guide_resources


def make_route_note(message, latitude, longitude):
    return route_guide_pb2.RouteNote(
        message=message,
        location=route_guide_pb2.Point(latitude=latitude, longitude=longitude))


def guide_get_one_feature(stub, point):
    feature = stub.GetFeature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print("Found no feature at %s" % feature.location)


def guide_get_feature(stub):
    guide_get_one_feature(
        stub, route_guide_pb2.Point(latitude=409146138, longitude=-746188906))
    guide_get_one_feature(stub, route_guide_pb2.Point(latitude=0, longitude=0))


def guide_list_features(stub):
    rectangle = route_guide_pb2.Rectangle(
        lo=route_guide_pb2.Point(latitude=400000000, longitude=-750000000),
        hi=route_guide_pb2.Point(latitude=420000000, longitude=-730000000))
    print("Looking for features between 40, -75 and 42, -73")

    features = stub.ListFeatures(rectangle)

    for feature in features:
        print("Feature called %s at %s" % (feature.name, feature.location))


def generate_route(feature_list):
    for _ in range(0, 10):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print("Visiting point %s" % random_feature.location)
        yield random_feature.location


def guide_record_route(stub):
    feature_list = route_guide_resources.read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = stub.RecordRoute(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Travelled %s meters " % route_summary.distance)
    print("It took %s seconds " % route_summary.elapsed_time)


def generate_messages():
    messages = [
        make_route_note("First message", 0, 0),
        make_route_note("Second message", 0, 1),
        make_route_note("Third message", 1, 0),
        make_route_note("Fourth message", 0, 0),
        make_route_note("Fifth message", 1, 0),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.message, msg.location))
        yield msg


def guide_route_chat(stub):
    responses = stub.RouteChat(generate_messages())
    for response in responses:
        print("Received message %s at %s" %
              (response.message, response.location))


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- GetFeature --------------")
        guide_get_feature(stub)
        print("-------------- ListFeatures --------------")
        guide_list_features(stub)
        print("-------------- RecordRoute --------------")
        guide_record_route(stub)
        print("-------------- RouteChat --------------")
        guide_route_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()



###Multiplex Server and Client - A server can serve as many Proto RPC as it wants 

##Server 
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
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
        route_guide_server.RouteGuideServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
    
##Client 
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



###Other Functionality 
Interceptors (client, server)
    Check gprc_examples in github or advanced\web\gprc_examples\python\interceptors\* 
MetaData 
    Check gprc_examples in github or advanced\web\gprc_examples\python\metadata\* 
SSL and Auth 
    Check gprc_examples in github or advanced\web\gprc_examples\python\auth\* 

API Reference 
    https://grpc.github.io/grpc/python/



    
